import os
import time
import win32file
import win32con
import threading
from collections import deque
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication
from .ob_02_BaseEvento import BaseEvento
from .ob_03_DiretorioScanner import ScanWorker
from .ob_04_EventoAdicionado import EventoAdicionado
from .ob_05_EventoExcluido import EventoExcluido
from .ob_06_EventoModificado import EventoModificado
from .ob_07_EventoRenomeado import EventoRenomeado
from .ob_10_GerenciadorColunas import GerenciadorColunas
from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

if not hasattr(win32con, 'FILE_NOTIFY_CHANGE_CREATION'):
    win32con.FILE_NOTIFY_CHANGE_CREATION = 0x00000040


class Observador:
    def __init__(self, diretorio, callback):
        self.diretorio = diretorio
        self.callback = callback
        self.ativo = False
        self.desligando = False
        self.thread = None
        self.ultimo_evento = None
        self.eventos_pendentes = {}
        self.registros_anteriores = {}
        self.eventos_ignorados = set()
        self.arquivos_recem_adicionados = {}
        self.arquivos_recem_excluidos = {}
        self.arquivos_recem_renomeados = {}
        self.arquivos_recem_modificados = {}
        self.ultima_modificacao = {}

        self._lock = threading.Lock()
        self.loc = LocalizadorQt()
        self.falhas_consecutivas = 0
        self.max_falhas = 3
        self.ultimo_erro = None
        self.buffer_eventos = deque(maxlen=1000000)
        self.evento_lock = threading.Lock()
        self.operacao_massiva_detectada = False
        self.contador_eventos_segundo = 0
        self.ultimo_reset_contador = time.time()
        self.thread_pool = []
        self.max_threads = 4
        self.total_eventos_recebidos = 0
        self.total_eventos_processados = 0
        self.eventos_perdidos_estimados = 0
        self.interface = None

        self.gerenciador_colunas = GerenciadorColunas(self)
        self.evento_base = BaseEvento(self)
        self.evento_adicionado = EventoAdicionado(self)
        self.evento_excluido = EventoExcluido(self)
        self.evento_modificado = EventoModificado(self)
        self.evento_renomeado = EventoRenomeado(self)

        self.ACOES = {
            1: self.loc.get_text("op_added"),
            2: self.loc.get_text("op_deleted"),
            3: self.loc.get_text("op_modified"),
            4: self.loc.get_text("op_renamed"),
            5: self.loc.get_text("op_renamed")
        }

        self.registros_lock = threading.Lock()
        self.thread_scan = None
        self.scan_worker = None
        self.pausado = False
        self._pause_event = threading.Event()
        self._pause_event.set()

    def detectar_operacao_massiva(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_reset_contador >= 1.0:
            if self.contador_eventos_segundo > 100:
                self.operacao_massiva_detectada = True
                logger.info(f"Operação massiva detectada: {self.contador_eventos_segundo} eventos/segundo")

            elif self.contador_eventos_segundo < 10:
                self.operacao_massiva_detectada = False

            self.contador_eventos_segundo = 0
            self.ultimo_reset_contador = tempo_atual

        self.contador_eventos_segundo += 1

    def iniciar(self):
        with self._lock:
            if not self.ativo:
                self.ativo = True
                self.desligando = False
                self.pausado = False
                try:
                    self._pause_event.set()

                except Exception:
                    pass

                from .ob_03_DiretorioScanner import DiretorioScanner
                self.scanner = DiretorioScanner(self)
                try:
                    self.scanner.pausado = False
                    self.scanner._pause_event.set()

                except Exception:
                    pass

                self.thread_scan = QThread()
                self.scan_worker = ScanWorker(self.scanner, self.diretorio)
                self.scan_worker.moveToThread(self.thread_scan)
                self.thread_scan.started.connect(self.scan_worker.run)
                self.scan_worker.finished.connect(self.iniciar_monitoramento)
                self.scan_worker.error.connect(self.handle_scan_error)
                self.scan_worker.finished.connect(self.thread_scan.quit)
                self.scan_worker.finished.connect(self.scan_worker.deleteLater)
                self.thread_scan.finished.connect(self.thread_scan.deleteLater)
                self.thread_scan.start()

    def handle_scan_error(self, error_msg):
        logger.error(f"Erro durante escaneamento: {error_msg}")
        self.ativo = False
        if hasattr(self, 'interface'):
            self.interface.rotulo_resultado.setText(f"Erro: {error_msg}")

    def iniciar_monitoramento(self):
        try:
            self.thread = threading.Thread(target=self.monitorar)
            self.thread.daemon = True
            self.thread.start()
            self.thread_buffer = threading.Thread(target=self.processar_buffer_eventos)
            self.thread_buffer.daemon = True
            self.thread_buffer.start()
            if hasattr(self, 'interface') and hasattr(self.interface, 'gerenciador_tabela'):
                self.interface.gerenciador_tabela.atualizar_dados_tabela(self.interface.tabela_dados)
                self.interface.atualizar_status()

            if hasattr(self, 'interface'):
                self.interface.rotulo_resultado.setText(self.interface.loc.get_text("monitoring_started"))
                self.interface.atualizar_status()

        except Exception as e:
            logger.error(f"Erro ao iniciar monitoramento: {e}", exc_info=True)

    def processar_buffer_eventos(self):
        INTERVALO_MAXIMO = 0.1
        ULTIMO_PROCESSAMENTO = [time.time()]
        while self.ativo:
            try:
                if not self._pause_event.is_set():
                    time.sleep(0.1)
                    continue

                processar_agora = False
                with self.evento_lock:
                    buffer_len = len(self.buffer_eventos)
                    tempo_atual = time.time()
                    if buffer_len >= 1:
                        processar_agora = True

                    elif buffer_len > 0 and (tempo_atual - ULTIMO_PROCESSAMENTO[0]) >= INTERVALO_MAXIMO:
                        processar_agora = True

                    if processar_agora:
                        eventos_para_processar = []
                        for _ in range(min(1, buffer_len)):
                            if self.buffer_eventos:
                                eventos_para_processar.append(self.buffer_eventos.popleft())

                        ULTIMO_PROCESSAMENTO[0] = tempo_atual

                    else:
                        eventos_para_processar = []

                for acao, nome_arquivo, tempo_evento in eventos_para_processar:
                    if not self._pause_event.is_set() or self.pausado:
                        with self.evento_lock:
                            self.buffer_eventos.appendleft((acao, nome_arquivo, tempo_evento))

                        logger.debug("Processamento pausado durante consumo do buffer; evento reenfileirado")
                        break

                    self._processar_evento_interno(acao, nome_arquivo, tempo_evento)

                if eventos_para_processar:
                    logger.info(f"Processados {len(eventos_para_processar)} eventos do buffer")

                if not eventos_para_processar:
                    time.sleep(0.01)

                else:
                    time.sleep(0.001)

            except Exception as e:
                logger.error(f"Erro ao processar buffer de eventos: {e}", exc_info=True)
                time.sleep(0.1)

    def parar_scan(self):
        if self.thread_scan:
            try:
                if self.thread_scan.isRunning():
                    self.desligando = True
                    self.ativo = False
                    try:
                        self.pausado = False
                        self._pause_event.set()
                        if hasattr(self, 'scan_worker') and hasattr(self.scan_worker, 'scanner'):
                            scanner = self.scan_worker.scanner
                            scanner.pausado = False
                            scanner._pause_event.set()

                    except Exception:
                        pass

                    self.thread_scan.requestInterruption()
                    self.thread_scan.quit()
                    self.thread_scan.wait(5000)

            except Exception as e:
                logger.error(f"Erro ao parar thread de escaneamento: {e}", exc_info=True)

            finally:
                self.thread_scan = None
                self.scan_worker = None

            try:
                if hasattr(self, 'interface') and self.interface:
                    try:
                        self.interface.rotulo_resultado.setText(self.interface.loc.get_text("monitoring_stopped"))

                    except Exception:
                        pass

                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            self.interface.barra_progresso.hide()
                            self.interface.barra_progresso.setValue(0)

                        except Exception:
                            pass

                    QApplication.processEvents()

            except Exception:
                pass

    def parar(self):
        with self._lock:
            self.parar_scan()
            if not self.ativo:
                try:
                    self.pausado = False
                    self._pause_event.set()
                    if hasattr(self, 'scanner') and self.scanner:
                        self.scanner.pausado = False
                        self.scanner._pause_event.set()

                except Exception:
                    pass

                return

            self.desligando = True
            self.ativo = False
            if self.thread:
                try:
                    win32file.CancelIo(self.handle_dir)
                    self.thread.join(timeout=0.05)
                    if hasattr(self, 'handle_dir'):
                        win32file.CloseHandle(self.handle_dir)
                        del self.handle_dir

                except Exception as e:
                    logger.error(f"Erro ao parar a thread: {e}", exc_info=True)

            self.limpar_estado()
            self.desligando = False
            logger.info(f"Estatísticas finais:")
            logger.info(f"  Eventos recebidos: {self.total_eventos_recebidos}")
            logger.info(f"  Eventos processados: {self.total_eventos_processados}")
            logger.info(f"  Eventos no buffer: {len(self.buffer_eventos)}")
            try:
                if hasattr(self, 'interface') and self.interface:
                    try:
                        self.interface.rotulo_resultado.setText(self.interface.loc.get_text("monitoring_stopped"))

                    except Exception:
                        pass

                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            self.interface.barra_progresso.hide()
                            self.interface.barra_progresso.setValue(0)

                        except Exception:
                            pass

                    QApplication.processEvents()

            except Exception:
                pass

    def limpar_estado(self):
        self.eventos_pendentes.clear()
        self.registros_anteriores.clear()
        self.eventos_ignorados.clear()
        self.arquivos_recem_adicionados.clear()
        self.arquivos_recem_excluidos.clear()
        self.ultima_modificacao.clear()

    def monitorar(self):
        BUFFER_SIZE = 16777216
        FILE_LIST_DIRECTORY = 0x0001
        try:
            self.handle_dir = None
            self.handle_dir = win32file.CreateFile(
                self.diretorio,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ |
                win32con.FILE_SHARE_WRITE |
                win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS |
                win32con.FILE_FLAG_OVERLAPPED,
                None
            )

        except Exception as e:
            logger.error(f"Erro ao criar handle de diretório: {e}", exc_info=True)
            self.handle_dir = None
            return

        while self.ativo:
            if not self._pause_event.is_set():
                time.sleep(0.1)
                continue

            try:
                self._pause_event.wait()
                results = win32file.ReadDirectoryChangesW(
                    self.handle_dir,
                    BUFFER_SIZE,
                    True,
                    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                    win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                    win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                    win32con.FILE_NOTIFY_CHANGE_SIZE |
                    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                    win32con.FILE_NOTIFY_CHANGE_SECURITY |
                    win32con.FILE_NOTIFY_CHANGE_CREATION,
                    None,
                    None
                )

                tempo_batch = time.time()
                self.total_eventos_recebidos += len(results)
                if len(results) > 500:
                    logger.warning(f"Batch grande detectado: {len(results)} eventos")
                    self.operacao_massiva_detectada = True
                    if hasattr(self, 'scan_worker'):
                        arquivos_atuais = set(os.listdir(self.diretorio))
                        arquivos_anteriores = set(self.registros_anteriores.keys())
                        arquivos_excluidos = arquivos_anteriores - arquivos_atuais
                        for nome_arquivo in arquivos_excluidos:
                            self.evento_excluido.processar(nome_arquivo, os.path.join(self.diretorio, nome_arquivo), time.time())

                for action, file in results:
                    self.detectar_operacao_massiva()
                    if self.operacao_massiva_detectada:
                        with self.evento_lock:
                            self.buffer_eventos.append((action, file, tempo_batch))

                    else:
                        self._processar_evento_interno(action, file, tempo_batch)

            except win32file.error as e:
                if self.desligando:
                    break

                logger.error(f"Erro no monitoramento: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro desconhecido: {e}", exc_info=True)

        try:
            if hasattr(self, 'handle_dir') and self.handle_dir is not None:
                win32file.CloseHandle(self.handle_dir)
                self.handle_dir = None

        except Exception as e:
            logger.error(f"Erro ao fechar handle de diretório: {e}", exc_info=True)

    def _processar_evento_interno(self, acao, nome_arquivo, tempo_evento):
        try:
            if self.pausado or not self._pause_event.is_set():
                with self.evento_lock:
                    self.buffer_eventos.appendleft((acao, nome_arquivo, tempo_evento))

                logger.debug("Pausado: evento recolocado no buffer em _processar_evento_interno")
                return

            self.total_eventos_processados += 1
            self.processar_evento(acao, nome_arquivo, tempo_evento)

        except Exception as e:
            logger.error(f"Erro ao processar evento interno: {e}", exc_info=True)

    def processar_evento(self, acao, nome_arquivo, tempo_evento=None):
        try:
            if self.pausado or not self._pause_event.is_set():
                logger.debug("processar_evento abortado devido a pausa")
                return

            if self.falhas_consecutivas >= self.max_falhas:
                print("Muitas falhas consecutivas, reiniciando monitoramento...")
                self.reiniciar_monitoramento()
                return

            caminho_completo = os.path.join(self.diretorio, nome_arquivo)
            tempo_atual = tempo_evento if tempo_evento else time.time()
            if nome_arquivo in self.eventos_ignorados:
                self.eventos_ignorados.remove(nome_arquivo)
                return

            if acao == 3 and os.path.isdir(caminho_completo):
                return

            ext = os.path.splitext(nome_arquivo)[1].lower()
            arquivos_especiais = {'.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mov', '.avi', '.mkv', '.xml'}
            if acao == 2:
                if nome_arquivo in self.arquivos_recem_excluidos:
                    tempo_limite = 1.0 if ext in arquivos_especiais else 0.1
                    if (tempo_atual - self.arquivos_recem_excluidos[nome_arquivo]) < tempo_limite:
                        return

                self.evento_excluido.processar(nome_arquivo, caminho_completo, tempo_atual)
                return

            elif acao in [4, 5]:
                with self.registros_lock:
                    self.evento_renomeado.processar(nome_arquivo, caminho_completo, acao)

                return

            elif acao == 1:
                if nome_arquivo in self.arquivos_recem_adicionados:
                    tempo_limite = 1.0 if ext in arquivos_especiais else 0.1
                    if (tempo_atual - self.arquivos_recem_adicionados[nome_arquivo]) < tempo_limite:
                        return

                self.arquivos_recem_adicionados[nome_arquivo] = tempo_atual
                self.evento_adicionado.processar(nome_arquivo, caminho_completo, tempo_atual)
                return

            elif acao == 3:
                if nome_arquivo in self.arquivos_recem_modificados:
                    tempo_limite = 1.0 if ext in arquivos_especiais else 0.1
                    if (tempo_atual - self.arquivos_recem_modificados[nome_arquivo]) < tempo_limite:
                        return

                if os.path.exists(caminho_completo):
                    self.evento_modificado.processar(nome_arquivo, caminho_completo, tempo_atual)

            self.falhas_consecutivas = 0

        except Exception as e:
            self.falhas_consecutivas += 1
            self.ultimo_erro = str(e)
            logger.error(f"Erro ao processar evento (tentativa {self.falhas_consecutivas}): {e}", exc_info=True)

    def reiniciar_monitoramento(self):
        try:
            self.parar()
            time.sleep(2)
            self.falhas_consecutivas = 0
            self.iniciar()

        except Exception as e:
             logger.error(f"Erro ao reiniciar monitoramento: {e}", exc_info=True)

    def pausar_monitoramento_ou_escaneamento(self):
        self.pausado = not self.pausado
        if self.pausado:
            self._pause_event.clear()

        else:
            self._pause_event.set()

        if self.scan_worker and hasattr(self.scan_worker, "scanner"):
            try:
                self.scan_worker.scanner.pausado = self.pausado
                if self.pausado:
                    self.scan_worker.scanner._pause_event.clear()

                else:
                    self.scan_worker.scanner._pause_event.set()

            except Exception:
                pass

        if hasattr(self, "scanner") and self.scanner:
            try:
                self.scanner.pausado = self.pausado
                if self.pausado:
                    self.scanner._pause_event.clear()

                else:
                    self.scanner._pause_event.set()

            except Exception:
                pass

        try:
            if not hasattr(self, 'interface') or not self.interface:
                return

            scan_running = False
            try:
                scan_running = bool(getattr(self, 'thread_scan', None) and self.thread_scan.isRunning())

            except Exception:
                scan_running = False

            if scan_running and self.scan_worker and hasattr(self.scan_worker, 'scanner'):
                scanner = self.scan_worker.scanner
                progresso = int(getattr(scanner, 'ultimo_progresso', 0))
                contador = int(getattr(scanner, 'contador_processados', 0))
                total = int(getattr(scanner, 'total_arquivos', 0))

                if self.pausado:
                    texto = f"{self.loc.get_text('paused')} {progresso}% ({contador}/{total})"
                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            if not self.interface.barra_progresso.isVisible():
                                self.interface.barra_progresso.show()

                            self.interface.barra_progresso.setValue(progresso)

                        except Exception:
                            pass

                else:
                    texto = f"{self.loc.get_text('scanning')} {progresso}% ({contador}/{total})"
                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            if not self.interface.barra_progresso.isVisible():
                                self.interface.barra_progresso.show()

                            self.interface.barra_progresso.setValue(progresso)

                        except Exception:
                            pass

                try:
                    self.interface.rotulo_resultado.setText(texto)

                except Exception:
                    pass

                QApplication.processEvents()
                return

            if self.pausado:
                try:
                    self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_paused"))

                except Exception:
                    pass

                if hasattr(self.interface, 'barra_progresso'):
                    try:
                        self.interface.barra_progresso.hide()
                        self.interface.barra_progresso.setValue(0)

                    except Exception:
                        pass

            else:
                try:
                    self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_started"))

                except Exception:
                    pass

                if hasattr(self.interface, 'barra_progresso'):
                    try:
                        self.interface.barra_progresso.hide()
                        self.interface.barra_progresso.setValue(0)

                    except Exception:
                        pass

            QApplication.processEvents()
            return

        except Exception as e:
            logger.error(f"Erro ao alternar pausa: {e}", exc_info=True)

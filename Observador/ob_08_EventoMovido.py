import os
import time
import sqlite3
from PySide6.QtCore import QMutexLocker, QTimer, QObject, Signal, QMutex, QThreadPool
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem, QApplication
from concurrent.futures import ThreadPoolExecutor


class EventoRunnable(QObject):
    concluido = Signal(dict)

    def __init__(self, evento, func_processar):
        super().__init__()
        self.evento = evento
        self.func_processar = func_processar

    def run(self):
        resultado = self.func_processar(self.evento)
        if resultado:
            self.concluido.emit(resultado)


class EventoMovido(QObject):
    evento_processado = Signal(dict)
    eventos_em_lote_processados = Signal(list)

    def __init__(self):
        super().__init__()
        self.eventos_pendentes = []
        self.eventos_lock = QMutex()
        self.processamento_timer = QTimer()
        self.processamento_timer.timeout.connect(self.processar_lote)
        self.processamento_timer.start(100)
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)

    def processar_evento(self, evento):
        self.evento_processado.emit(evento)

    def adicionar_evento_para_lote(self, evento):
        with QMutexLocker(self.eventos_lock):
            self.eventos_pendentes.append(evento)

    def processar_lote(self):
        eventos_para_processar = []
        with QMutexLocker(self.eventos_lock):
            if self.eventos_pendentes:
                eventos_para_processar = self.eventos_pendentes.copy()
                self.eventos_pendentes.clear()

        if eventos_para_processar:
            self.eventos_em_lote_processados.emit(eventos_para_processar)

def normalizar_caminho(caminho):
    return os.path.normpath(caminho).replace('/', '\\')

def verificar_movimentacao(interfaceMonitor, evento):
    try:
        if not isinstance(evento, dict) or "tipo_operacao" not in evento or "nome" not in evento:
            return evento

        if "dir_atual" in evento and evento["dir_atual"]:
            evento["dir_atual"] = normalizar_caminho(evento["dir_atual"])

        if "dir_anterior" in evento and evento["dir_anterior"]:
            evento["dir_anterior"] = normalizar_caminho(evento["dir_anterior"])

        with QMutexLocker(interfaceMonitor.mutex):
            if evento["tipo_operacao"] == interfaceMonitor.loc.get_text("op_deleted"):
                evento["exclusao_id"] = str(time.time())
                interfaceMonitor.excluidos_recentemente.setdefault(evento["nome"], []).append((time.time(), evento.get("dir_anterior", ""), evento))
                evento["_temporario"] = True
                return None

            elif evento["tipo_operacao"] == interfaceMonitor.loc.get_text("op_added"):
                if evento["nome"] in interfaceMonitor.excluidos_recentemente:
                    lista_exclusoes = interfaceMonitor.excluidos_recentemente[evento["nome"]]
                    lista_exclusoes.sort(key=lambda x: x[0], reverse=True)

                    for exclusao in lista_exclusoes:
                        excl_time, excl_dir, evento_exclusao = exclusao
                        tempo_limite = 5 if evento["nome"].lower().endswith(('.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mkv', '.mov', '.avi', '.xml', '.exe')) else 0.5
                        if time.time() - excl_time < tempo_limite:
                            if excl_dir != evento["dir_atual"]:
                                lista_exclusoes.remove(exclusao)
                                if not lista_exclusoes:
                                    del interfaceMonitor.excluidos_recentemente[evento["nome"]]

                                exclusao_id = evento_exclusao.get("exclusao_id")
                                with ThreadPoolExecutor(max_workers=1) as executor:
                                    executor.submit(_remover_exclusao, interfaceMonitor, evento["nome"], excl_dir, exclusao_id)

                                evento["tipo_operacao"] = interfaceMonitor.loc.get_text("op_moved")
                                evento["dir_anterior"] = excl_dir
                                return evento

                    if not lista_exclusoes:
                        del interfaceMonitor.excluidos_recentemente[evento["nome"]]

        return evento

    except Exception as e:
        print(f"Erro geral em verificar_movimentacao: {e}")
        import traceback
        traceback.print_exc()
        return evento

def _remover_exclusao(interfaceMonitor, nome, dir_anterior, exclusao_id=None):
    try:
        with sqlite3.connect(interfaceMonitor.evento_base.db_path) as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = WAL')

            cursor = conn.cursor()
            try:
                cursor.execute("BEGIN IMMEDIATE TRANSACTION")

                if exclusao_id:
                    cursor.execute("""
                        SELECT id FROM monitoramento 
                        WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                        ORDER BY id DESC LIMIT 1
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                    resultado = cursor.fetchone()
                    if resultado:
                        registro_id = resultado[0]

                        cursor.execute("""
                            DELETE FROM monitoramento 
                            WHERE id = ?
                        """, (registro_id,))

                        cursor.execute("""
                            DELETE FROM excluido 
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            AND timestamp = (SELECT timestamp FROM monitoramento WHERE id = ?)
                        """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior, registro_id))

                else:
                    cursor.execute("""
                        DELETE FROM monitoramento 
                        WHERE id IN (
                            SELECT id FROM monitoramento
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            ORDER BY id DESC LIMIT 1
                        )
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                    cursor.execute("""
                        DELETE FROM excluido 
                        WHERE id IN (
                            SELECT id FROM excluido
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            ORDER BY id DESC LIMIT 1
                        )
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                cursor.execute("COMMIT")

            except sqlite3.Error as e:
                cursor.execute("ROLLBACK")
                print(f"Erro SQL ao remover exclusão: {e}")
                return False

        QTimer.singleShot(0, lambda: _atualizar_linha_recente(interfaceMonitor))

        return True

    except Exception as e:
        print(f"Erro ao remover registro de exclusão: {e}")
        return False

def _atualizar_linha_recente(interfaceMonitor):
    try:
        if hasattr(interfaceMonitor, 'gerenciador_tabela'):
            interfaceMonitor.gerenciador_tabela.atualizar_linha_mais_recente(interfaceMonitor.tabela_dados)
            interfaceMonitor.atualizar_status()

    except Exception as e:
        print(f"Erro ao atualizar linha recente: {e}")
        _atualizar_tabela_completa(interfaceMonitor)

def _atualizar_tabela_completa(interfaceMonitor):
    try:
        if hasattr(interfaceMonitor, 'gerenciador_tabela'):
            sorting_enabled = interfaceMonitor.tabela_dados.isSortingEnabled()
            interfaceMonitor.tabela_dados.setSortingEnabled(False)
            interfaceMonitor.gerenciador_tabela.atualizar_dados_tabela(interfaceMonitor.tabela_dados)

            interfaceMonitor.atualizar_status()

            interfaceMonitor.tabela_dados.setSortingEnabled(sorting_enabled)
            interfaceMonitor.tabela_dados.viewport().update()

    except Exception as e:
        print(f"Erro ao atualizar tabela completa: {e}")
        import traceback
        traceback.print_exc()

def _inicializar_sistema_evento(interfaceMonitor):
    if not hasattr(interfaceMonitor, 'processador_evento'):
        interfaceMonitor.processador_evento = EventoMovido()

        if not hasattr(interfaceMonitor, 'evento_buffer'):
            interfaceMonitor.evento_buffer = EventoBuffer(interfaceMonitor)

        if not hasattr(interfaceMonitor, 'movimentacao_worker'):
            from Observador.ob_09_MovimentacaoWorker import MovimentacaoWorker
            interfaceMonitor.movimentacao_worker = MovimentacaoWorker(interfaceMonitor)
            interfaceMonitor.movimentacao_worker.processamento_concluido.connect(lambda: interfaceMonitor.gerenciador_tabela.atualizar_linha_mais_recente(interfaceMonitor.tabela_dados))

        interfaceMonitor.processador_evento.evento_processado.connect(lambda evento: interfaceMonitor.evento_buffer.adicionar_evento(evento))
        interfaceMonitor.processador_evento.eventos_em_lote_processados.connect(lambda eventos: interfaceMonitor.evento_buffer.adicionar_eventos_lote(eventos))

    if not hasattr(interfaceMonitor, 'contador_eventos'):
        interfaceMonitor.contador_eventos = 0

    if not hasattr(interfaceMonitor, 'refresh_timer'):
        interfaceMonitor.refresh_timer = QTimer()
        interfaceMonitor.refresh_timer.timeout.connect(lambda: interfaceMonitor.atualizar_status())
        interfaceMonitor.refresh_timer.start(1000)

    if not hasattr(interfaceMonitor, 'exclusao_timer'):
        interfaceMonitor.exclusao_timer = QTimer()
        interfaceMonitor.exclusao_timer.timeout.connect(lambda: _processar_exclusoes_pendentes(interfaceMonitor))
        interfaceMonitor.exclusao_timer.start(1000)

def _processar_exclusoes_pendentes(interfaceMonitor):
    try:
        eventos_para_processar = []
        tempo_atual = time.time()

        with QMutexLocker(interfaceMonitor.mutex):
            nomes_para_remover = []
            for nome, eventos_lista in interfaceMonitor.excluidos_recentemente.items():
                eventos_a_remover = []
                for registro in eventos_lista:
                    timestamp, dir_anterior, evento = registro
                    tempo_limite = 5 if nome.lower().endswith(('.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mkv', '.mov', '.avi', '.xml', '.exe')) else 0.5
                    if tempo_atual - timestamp > tempo_limite:
                        novo_evento = evento.copy()
                        novo_evento.pop("_temporario", None)
                        novo_evento["id_exclusao_unico"] = f"{nome}_{timestamp}_{id(registro)}"
                        eventos_para_processar.append(novo_evento)
                        eventos_a_remover.append(registro)

                for registro in eventos_a_remover:
                    eventos_lista.remove(registro)

                if not eventos_lista:
                    nomes_para_remover.append(nome)

            for nome in nomes_para_remover:
                del interfaceMonitor.excluidos_recentemente[nome]

        if len(eventos_para_processar) > 1:
            QTimer.singleShot(0, lambda: interfaceMonitor.processador_evento.eventos_em_lote_processados.emit(eventos_para_processar))

        elif eventos_para_processar:
            for evento in eventos_para_processar:
                QTimer.singleShot(0, lambda e=evento: interfaceMonitor.processador_evento.evento_processado.emit(e))

    except Exception as e:
        print(f"Erro ao processar exclusões pendentes: {e}")
        import traceback
        traceback.print_exc()

def _adicionar_item_tabela(interfaceMonitor, evento, atualizar_interface=True):
    try:
        tipo_operacao_traduzido = interfaceMonitor.loc.get_text(evento["tipo_operacao"])
        if not interfaceMonitor.painel_filtros.verificar_filtro_operacao(tipo_operacao_traduzido):
            return

        row_position = 0
        interfaceMonitor.tabela_dados.insertRow(row_position)

        colunas_visiveis = [(key, col) for key, col in sorted(interfaceMonitor.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]) if col["visivel"]]

        cores = {
            interfaceMonitor.loc.get_text("op_renamed"): QColor(0, 255, 0),
            interfaceMonitor.loc.get_text("op_added"): QColor(0, 0, 255),
            interfaceMonitor.loc.get_text("op_deleted"): QColor(255, 0, 0),
            interfaceMonitor.loc.get_text("op_modified"): QColor(255, 98, 0),
            interfaceMonitor.loc.get_text("op_moved"): QColor(255, 0, 255),
            interfaceMonitor.loc.get_text("op_scanned"): QColor(128, 128, 128)
        }

        for col, (key, coluna) in enumerate(colunas_visiveis):
            try:
                valor = coluna["getter"](evento) if callable(coluna.get("getter")) else evento.get(key, "")

                if key == "tipo_operacao":
                    valor = interfaceMonitor.loc.get_text(valor)

                if key in ["dir_anterior", "dir_atual"] and valor:
                    valor = "" if not valor or valor == "." else normalizar_caminho(str(valor))

                valor_texto = str(valor)
                novo_item = QTableWidgetItem(valor_texto)

                if key == "tipo_operacao":
                    novo_item.setBackground(cores.get(valor, QColor(255, 255, 255)))

                interfaceMonitor.tabela_dados.setItem(row_position, col, novo_item)

            except Exception as e:
                print(f"Erro ao adicionar item na coluna {key}: {e}")
                interfaceMonitor.tabela_dados.setItem(row_position, col, QTableWidgetItem(""))

        if atualizar_interface:
            interfaceMonitor.atualizar_status()

    except Exception as e:
        print(f"Erro ao adicionar item na tabela: {e}")
        import traceback
        traceback.print_exc()

def adicionar_evento(interfaceMonitor, evento):
    try:
        if not evento or "tipo_operacao" not in evento or "nome" not in evento:
            print("Evento inválido recebido:", evento)
            return

        _inicializar_sistema_evento(interfaceMonitor)

        evento_processado = verificar_movimentacao(interfaceMonitor, evento)

        if evento_processado is not None:
            interfaceMonitor.processador_evento.evento_processado.emit(evento_processado)

    except Exception as e:
        print(f"Erro em adicionar_evento: {e}")
        import traceback
        traceback.print_exc()


class EventoBuffer:
    def __init__(self, interface_monitor):
        self.interface = interface_monitor
        self.lock = QMutex()
        self.ultimo_update = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(250)
        self.eventos_pendentes = []

    def adicionar_evento(self, evento):
        with QMutexLocker(self.lock):
            self._processar_evento_imediato(evento)

    def adicionar_eventos_lote(self, eventos):
        if not eventos:
            return

        with QMutexLocker(self.lock):
            self.interface.tabela_dados.blockSignals(True)
            ordenacao_habilitada = self.interface.tabela_dados.isSortingEnabled()
            self.interface.tabela_dados.setSortingEnabled(False)

            try:
                for evento in eventos:
                    self._processar_evento_imediato(evento)

                eventos_movidos = [e for e in eventos if e.get("tipo_operacao") == self.interface.loc.get_text("op_moved")]
                if eventos_movidos and hasattr(self.interface, 'movimentacao_worker'):
                    for evento in eventos_movidos:
                        self.interface.movimentacao_worker.adicionar_evento(evento)

            finally:
                self.interface.tabela_dados.setSortingEnabled(ordenacao_habilitada)
                self.interface.tabela_dados.blockSignals(False)
                self.interface.tabela_dados.viewport().update()
                QApplication.processEvents()

    def _adicionar_evento_lote(self, evento):
        try:
            tipo_operacao_traduzido = self.interface.loc.get_text(evento["tipo_operacao"])
            if not self.interface.painel_filtros.verificar_filtro_operacao(tipo_operacao_traduzido):
                return

            self.interface.tabela_dados.setUpdatesEnabled(False)
            _adicionar_item_tabela(self.interface, evento, atualizar_interface=False)
            self.interface.tabela_dados.setUpdatesEnabled(True)

        except Exception as e:
            print(f"Erro ao adicionar evento em lote: {e}")

    def _processar_evento_imediato(self, evento):
        ordenacao_habilitada = self.interface.tabela_dados.isSortingEnabled()
        self.interface.tabela_dados.setSortingEnabled(False)

        try:
            _adicionar_item_tabela(self.interface, evento, atualizar_interface=False)

            if evento.get("tipo_operacao") == self.interface.loc.get_text("op_moved") and hasattr(self.interface, 'movimentacao_worker'):
                self.interface.movimentacao_worker.adicionar_evento(evento)

        finally:
            self.interface.tabela_dados.setSortingEnabled(ordenacao_habilitada)
            self.interface.tabela_dados.viewport().update()
            QApplication.processEvents()

    def atualizar_interface(self):
        self.interface.atualizar_status()

        if hasattr(self.interface, 'gerenciador_tabela'):
            self.interface.gerenciador_tabela.atualizacao_pendente = True

        self.interface.tabela_dados.viewport().update()

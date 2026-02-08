import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal, QMetaObject, Qt
from source.Observador.GerenciamentoDiretorioScanner.gscanner_01_process_batch import _process_batch
from source.Observador.GerenciamentoDiretorioScanner.gscanner_02_scan_directory import scan_directory
from source.Observador.GerenciamentoDiretorioScanner.gscanner_03_processar_fila import _processar_fila
from source.Observador.GerenciamentoDiretorioScanner.gscanner_04_get_file_type import get_file_type
from source.Observador.GerenciamentoDiretorioScanner.gscanner_05_processar_item import _processar_item
from source.Observador.GerenciamentoDiretorioScanner.gscanner_06_atualizar_progresso import _atualizar_progresso
from source.Observador.GerenciamentoDiretorioScanner.gscanner_07_atualizar_interface import _atualizar_interface
from source.Observador.GerenciamentoDiretorioScanner.gscanner_08_finalizar_scan import _finalizar_scan
from source.Observador.GerenciamentoDiretorioScanner.gscanner_09_scan_worker_run import run as scan_worker_run
from utils.LogManager import LogManager
logger = LogManager.get_logger()

class DiretorioScanner(QObject):
    progresso_atualizado = Signal(int, int, int)
    scan_finalizado = Signal()

    def __init__(self, observador):
        super().__init__()
        try:
            self.observador = observador
            self.db_path = observador.evento_base.db_path
            self.gerenciador_colunas = observador.gerenciador_colunas
            self.fila_processamento = queue.Queue()
            self.contador_processados = 0
            self.total_arquivos = 0
            self.executor = ThreadPoolExecutor(max_workers=4)
            self.lock_db = threading.Lock()
            self.ultimo_progresso = 0
            self.intervalo_atualizacao = 1
            self.pausado = False
            self._pause_event = threading.Event()
            self._pause_event.set()
            if hasattr(self.observador, 'interface'):
                QMetaObject.invokeMethod(self.observador.interface, "criar_barra_progresso",
                                        Qt.ConnectionType.QueuedConnection)

                self.progresso_atualizado.connect(self._atualizar_interface)
                self.scan_finalizado.connect(self._finalizar_scan)

        except Exception as e:
            logger.error(f"Erro ao inicializar DiretorioScanner: {e}", exc_info=True)

    def pausar(self):
        try:
            if not self.pausado:
                self.pausado = True
                self._pause_event.clear()

            else:
                self.pausado = False
                self._pause_event.set()

            if hasattr(self.observador, "interface") and hasattr(self.observador.interface, "rotulo_resultado"):
                status = self.observador.loc.get_text("paused") if self.pausado else self.observador.loc.get_text("resumed")
                self.observador.interface.rotulo_resultado.setText(status)

        except Exception as e:
            logger.error(f"Erro ao pausar/resumir o scan: {e}", exc_info=True)

    _process_batch = _process_batch
    scan_directory = scan_directory
    _processar_fila = _processar_fila
    get_file_type = get_file_type
    _processar_item = _processar_item
    _atualizar_progresso = _atualizar_progresso
    _atualizar_interface = _atualizar_interface
    _finalizar_scan = _finalizar_scan


class ScanWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, scanner, directory):
        super().__init__()
        try:
            self.scanner = scanner
            self.directory = directory

        except Exception as e:
            logger.error(f"Erro ao inicializar ScanWorker: {e}", exc_info=True)

    run = scan_worker_run

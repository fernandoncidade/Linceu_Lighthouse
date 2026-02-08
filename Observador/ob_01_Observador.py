import time
import win32con
import threading
from collections import deque
from .ob_02_BaseEvento import BaseEvento
from .ob_04_EventoAdicionado import EventoAdicionado
from .ob_05_EventoExcluido import EventoExcluido
from .ob_06_EventoModificado import EventoModificado
from .ob_07_EventoRenomeado import EventoRenomeado
from .ob_09_GerenciadorColunas import GerenciadorColunas
from Observador.GerenciamentoObservador.gob_01_DetectarOperacaoMassiva import detectar_operacao_massiva
from Observador.GerenciamentoObservador.gob_02_Iniciar import iniciar
from Observador.GerenciamentoObservador.gob_03_HandleScanError import handle_scan_error
from Observador.GerenciamentoObservador.gob_04_IniciarMonitoramento import iniciar_monitoramento
from Observador.GerenciamentoObservador.gob_05_ProcessarBufferEventos import processar_buffer_eventos
from Observador.GerenciamentoObservador.gob_06_PararScan import parar_scan
from Observador.GerenciamentoObservador.gob_07_Parar import parar
from Observador.GerenciamentoObservador.gob_08_LimparEstado import limpar_estado
from Observador.GerenciamentoObservador.gob_09_Monitorar import monitorar
from Observador.GerenciamentoObservador.gob_10_ProcessarEventoInterno import _processar_evento_interno
from Observador.GerenciamentoObservador.gob_11_ProcessarEvento import processar_evento
from Observador.GerenciamentoObservador.gob_12_ReiniciarMonitoramento import reiniciar_monitoramento
from Observador.GerenciamentoObservador.gob_13_PausarMonitoramentoEscaneamento import pausar_monitoramento_ou_escaneamento
from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

if not hasattr(win32con, 'FILE_NOTIFY_CHANGE_CREATION'):
    win32con.FILE_NOTIFY_CHANGE_CREATION = 0x00000040


class Observador:
    def __init__(self, diretorio, callback):
        try:
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

        except Exception as e:
            logger.error(f"Erro ao inicializar Observador: {e}", exc_info=True)

    detectar_operacao_massiva = detectar_operacao_massiva
    iniciar = iniciar
    handle_scan_error = handle_scan_error
    iniciar_monitoramento = iniciar_monitoramento
    processar_buffer_eventos = processar_buffer_eventos
    parar_scan = parar_scan
    parar = parar
    limpar_estado = limpar_estado
    monitorar = monitorar
    _processar_evento_interno = _processar_evento_interno
    processar_evento = processar_evento
    reiniciar_monitoramento = reiniciar_monitoramento
    pausar_monitoramento_ou_escaneamento = pausar_monitoramento_ou_escaneamento

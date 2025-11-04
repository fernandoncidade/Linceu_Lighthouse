from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _inicializar_tradutor_metadados(self):
    try:
        from GerenciamentoUI.ui_13_TradutorMetadadosQt import TradutorMetadadosQt
        self.tradutor_metadados = TradutorMetadadosQt(self)

    except ImportError as e:
        logger.error(f"Erro ao importar TradutorMetadadosQt: {e}")
        self.tradutor_metadados = None

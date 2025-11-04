import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _limpar_dados_monitorados(self):
    try:
        if hasattr(self.interface, 'observador') and self.interface.observador and self.interface.observador.ativo:
            self.interface.gerenciador_botoes.alternar_analise_diretorio()

        if hasattr(self.interface, 'evento_base'):
            self.interface.evento_base.limpar_registros()

        db_paths = [
            "monitoramento.db", 
            os.path.join(os.path.dirname(__file__), "..", "Observador", "monitoramento.db"), 
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Observador", "monitoramento.db")
        ]
        db_removido = False
        for db_path in db_paths:
            if os.path.exists(db_path):
                os.remove(db_path)
                db_removido = True

        if not db_removido:
            logger.warning("Arquivo de banco de dados não encontrado para remoção.")

        self._limpar_dados_interface()

    except Exception as e:
        logger.error(f"Erro ao limpar dados monitorados: {e}", exc_info=True)

from source.GerenciamentoUI.GerenciamentoEstatisticasUI.geui_30_botao_rotacionado import BotaoRotacionado
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_botao_toggle_painel(self, texto):
    try:
        rotated_btn = BotaoRotacionado(texto)
        rotated_btn.clicked.connect(self._toggle_painel_selecao)
        return rotated_btn

    except Exception as e:
        logger.error(f"Erro ao criar botão de toggle do painel: {e}", exc_info=True)


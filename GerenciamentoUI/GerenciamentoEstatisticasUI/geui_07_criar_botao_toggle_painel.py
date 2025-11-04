from GerenciamentoUI.GerenciamentoEstatisticasUI.geui_30_botao_rotacionado import BotaoRotacionado

def _criar_botao_toggle_painel(self, texto):
    rotated_btn = BotaoRotacionado(texto)
    rotated_btn.clicked.connect(self._toggle_painel_selecao)
    return rotated_btn

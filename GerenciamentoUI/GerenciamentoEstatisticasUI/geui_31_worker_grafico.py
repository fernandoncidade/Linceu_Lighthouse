from PySide6.QtCore import QThread, Signal
import pandas as pd
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class GraficoWorker(QThread):
    dados_grafico_prontos = Signal(str, object, object, str)
    todos_concluidos = Signal()
    progresso_atualizado = Signal(int, int)
    erro_ocorrido = Signal(str, str)

    def __init__(self, graficos):
        super().__init__()
        self.graficos = graficos
        self.parar_flag = False

    def run(self):
        total_graficos = len(self.graficos)
        for i, grafico in enumerate(self.graficos):
            if self.parar_flag:
                break

            try:
                logger.debug(f"Thread: Preparando dados para o gráfico: {grafico['titulo']}")
                self.progresso_atualizado.emit(i + 1, total_graficos)

                dados = self._preparar_dados_grafico(grafico["func"])

                self.dados_grafico_prontos.emit(
                    grafico["titulo"], 
                    dados,
                    grafico["func"],
                    grafico["titulo"]
                )

            except Exception as e:
                logger.error(f"Thread: Erro ao preparar dados para o gráfico {grafico['titulo']}: {e}", exc_info=True)
                self.erro_ocorrido.emit(grafico["titulo"], str(e))

        self.todos_concluidos.emit()

    def _preparar_dados_grafico(self, func_gerador):
        if hasattr(func_gerador.__self__, '_obter_dados'):
            dados = func_gerador.__self__._obter_dados()
            return dados

        return None

    def parar(self):
        self.parar_flag = True

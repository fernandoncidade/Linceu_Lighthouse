from PySide6.QtCore import QThread, Signal
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoWorker(QThread):
    dados_grafico_prontos = Signal(str, object, object, str)
    todos_concluidos = Signal()
    progresso_atualizado = Signal(int, int)
    erro_ocorrido = Signal(str, str)

    def __init__(self, graficos):
        try:
            super().__init__()
            self.graficos = graficos
            self.parar_flag = False

        except Exception as e:
            logger.error(f"Erro ao inicializar GraficoWorker: {e}", exc_info=True)

    def run(self):
        try:
            total_graficos = len(self.graficos)
            for i, grafico in enumerate(self.graficos):
                if self.parar_flag:
                    break

                try:
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

        except Exception as e:
            logger.error(f"Erro na execução da thread GraficoWorker: {e}", exc_info=True)

    def _preparar_dados_grafico(self, func_gerador):
        try:
            if hasattr(func_gerador.__self__, '_obter_dados'):
                dados = func_gerador.__self__._obter_dados()
                return dados

            return None

        except Exception as e:
            logger.error(f"Erro ao preparar dados do gráfico: {e}", exc_info=True)
            return None

    def parar(self):
        try:
            self.parar_flag = True

        except Exception as e:
            logger.error(f"Erro ao parar GraficoWorker: {e}", exc_info=True)

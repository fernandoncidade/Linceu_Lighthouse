import warnings
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def desconectar_sinais(self):
    try:
        import shiboken6

        conexoes_validas = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            for sinal, conexao in self.conexoes_sinais:
                try:
                    if hasattr(sinal, 'disconnect'):
                        try:
                            sinal.disconnect(conexao)

                        except RuntimeError:
                            logger.error("Sinal já desconectado ou inválido", exc_info=True)

                        except TypeError:
                            logger.error("Tipo inválido durante desconexão", exc_info=True)

                except Exception as e:
                    logger.error(f"Erro ao verificar/desconectar sinal: {e}", exc_info=True)

        self.conexoes_sinais = []
        self.parent = None

    except Exception as e:
        logger.error(f"Erro ao desconectar sinais: {e}", exc_info=True)

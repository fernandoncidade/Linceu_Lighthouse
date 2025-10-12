from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GerenciadorMensagens:
    @staticmethod
    def atualizar_rotulos(interface):
        try:
            if interface.diretorio_atual:
                interface.rotulo_diretorio.setText(interface.loc.get_text("dir_selected").format(interface.diretorio_atual))

            else:
                interface.rotulo_diretorio.setText(interface.loc.get_text("no_dir"))

            if interface.observador and interface.observador.ativo:
                interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_started"))

            elif interface.observador and not interface.observador.ativo:
                interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_stopped"))

            else:
                interface.rotulo_resultado.setText(interface.loc.get_text("select_to_start"))

            interface.atualizar_status()

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos: {e}", exc_info=True)

    @staticmethod
    def notificar_erro(interface, mensagem):
        try:
            logger.error(f"Notificando erro: {mensagem}")
            interface.rotulo_resultado.setText(f"Erro: {mensagem}")

        except Exception as e:
            logger.error(f"Erro ao notificar erro: {e}", exc_info=True)

    @staticmethod
    def notificar_sucesso(interface, mensagem):
        try:
            logger.info(f"Notificando sucesso: {mensagem}")
            interface.rotulo_resultado.setText(mensagem)

        except Exception as e:
            logger.error(f"Erro ao notificar sucesso: {e}", exc_info=True)

from utils.LogManager import LogManager
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt


class Atualizador:
    @staticmethod
    def atualizar_interface(interface):
        logger = LogManager.get_logger()
        try:
            logger.debug("Atualizando interface")
            if hasattr(interface, 'tabela_dados'):
                interface.tabela_dados.blockSignals(True)

            if hasattr(interface, 'painel_filtros'):
                interface.painel_filtros.blockSignals(True)

            interface.setWindowTitle(interface.loc.get_text("window_title"))
            if hasattr(interface, 'rotulo_diretorio'):
                if interface.diretorio_atual:
                    interface.rotulo_diretorio.setText(interface.loc.get_text("dir_selected").format(interface.diretorio_atual))

                else:
                    interface.rotulo_diretorio.setText(interface.loc.get_text("no_dir"))

            if hasattr(interface, 'rotulo_resultado'):
                if interface.observador and interface.observador.ativo:
                    interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_started"))

                elif interface.observador and not interface.observador.ativo:
                    interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_stopped"))

                else:
                    interface.rotulo_resultado.setText(interface.loc.get_text("select_to_start"))

            if hasattr(interface, 'gerenciador_menus_ui'):
                interface.gerenciador_menus_ui.criar_menu_principal()

            if hasattr(interface, 'gerenciador_botoes_ui'):
                interface.gerenciador_botoes_ui.update_buttons_text(interface.loc)

            if hasattr(interface, 'painel_filtros'):
                interface.painel_filtros.atualizar_interface()

            if hasattr(interface, 'gerenciador_tabela'):
                interface.gerenciador_tabela.configurar_tabela(interface.tabela_dados)
                if hasattr(interface.gerenciador_tabela, 'aplicar_cores_todas_colunas_processamento'):
                    dados_processamento = {'reprocessar': True}
                    interface.gerenciador_tabela.aplicar_cores_todas_colunas_processamento(dados_processamento)

            if hasattr(interface, 'tabela_dados'):
                interface.tabela_dados.blockSignals(False)
                interface.tabela_dados.viewport().update()

            if hasattr(interface, 'painel_filtros'):
                interface.painel_filtros.blockSignals(False)

            interface.atualizar_status()
            interface.update()
            QApplication.processEvents()
            logger.debug("Interface atualizada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao atualizar interface: {e}", exc_info=True)

    @staticmethod
    def atualizar_status(interface, *args):
        logger = LogManager.get_logger()
        try:
            logger.debug("Atualizando status")

            if hasattr(interface, "label_contagem") and hasattr(interface, "painel_filtros"):
                interface.label_contagem.setText(interface.painel_filtros.atualizar_contagem())
                logger.debug("Status atualizado com sucesso")

            if hasattr(interface, 'rotulo_contador_eventos') and hasattr(interface, 'painel_filtros'):
                texto_contador = interface.painel_filtros.administrador_filtros.atualizar_contagem_eventos_monitorados()
                interface.rotulo_contador_eventos.setText(texto_contador)
                logger.debug("Contador de eventos atualizado com sucesso")

        except Exception as e:
            logger.error(f"Erro ao atualizar status: {e}", exc_info=True)

    @staticmethod
    def abrir_janela_filtros(interface):
        try:
            from Filtros.fil_01_Filtros import Filtros
            from utils.LogManager import LogManager
            logger = LogManager.get_logger()
            logger.info("Abrindo janela de filtros avançados")
            if hasattr(interface, 'painel_filtros') and interface.painel_filtros:
                if interface.painel_filtros.isVisible():
                    interface.painel_filtros.raise_()
                    interface.painel_filtros.activateWindow()
                    return

                interface.painel_filtros.deleteLater()
                interface.painel_filtros = None

            interface.painel_filtros = Filtros(interface.tabela_dados, interface.loc)
            interface.painel_filtros.setWindowModality(Qt.NonModal)
            interface.painel_filtros.show()
            interface.painel_filtros.filtroAplicado.connect(interface.atualizar_status)
            logger.info("Janela de filtros avançados exibida com sucesso")

        except Exception as e:
            logger = LogManager.get_logger()
            logger.error(f"Erro ao abrir janela de filtros: {e}", exc_info=True)

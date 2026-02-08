import os
from PySide6.QtWidgets import QWidget
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def alternar_estrutura_diretorios(interface, checked=None, ajustar_tamanho=True):
    try:
        from ..ic_10_EstruturaDiretoriosWidget import EstruturaDiretoriosWidget
        from .gedw_16_obter_status_diretorios import obter_status_diretorios

    except Exception:
        EstruturaDiretoriosWidget = None
        obter_status_diretorios = None

    try:
        if checked is None:
            checked = not getattr(interface, "estrutura_ativa", False)

        if checked and getattr(interface, "desempenho_ativo", False):
            try:
                if hasattr(interface, "alternar_graficos_desempenho"):
                    interface.alternar_graficos_desempenho(False, ajustar_tamanho=False)

            except Exception as e:
                logger.warning(f"Falha ao desativar gráficos ao ativar estrutura: {e}", exc_info=True)

            try:
                if (hasattr(interface, "gerenciador_menus_ui") and
                    hasattr(interface.gerenciador_menus_ui, "acao_toggle_desempenho")):
                    interface.gerenciador_menus_ui.acao_toggle_desempenho.setChecked(False)

            except Exception:
                pass

        if checked and not getattr(interface, "estrutura_ativa", False):
            try:
                if EstruturaDiretoriosWidget and obter_status_diretorios:
                    root_path = getattr(interface, "diretorio_atual", "") or os.getcwd()
                    status_map = obter_status_diretorios(root_path)
                    interface.estrutura_widget = EstruturaDiretoriosWidget(root_path, status_map)
                    novo = interface.estrutura_widget

                    try:
                        def _on_select_dir(path, iface=interface):
                            try:
                                iface.diretorio_atual = path
                                logger.info(f"Diretório monitorado alterado para: {path}")

                                try:
                                    if hasattr(iface, 'rotulo_diretorio') and iface.rotulo_diretorio:
                                        iface.rotulo_diretorio.setText(path)

                                except Exception as e:
                                    logger.debug(f"Falha ao atualizar rotulo_diretorio: {e}", exc_info=True)

                                try:
                                    if hasattr(iface, 'atualizar_status'):
                                        iface.atualizar_status()

                                except Exception as e:
                                    logger.error(f"Erro ao atualizar status após seleção de diretório: {e}", exc_info=True)

                                try:
                                    gm = getattr(iface, 'gerenciador_monitoramento', None)
                                    if gm:
                                        if hasattr(gm, 'definir_diretorio'):
                                            gm.definir_diretorio(path)

                                        elif hasattr(iface, 'reiniciar_sistema_monitoramento'):
                                            iface.reiniciar_sistema_monitoramento()

                                except Exception as e:
                                    logger.warning(f"Não foi possível notificar gerenciador_monitoramento: {e}", exc_info=True)

                            except Exception as e:
                                logger.error(f"Erro ao aplicar diretório selecionado pela árvore: {e}", exc_info=True)

                        if hasattr(novo, 'selecionar_diretorio_solicitado'):
                            novo.selecionar_diretorio_solicitado.connect(_on_select_dir)

                    except Exception:
                        pass

                else:
                    novo = QWidget()

            except Exception:
                novo = QWidget()

            if hasattr(interface, "splitter_lateral"):
                antigo = interface.splitter_lateral.widget(0)
                if antigo:
                    antigo.setParent(None)

                interface.splitter_lateral.insertWidget(0, novo)

            interface.widget_desempenho = novo
            interface.estrutura_ativa = True

        elif not checked and getattr(interface, "estrutura_ativa", False):
            interface.estrutura_widget = None
            placeholder = QWidget()
            if hasattr(interface, "splitter_lateral"):
                antigo = interface.splitter_lateral.widget(0)
                if antigo:
                    antigo.setParent(None)

                interface.splitter_lateral.insertWidget(0, placeholder)

            interface.widget_desempenho = placeholder
            interface.estrutura_ativa = False

        if (hasattr(interface, "gerenciador_menus_ui") and hasattr(interface.gerenciador_menus_ui, "acao_toggle_estrutura")):
            interface.gerenciador_menus_ui.acao_toggle_estrutura.setChecked(interface.estrutura_ativa)

        try:
            if ajustar_tamanho and not interface.isMaximized() and not interface.isFullScreen():
                if interface.estrutura_ativa:
                    interface.setGeometry(100, 100, 1300, 800)

                else:
                    interface.setGeometry(100, 100, 900, 500)

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao alternar visualização de estrutura: {e}", exc_info=True)

    return getattr(interface, "estrutura_ativa", False)

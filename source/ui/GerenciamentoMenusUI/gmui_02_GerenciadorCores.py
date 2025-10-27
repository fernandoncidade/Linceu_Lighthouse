import os
import json
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import QThread, Signal
from source.utils.IconUtils import get_icon_path, get_app_base_path
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_palette_icon_path(tipo="paleta"):
    try:
        if tipo == "paleta":
            icon_name = "blocos-de-cores.ico"

        else:
            icon_name = "paleta-de-cores.ico"

        return get_icon_path(icon_name)

    except Exception as e:
        logger.error(f"Erro ao obter caminho do ícone da paleta: {e}", exc_info=True)
        return ""


class GerenciadorCores:
    def __init__(self, interface_principal):
        try:
            self.interface = interface_principal
            self.loc = interface_principal.loc
            self.thread_cores = None

            self.cores_operacoes = {
                "op_renamed": "#00ff00",
                "op_added": "#0000ff",
                "op_deleted": "#ff0000",
                "op_modified": "#ff6200",
                "op_moved": "#ff00ff",
                "op_scanned": "#808080"
            }
            self.carregar_cores()

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorCores: {e}", exc_info=True)

    def carregar_cores(self):
        try:
            config_dir = obter_caminho_persistente()
            cores_path = os.path.join(config_dir, "cores_config.json")
            if os.path.exists(cores_path):
                with open(cores_path, 'r', encoding='utf-8') as f:
                    cores_salvas = json.load(f)

                for tipo, cor in cores_salvas.get('cores_operacoes', {}).items():
                    if tipo in self.cores_operacoes:
                        self.cores_operacoes[tipo] = cor

            else:
                pass

        except Exception as e:
            logger.error(f"Erro ao carregar configurações de cores: {e}", exc_info=True)

    def salvar_cores(self):
        try:
            config_dir = obter_caminho_persistente()
            cores_path = os.path.join(config_dir, "cores_config.json")
            os.makedirs(config_dir, exist_ok=True)
            cores_config = {'cores_operacoes': self.cores_operacoes}
            with open(cores_path, 'w', encoding='utf-8') as f:
                json.dump(cores_config, f, indent=4)

            return True

        except Exception as e:
            logger.error(f"Erro ao salvar configurações de cores: {e}", exc_info=True)
            return False

    def _obter_diretorio_config(self):
        try:
            base_path = get_app_base_path()
            config_dir = os.path.join(base_path, "config")
            return config_dir

        except Exception as e:
            logger.error(f"Erro ao obter diretório de configuração: {e}", exc_info=True)
            return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config"))

    def obter_cor_qcolor(self, tipo_operacao):
        try:
            cor_hex = self.cores_operacoes.get(tipo_operacao, "#333333")
            return QColor(cor_hex)

        except Exception as e:
            logger.error(f"Erro ao obter QColor para operação {tipo_operacao}: {e}", exc_info=True)
            return QColor("#333333")

    def obter_cor_hex(self, tipo_operacao):
        try:
            return self.cores_operacoes.get(tipo_operacao, "#333333")

        except Exception as e:
            logger.error(f"Erro ao obter cor hex para operação {tipo_operacao}: {e}", exc_info=True)
            return "#333333"

    def definir_cor(self, tipo_operacao, cor_hex):
        try:
            if tipo_operacao in self.cores_operacoes:
                self.cores_operacoes[tipo_operacao] = cor_hex
                return True

            return False

        except Exception as e:
            logger.error(f"Erro ao definir cor para operação {tipo_operacao}: {e}", exc_info=True)
            return False

    def atualizar_cores_no_sistema(self):
        try:
            from ui.GerenciamentoMenusUI.gmui_02_GerenciadorCores import ThreadAtualizarCores
            if self.thread_cores is not None and self.thread_cores.isRunning():
                self.thread_cores.quit()
                self.thread_cores.wait()

            self.thread_cores = ThreadAtualizarCores(self, self.interface)
            self.thread_cores.sinal_concluido.connect(self.interface.update)
            self.thread_cores.start()

        except Exception as e:
            logger.error(f"Erro ao atualizar cores no sistema: {e}", exc_info=True)

    def _atualizar_cores_no_sistema_threadsafe(self):
        try:
            if hasattr(self.interface, 'gerenciador_tabela') and hasattr(self.interface, 'tabela_dados') and self.interface.tabela_dados is not None:
                self.interface.gerenciador_tabela.atualizacao_pendente = True
                self.interface.gerenciador_tabela.atualizar_dados_tabela(self.interface.tabela_dados)

            if hasattr(self.interface, 'gerenciador_estatisticas_ui') and hasattr(self.interface.gerenciador_estatisticas_ui, 'gerador_atual'):
                if self.interface.gerenciador_estatisticas_ui.gerador_atual:
                    self.interface.gerenciador_estatisticas_ui.gerador_atual.atualizar_textos_traduzidos()

        except Exception as e:
            logger.error(f"Erro ao atualizar cores no sistema (threadsafe): {e}", exc_info=True)

    @staticmethod
    def aplicar_icone_paleta(dialog, tipo="paleta"):
        try:
            icon_file = get_palette_icon_path(tipo)
            dialog.setWindowIcon(QIcon(icon_file))

        except Exception as e:
            logger.error(f"Erro ao aplicar ícone da paleta: {e}", exc_info=True)


class ThreadAtualizarCores(QThread):
    sinal_concluido = Signal()

    def __init__(self, gerenciador_cores, interface):
        super().__init__()
        self.gerenciador_cores = gerenciador_cores
        self.interface = interface

    def run(self):
        try:
            self.gerenciador_cores._atualizar_cores_no_sistema_threadsafe()

        except Exception as e:
            logger.error(f"Erro na thread de atualização de cores: {e}", exc_info=True)

        finally:
            self.sinal_concluido.emit()

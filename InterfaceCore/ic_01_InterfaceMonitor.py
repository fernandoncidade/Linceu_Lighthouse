from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()
log_file = LogManager.get_log_file()
from .ic_02_Inicializador import Inicializador
import matplotlib
matplotlib.use('QtAgg')
from GerenciamentoUI.ui_07_GerenciadorDados import GerenciadorDados
from GerenciamentoUI.ui_08_GerenciadorEventosArquivo import GerenciadorEventosArquivo
from GerenciamentoUI.ui_09_GerenciadorMonitoramento import GerenciadorMonitoramento
from GerenciamentoUI.ui_10_GerenciadorLimpeza import GerenciadorLimpeza
from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from Observador.ob_11_GerenciadorTabela import GerenciadorTabela
from .ic_03_Configurador import Configurador
from .ic_04_Atualizador import Atualizador
from .ic_05_GerenciadorProgresso import GerenciadorProgresso
from .ic_07_ManipuladorTabela import ManipuladorTabela
from .ic_08_Internacionalizador import Internacionalizador


class InterfaceMonitor(QMainWindow):
    def __init__(self):
        try:
            logger.info("Iniciando a aplicação Linceu_Lighthouse")
            super().__init__()
            logger.debug("Inicializando sistema de tradução nativo do Qt")
            app = QApplication.instance()
            Internacionalizador.inicializar_sistema_traducao(app)
            logger.debug("Inicializando o LocalizadorQt")

            self.loc = LocalizadorQt()
            self.loc.idioma_alterado.connect(self.atualizar_interface)
            self.loc.traducoes_carregadas.connect(self.atualizar_tradutor_qt)

            Inicializador.inicializar_atributos(self)
            Inicializador.inicializar_componentes(self)
            logger.debug("Inicializando GerenciadorTabela")

            self.gerenciador_tabela = GerenciadorTabela(self)
            self.gerenciador_tabela._carregar_configuracoes_cores()
            self.gerenciador_tabela.cores_processadas.connect(self._atualizar_cores_tabela)
            Inicializador.inicializar_gerenciadores(self)
            logger.debug("Configurando interface principal")

            self.configurar_tabela()
            self.setup_ui()
            self.setup_menu_bar()
            if hasattr(self, 'painel_filtros'):
                self.painel_filtros.sincronizar_com_menu_principal()

            self.gerenciador_eventos_arquivo = GerenciadorEventosArquivo(self)
            self.gerenciador_dados = GerenciadorDados(self)
            self.gerenciador_monitoramento = GerenciadorMonitoramento(self)
            self.gerenciador_limpeza = GerenciadorLimpeza(self)
            logger.info("Inicialização da aplicação concluída com sucesso")

        except Exception as e:
            logger.critical(f"Erro fatal na inicialização: {e}", exc_info=True)
            QApplication.quit()

    def setup_ui(self):
        Configurador.setup_ui(self)

    def setup_menu_bar(self):
        Configurador.setup_menu_bar(self)

    def atualizar_interface(self, *args):
        Atualizador.atualizar_interface(self)
        self.atualizar_status()
        if hasattr(self, 'gerenciador_menus_ui'):
            self.gerenciador_menus_ui.criar_menu_principal()

        if hasattr(self, 'gerenciador_botoes_ui'):
            self.gerenciador_botoes_ui.update_buttons_text(self.loc)

        if hasattr(self, 'painel_filtros'):
            self.painel_filtros.atualizar_interface()

        if hasattr(self, 'gerenciador_tabela'):
            self.gerenciador_tabela.retraduzir_dados_existentes()

        self.atualizar_tradutor_qt(self.loc.idioma_atual)

    def abrir_janela_filtros(self):
        Atualizador.abrir_janela_filtros(self)

    def atualizar_status(self, *args):
        Atualizador.atualizar_status(self, *args)

    def configurar_tabela(self):
        ManipuladorTabela.configurar_tabela(self)

    def verificar_movimentacao(self, evento):
        return self.gerenciador_eventos_arquivo.verificar_movimentacao(evento)

    def adicionar_evento(self, evento):
        self.gerenciador_eventos_arquivo.adicionar_evento(evento)

    def selecionar_diretorio(self):
        logger.info("Usuário iniciou seleção de diretório")
        self.gerenciador_botoes.selecionar_diretorio()

    def alternar_analise_diretorio(self):
        logger.info("Usuário alternando análise de diretório")
        self.gerenciador_botoes.alternar_analise_diretorio()

    def salvar_dados(self):
        self.gerenciador_dados.salvar_dados()

    def abrir_salvar_como(self):
        self.gerenciador_dados.abrir_salvar_como()

    def mostrar_estatisticas(self):
        self.gerenciador_estatisticas_ui.mostrar_estatisticas()

    def salvar_todos_graficos(self, gerador):
        self.gerenciador_estatisticas_ui.salvar_todos_graficos(gerador)

    def limpar_dados(self):
        self.gerenciador_limpeza.limpar_dados()

    def sair_aplicacao(self):
        self.close()

    @Slot()
    def criar_barra_progresso(self):
        GerenciadorProgresso.criar_barra_progresso(self)

    @Slot(int, int, int)
    def atualizar_progresso_scan(self, progresso, contador, total):
        GerenciadorProgresso.atualizar_progresso_scan(self, progresso, contador, total)

    def alternar_filtro(self):
        self.gerenciador_eventos_ui.alternar_filtro()

    def alternar_visibilidade_coluna(self):
        self.gerenciador_eventos_ui.alternar_visibilidade_coluna()

    def resetar_colunas(self):
        self.gerenciador_eventos_ui.resetar_colunas()

    def alterar_idioma(self):
        self.gerenciador_eventos_ui.alterar_idioma()

    def atualizar_visibilidade_colunas(self):
        ManipuladorTabela.atualizar_visibilidade_colunas(self)

    def reiniciar_sistema_monitoramento(self):
        self.gerenciador_monitoramento.reiniciar_sistema_monitoramento()

    def atualizar_tradutor_qt(self, idioma):
        logger = LogManager.get_logger()
        logger.debug(f"Atualizando tradutor Qt para idioma: {idioma}")
        QApplication.processEvents()

    @Slot(dict)
    def _atualizar_cores_tabela(self, resultado_cores):
        try:
            if hasattr(self, 'gerenciador_tabela'):
                self.gerenciador_tabela._atualizar_cores_na_interface(resultado_cores)
                self.gerenciador_tabela.atualizar_interface_pos_processamento(resultado_cores)

        except Exception as e:
            logger.error(f"Erro ao atualizar cores da tabela: {e}", exc_info=True)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'gerenciador_menus_ui') and hasattr(self.gerenciador_menus_ui, 'gerenciador_cores'):
                thread_cores = self.gerenciador_menus_ui.gerenciador_cores.thread_cores
                if thread_cores and thread_cores.isRunning():
                    thread_cores.quit()
                    thread_cores.wait()

            if hasattr(self, 'gerenciador_tabela') and hasattr(self.gerenciador_tabela, 'executor'):
                logger.debug("Encerrando ThreadPoolExecutor do GerenciadorTabela")
                self.gerenciador_tabela.executor.shutdown(wait=True)

            if (hasattr(self, 'gerenciador_tabela') and 
                hasattr(self.gerenciador_tabela, 'timer_atualizacao')):
                self.gerenciador_tabela.timer_atualizacao.stop()

            logger.info("Recursos da aplicação finalizados adequadamente")

        except Exception as e:
            logger.error(f"Erro ao fechar recursos da aplicação: {e}", exc_info=True)

        finally:
            super().closeEvent(event)

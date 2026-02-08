import os
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from .ob_10_GerenciadorTabela import GerenciadorTabela
from Observador.GerenciamentoMetadados import (
    get_atributos_arquivo,
    get_autor_arquivo,
    get_dimensoes_arquivo,
    get_duracao_arquivo,
    get_taxa_bits_arquivo,
    get_protecao_arquivo,
    atualizar_interface,
    salvar_estado_tabela,
    restaurar_estado_tabela,
    carregar_configuracoes,
    salvar_configuracoes,
    processar_fila_metadados,
    callback_metadados,
    configurar_tabela,
    mostrar_dialogo_configuracao,
    invalidar_cache_diretorios_relacionados,
    get_metadados_gc,
    identificar_tipo_arquivo_gc,
    adicionar_metadados_ao_item,
    processar_coluna_thread,
    adicionar_item_para_coluna,
    atualizar_coluna_interface,
    extrair_metadados_em_lote,
    _metadados_extraidos_callback,
    _get_size_unit,
    _get_tamanho_bytes
)
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GerenciadorColunas:
    def __init__(self, interface_monitor):
        try:
            self.interface = interface_monitor
            if hasattr(interface_monitor, 'loc'):
                self.loc = interface_monitor.loc

            else:
                self.loc = interface_monitor.observador.loc

            self.loc.idioma_alterado.connect(self.atualizar_interface)
            self.config_path = os.path.join(obter_caminho_persistente(), "colunas_config.json")

            self.cache_metadados = {}
            self.fila_metadados = queue.Queue()
            self.executor = ThreadPoolExecutor(max_workers=2)
            self.executor_metadados = ThreadPoolExecutor(max_workers=4)
            self.lock_cache = threading.Lock()
            self.processando_metadados = False
            if hasattr(interface_monitor, "tabela_dados"):
                self.gerenciador_tabela = GerenciadorTabela(interface_monitor)

            else:
                self.gerenciador_tabela = None

            self.thread_metadados = threading.Thread(target=self.processar_fila_metadados, daemon=True)
            self.thread_metadados.start()
            self.COLUNAS_DISPONIVEIS = {
                "tipo_operacao": {
                    "translation_key": "operation_type",
                    "nome": self.loc.get_text("operation_type"),
                    "visivel": True,
                    "ordem": 0,
                    "getter": lambda item: item.get("tipo_operacao", "")
                },
                "nome": {
                    "translation_key": "name",
                    "nome": self.loc.get_text("name"),
                    "visivel": True,
                    "ordem": 1,
                    "getter": lambda item: item.get("nome", "")
                },
                "dir_anterior": {
                    "translation_key": "prev_dir",
                    "nome": self.loc.get_text("prev_dir"),
                    "visivel": True,
                    "ordem": 2,
                    "getter": lambda item: item.get("dir_anterior", "")
                },
                "dir_atual": {
                    "translation_key": "curr_dir",
                    "nome": self.loc.get_text("curr_dir"),
                    "visivel": True,
                    "ordem": 3,
                    "getter": lambda item: item.get("dir_atual", "")
                },
                "data_criacao": {
                    "translation_key": "creation_date",
                    "nome": self.loc.get_text("creation_date"),
                    "visivel": False,
                    "ordem": 4,
                    "getter": lambda item: item.get("data_criacao", "")
                },
                "data_modificacao": {
                    "translation_key": "modification_date",
                    "nome": self.loc.get_text("modification_date"),
                    "visivel": True,
                    "ordem": 6,
                    "getter": lambda item: item.get("data_modificacao", "")
                },
                "data_acesso": {
                    "translation_key": "access_date",
                    "nome": self.loc.get_text("access_date"),
                    "visivel": False,
                    "ordem": 7,
                    "getter": lambda item: item.get("data_acesso", "")
                },
                "tipo": {
                    "translation_key": "type",
                    "nome": self.loc.get_text("type"),
                    "visivel": True,
                    "ordem": 8,
                    "getter": lambda item: item.get("tipo", "")
                },
                "size_b": {
                    "translation_key": "size_b",
                    "nome": self.loc.get_text("size_b"),
                    "visivel": False,
                    "ordem": 9,
                    "getter": lambda item: self._get_size_unit(item, "B")
                },
                "size_kb": {
                    "translation_key": "size_kb",
                    "nome": self.loc.get_text("size_kb"),
                    "visivel": True,
                    "ordem": 10,
                    "getter": lambda item: self._get_size_unit(item, "KB")
                },
                "size_mb": {
                    "translation_key": "size_mb",
                    "nome": self.loc.get_text("size_mb"),
                    "visivel": False,
                    "ordem": 11,
                    "getter": lambda item: self._get_size_unit(item, "MB")
                },
                "size_gb": {
                    "translation_key": "size_gb",
                    "nome": self.loc.get_text("size_gb"),
                    "visivel": False,
                    "ordem": 12,
                    "getter": lambda item: self._get_size_unit(item, "GB")
                },
                "size_tb": {
                    "translation_key": "size_tb",
                    "nome": self.loc.get_text("size_tb"),
                    "visivel": False,
                    "ordem": 13,
                    "getter": lambda item: self._get_size_unit(item, "TB")
                },
                "atributos": {
                    "translation_key": "attributes",
                    "nome": self.loc.get_text("attributes"),
                    "visivel": False,
                    "ordem": 14,
                    "getter": lambda item: get_atributos_arquivo(item, self.loc)
                },
                "autor": {
                    "translation_key": "author",
                    "nome": self.loc.get_text("author"),
                    "visivel": False,
                    "ordem": 15,
                    "getter": lambda item: get_autor_arquivo(item, self.loc)
                },
                "dimensoes": {
                    "translation_key": "dimensions",
                    "nome": self.loc.get_text("dimensions"),
                    "visivel": False,
                    "ordem": 16,
                    "getter": lambda item: get_dimensoes_arquivo(self, item, self.loc)
                },
                "duracao": {
                    "translation_key": "duration",
                    "nome": self.loc.get_text("duration"),
                    "visivel": False,
                    "ordem": 17,
                    "getter": lambda item: get_duracao_arquivo(self, item)
                },
                "taxa_bits": {
                    "translation_key": "bit_rate",
                    "nome": self.loc.get_text("bit_rate"),
                    "visivel": False,
                    "ordem": 18,
                    "getter": lambda item: get_taxa_bits_arquivo(self, item)
                },
                "protegido": {
                    "translation_key": "protected",
                    "nome": self.loc.get_text("protected"),
                    "visivel": False,
                    "ordem": 19,
                    "getter": lambda item: get_protecao_arquivo(self, item, self.loc)
                },
                "paginas": {
                    "translation_key": "pages",
                    "nome": self.loc.get_text("pages"),
                    "visivel": False,
                    "ordem": 20,
                    "getter": lambda item: item.get("paginas", "")
                },
                "linhas": {
                    "translation_key": "lines",
                    "nome": self.loc.get_text("lines"),
                    "visivel": False,
                    "ordem": 21,
                    "getter": lambda item: item.get("linhas", "")
                },
                "palavras": {
                    "translation_key": "words",
                    "nome": self.loc.get_text("words"),
                    "visivel": False,
                    "ordem": 22,
                    "getter": lambda item: item.get("palavras", "")
                },
                "paginas_estimadas": {
                    "translation_key": "pages_estimated",
                    "nome": self.loc.get_text("pages_estimated"),
                    "visivel": False,
                    "ordem": 23,
                    "getter": lambda item: item.get("paginas_estimadas", "")
                },
                "linhas_codigo": {
                    "translation_key": "lines_code",
                    "nome": self.loc.get_text("lines_code"),
                    "visivel": False,
                    "ordem": 24,
                    "getter": lambda item: item.get("linhas_codigo", "")
                },
                "total_linhas": {
                    "translation_key": "total_lines",
                    "nome": self.loc.get_text("total_lines"),
                    "visivel": False,
                    "ordem": 25,
                    "getter": lambda item: item.get("total_linhas", "")
                },
                "slides_estimados": {
                    "translation_key": "slides_estimated",
                    "nome": self.loc.get_text("slides_estimated"),
                    "visivel": False,
                    "ordem": 26,
                    "getter": lambda item: item.get("slides_estimados", "")
                },
                "arquivos": {
                    "translation_key": "files",
                    "nome": self.loc.get_text("files"),
                    "visivel": False,
                    "ordem": 27,
                    "getter": lambda item: item.get("arquivos", "")
                },
                "unzipped_b": {
                    "translation_key": "unzipped_b",
                    "nome": self.loc.get_text("unzipped_b"),
                    "visivel": False,
                    "ordem": 28,
                    "getter": lambda item: self._get_unzipped_unit(item, "B")
                },
                "unzipped_kb": {
                    "translation_key": "unzipped_kb",
                    "nome": self.loc.get_text("unzipped_kb"),
                    "visivel": False,
                    "ordem": 29,
                    "getter": lambda item: self._get_unzipped_unit(item, "KB")
                },
                "unzipped_mb": {
                    "translation_key": "unzipped_mb",
                    "nome": self.loc.get_text("unzipped_mb"),
                    "visivel": False,
                    "ordem": 30,
                    "getter": lambda item: self._get_unzipped_unit(item, "MB")
                },
                "unzipped_gb": {
                    "translation_key": "unzipped_gb",
                    "nome": self.loc.get_text("unzipped_gb"),
                    "visivel": False,
                    "ordem": 31,
                    "getter": lambda item: self._get_unzipped_unit(item, "GB")
                },
                "unzipped_tb": {
                    "translation_key": "unzipped_tb",
                    "nome": self.loc.get_text("unzipped_tb"),
                    "visivel": False,
                    "ordem": 32,
                    "getter": lambda item: self._get_unzipped_unit(item, "TB")
                },
                "slides": {
                    "translation_key": "slides",
                    "nome": self.loc.get_text("slides"),
                    "visivel": False,
                    "ordem": 33,
                    "getter": lambda item: item.get("slides", "")
                },
                "binary_file_b": {
                    "translation_key": "binary_file_b",
                    "nome": self.loc.get_text("binary_file_b"),
                    "visivel": False,
                    "ordem": 34,
                    "getter": lambda item: self._get_binary_unit(item, "B")
                },
                "binary_file_kb": {
                    "translation_key": "binary_file_kb",
                    "nome": self.loc.get_text("binary_file_kb"),
                    "visivel": False,
                    "ordem": 35,
                    "getter": lambda item: self._get_binary_unit(item, "KB")
                },
                "binary_file_mb": {
                    "translation_key": "binary_file_mb",
                    "nome": self.loc.get_text("binary_file_mb"),
                    "visivel": False,
                    "ordem": 36,
                    "getter": lambda item: self._get_binary_unit(item, "MB")
                },
                "binary_file_gb": {
                    "translation_key": "binary_file_gb",
                    "nome": self.loc.get_text("binary_file_gb"),
                    "visivel": False,
                    "ordem": 37,
                    "getter": lambda item: self._get_binary_unit(item, "GB")
                },
                "binary_file_tb": {
                    "translation_key": "binary_file_tb",
                    "nome": self.loc.get_text("binary_file_tb"),
                    "visivel": False,
                    "ordem": 38,
                    "getter": lambda item: self._get_binary_unit(item, "TB")
                },
                "planilhas": {
                    "translation_key": "spreadsheets",
                    "nome": self.loc.get_text("spreadsheets"),
                    "visivel": False,
                    "ordem": 39,
                    "getter": lambda item: item.get("planilhas", "")
                },
                "colunas": {
                    "translation_key": "columns",
                    "nome": self.loc.get_text("columns"),
                    "visivel": False,
                    "ordem": 40,
                    "getter": lambda item: item.get("colunas", "")
                },
                "registros": {
                    "translation_key": "records",
                    "nome": self.loc.get_text("records"),
                    "visivel": False,
                    "ordem": 41,
                    "getter": lambda item: item.get("registros", "")
                },
                "tabelas": {
                    "translation_key": "tables",
                    "nome": self.loc.get_text("tables"),
                    "visivel": False,
                    "ordem": 42,
                    "getter": lambda item: item.get("tabelas", "")
                },
                "timestamp": {
                    "translation_key": "timestamp",
                    "nome": self.loc.get_text("timestamp"),
                    "visivel": True,
                    "ordem": 43,
                    "getter": lambda item: item.get("timestamp", "")
                }
            }
            self.carregar_configuracoes()
            self.filas_colunas = {}
            self.threads_colunas = {}
            self.resultados_colunas = {}
            self.lock_resultados = threading.Lock()
            for coluna_key in self.COLUNAS_DISPONIVEIS.keys():
                self.filas_colunas[coluna_key] = queue.Queue()
                thread = threading.Thread(
                    target=self.processar_coluna_thread,
                    args=(coluna_key,),
                    daemon=True
                )
                self.threads_colunas[coluna_key] = thread
                thread.start()

        except Exception as e:
            logger.error(f"Erro ao iniciar threads de colunas: {e}", exc_info=True)

    def atualizar_interface(self, idioma: str):
        return atualizar_interface(self, idioma)

    def salvar_estado_tabela(self, tabela):
        return salvar_estado_tabela(self, tabela)

    def restaurar_estado_tabela(self, tabela, eventos):
        return restaurar_estado_tabela(self, tabela, eventos)

    def carregar_configuracoes(self):
        return carregar_configuracoes(self)

    def salvar_configuracoes(self):
        return salvar_configuracoes(self)

    def processar_fila_metadados(self):
        return processar_fila_metadados(self)

    def callback_metadados(self, futuro):
        return callback_metadados(self, futuro)

    def configurar_tabela(self, tabela):
        return configurar_tabela(self, tabela)

    def mostrar_dialogo_configuracao(self, pos=None):
        return mostrar_dialogo_configuracao(self, pos)

    def _invalidar_cache_diretorios_relacionados(self, caminho: str):
        return invalidar_cache_diretorios_relacionados(self, caminho)

    def get_metadados(self, item):
        return get_metadados_gc(self, item)

    def identificar_tipo_arquivo(self, caminho):
        return identificar_tipo_arquivo_gc(self, caminho)

    def adicionar_metadados_ao_item(self, item):
        return adicionar_metadados_ao_item(self, item)

    def processar_coluna_thread(self, coluna_key):
        return processar_coluna_thread(self, coluna_key)

    def adicionar_item_para_coluna(self, coluna_key, item):
        return adicionar_item_para_coluna(self, coluna_key, item)

    def atualizar_coluna_interface(self, coluna_key=None):
        return atualizar_coluna_interface(self, coluna_key)

    def extrair_metadados_em_lote(self, lista_itens):
        return extrair_metadados_em_lote(self, lista_itens)

    def _metadados_extraidos_callback(self, futuro):
        return _metadados_extraidos_callback(self, futuro)

    def _get_size_unit(self, item, unidade):
        return _get_size_unit(self, item, unidade)

    def _get_tamanho_bytes(self, item):
        return _get_tamanho_bytes(self, item)

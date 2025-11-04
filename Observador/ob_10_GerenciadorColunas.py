import os
import json
import queue
import time
import threading
from PySide6.QtGui import QColor
from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import QTableWidgetItem
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from .ob_11_GerenciadorTabela import GerenciadorTabela
from Observador.GerenciamentoMetadados import (
    extrair_metadados_codigo_fonte,
    extrair_metadados_imagem,
    extrair_metadados_audio,
    extrair_metadados_video,
    extrair_metadados_documento,
    extrair_metadados_planilha,
    extrair_metadados_apresentacao,
    extrair_metadados_banco_dados,
    extrair_metadados_executavel,
    extrair_metadados_temporario,
    extrair_metadados_compactados,
    extrair_metadados_backup,
    extrair_metadados_log,
    extrair_metadados_config,
    extrair_metadados_olefile,
    identificar_tipo_arquivo,
    get_atributos_arquivo,
    get_autor_arquivo,
    get_dimensoes_arquivo,
    get_duracao_arquivo,
    get_taxa_bits_arquivo,
    get_protecao_arquivo
)
from utils.CaminhoPersistenteUtils import obter_caminho_persistente


class GerenciadorColunas:
    def __init__(self, interface_monitor):
        self.interface = interface_monitor
        if hasattr(interface_monitor, 'loc'):
            self.loc = interface_monitor.loc

        else:
            self.loc = interface_monitor.observador.loc

        self.loc.idioma_alterado.connect(self.atualizar_interface)

        self.config_path = os.path.join(obter_caminho_persistente(), "colunas_config.json")
        print(f"Caminho de configuração das colunas: {self.config_path}")

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

    def atualizar_interface(self, idioma: str):
        for key, coluna in self.COLUNAS_DISPONIVEIS.items():
            tk = coluna.get("translation_key", key)
            self.COLUNAS_DISPONIVEIS[key]["nome"] = self.loc.get_text(tk)

        with self.lock_cache:
            self.cache_metadados.clear()

        if hasattr(self.interface, 'gerenciador_tabela'):
            self.interface.gerenciador_tabela.atualizar_dados_tabela(self.interface.tabela_dados)

        else:
            self.gerenciador_tabela.configurar_tabela(self.interface.tabela_dados)

    def salvar_estado_tabela(self, tabela):
        eventos = []
        for row in range(tabela.rowCount()):
            evento = {}
            for col in range(tabela.columnCount()):
                header = tabela.horizontalHeaderItem(col).text()
                item = tabela.item(row, col)
                if item:
                    evento[header] = item.text()

            eventos.append(evento)

        return eventos

    def restaurar_estado_tabela(self, tabela, eventos):
        tabela.clearContents()
        tabela.setRowCount(len(eventos))

        colunas_visiveis = [(key, col) for key, col in sorted(self.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]) if col["visivel"]]

        for row, evento in enumerate(eventos):
            for col, (key, coluna) in enumerate(colunas_visiveis):
                valor = evento.get(coluna["nome"], "")
                item = QTableWidgetItem(str(valor))

                if key == "tipo_operacao":
                    cores = {
                        self.loc.get_text("op_renamed"): QColor(0, 255, 0),
                        self.loc.get_text("op_added"): QColor(0, 0, 255), 
                        self.loc.get_text("op_deleted"): QColor(255, 0, 0),
                        self.loc.get_text("op_modified"): QColor(255, 98, 0),
                        self.loc.get_text("op_moved"): QColor(255, 0, 255),
                        self.loc.get_text("op_scanned"): QColor(128, 128, 128)
                    }

                    item.setBackground(cores.get(valor, QColor(255, 255, 255)))

                tabela.setItem(row, col, item)

    def carregar_configuracoes(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)

                for k, v in config.items():
                    if k in self.COLUNAS_DISPONIVEIS:
                        self.COLUNAS_DISPONIVEIS[k]["visivel"] = v["visivel"]
                        self.COLUNAS_DISPONIVEIS[k]["ordem"] = v["ordem"]

        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")

    def salvar_configuracoes(self):
        config = {k: {"visivel": v["visivel"], "ordem": v["ordem"]} for k, v in self.COLUNAS_DISPONIVEIS.items()}

        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)

        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def processar_fila_metadados(self):
        while True:
            try:
                item = self.fila_metadados.get(timeout=1)
                caminho = item.get("dir_atual") or item.get("dir_anterior")

                if not caminho or not os.path.exists(caminho):
                    tipo = identificar_tipo_arquivo(caminho, self.loc, item.get("nome"))
                    metadados = {"tipo": tipo}
                    return metadados

                time.sleep(0.1)

                if os.path.exists(caminho):
                    metadados = self.get_metadados(item)

                    if metadados:
                        with self.lock_cache:
                            self.cache_metadados[caminho] = metadados

                        QMetaObject.invokeMethod(self.interface, "atualizar_colunas_tabela", Qt.QueuedConnection)

            except queue.Empty:
                continue

            except Exception as e:
                print(f"Erro no processamento de metadados: {e}")

    def callback_metadados(self, futuro):
        try:
            caminho, metadados = futuro.result()
            with self.lock_cache:
                self.cache_metadados[caminho] = metadados

            self.interface.atualizar_status()

        except Exception as e:
            print(f"Erro no callback: {e}")

    def configurar_tabela(self, tabela):
        self.gerenciador_tabela.configurar_tabela(tabela)

    def mostrar_dialogo_configuracao(self, pos=None):
        self.gerenciador_tabela.mostrar_dialogo_configuracao(pos)

    def _invalidar_cache_diretorios_relacionados(self, caminho: str):
        try:
            chaves_tamanho = {
                "tamanho_dir", "tamanho", "tamanho_dir_bytes",
                "tamanho_dir_mtime", "tamanho_dir_cached_at"
            }
            with self.lock_cache:
                if os.path.isfile(caminho):
                    dir_pai = os.path.dirname(caminho)
                    if dir_pai in self.cache_metadados:
                        for k in list(chaves_tamanho):
                            if k in self.cache_metadados[dir_pai]:
                                self.cache_metadados[dir_pai].pop(k, None)
                                print(f"Cache invalidado para diretório pai: {dir_pai}")

                        if not self.cache_metadados[dir_pai]:
                            self.cache_metadados.pop(dir_pai, None)

                dir_atual = os.path.dirname(caminho) if os.path.isfile(caminho) else caminho
                while True:
                    if dir_atual in self.cache_metadados:
                        for k in list(chaves_tamanho):
                            if k in self.cache_metadados[dir_atual]:
                                self.cache_metadados[dir_atual].pop(k, None)

                        if not self.cache_metadados[dir_atual]:
                            self.cache_metadados.pop(dir_atual, None)

                    pai = os.path.dirname(dir_atual)
                    if not pai or pai == dir_atual:
                        break

                    dir_atual = pai

                if os.path.isdir(caminho):
                    for root, dirs, files in os.walk(caminho):
                        if root in self.cache_metadados:
                            for k in list(chaves_tamanho):
                                if k in self.cache_metadados[root]:
                                    self.cache_metadados[root].pop(k, None)

                            if not self.cache_metadados[root]:
                                self.cache_metadados.pop(root, None)

        except Exception as e:
            print(f"Erro ao invalidar cache de diretórios: {e}")

    def get_metadados(self, item):
        try:
            from Observador.GerenciamentoMetadados.gmet_21_GetFormataTamanho import get_formata_tamanho

            caminho = item.get("dir_atual") or item.get("dir_anterior")
            if not caminho or not os.path.exists(caminho):
                tipo = identificar_tipo_arquivo(caminho, self.loc, item.get("nome"))
                metadados = {"tipo": tipo}
                return metadados

            tipo_operacao = item.get("tipo_operacao", "")
            ops_invalida = {
                self.loc.get_text("op_added"),
                self.loc.get_text("op_deleted"),
                self.loc.get_text("op_modified"),
                self.loc.get_text("op_moved"),
                self.loc.get_text("op_renamed"),
            }
            if tipo_operacao in ops_invalida:
                self._invalidar_cache_diretorios_relacionados(caminho)

            if tipo_operacao == self.loc.get_text("op_added") and os.path.isfile(caminho):
                with self.lock_cache:
                    if caminho in self.cache_metadados:
                        self.cache_metadados.pop(caminho, None)

            with self.lock_cache:
                if caminho in self.cache_metadados:
                    if (tipo_operacao == self.loc.get_text("op_added") and 
                        os.path.isdir(caminho) and 
                        self.cache_metadados[caminho].get("tamanho_dir_bytes", 0) == 0):
                        print(f"Removendo cache zerado para diretório adicionado: {caminho}")
                        self.cache_metadados.pop(caminho, None)

                    else:
                        for campo in [
                            "paginas", 
                            "linhas", 
                            "palavras", 
                            "paginas_estimadas", 
                            "linhas_codigo", 
                            "total_linhas", 
                            "slides_estimadas", 
                            "arquivos", 
                            "unzipped_b", 
                            "unzipped_kb", 
                            "unzipped_mb", 
                            "unzipped_gb", 
                            "unzipped_tb", 
                            "slides", 
                            "binary_file_b", 
                            "binary_file_kb", 
                            "binary_file_mb", 
                            "binary_file_gb", 
                            "binary_file_tb", 
                            "planilhas", 
                            "colunas", 
                            "registros", 
                            "tabelas"
                            ]:
                            if campo in self.cache_metadados[caminho]:
                                item[campo] = self.cache_metadados[caminho][campo]

                        return self.cache_metadados[caminho]

            if os.path.exists(caminho):
                stats = os.stat(caminho)
                tamanho_bytes = stats.st_size if os.path.isfile(caminho) else self._get_tamanho_bytes(item)
                metadados = {
                    "size_b": int(tamanho_bytes),
                    "size_kb": round(tamanho_bytes / 1024, 2),
                    "size_mb": round(tamanho_bytes / 1024**2, 2),
                    "size_gb": round(tamanho_bytes / 1024**3, 2),
                    "size_tb": round(tamanho_bytes / 1024**4, 2),
                    "data_acesso": datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
                    "data_modificacao": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "data_criacao": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    "atributos": get_atributos_arquivo(item, self.loc),
                    "autor": get_autor_arquivo(item, self.loc),
                    "protegido": get_protecao_arquivo(self, item, self.loc)
                }

                try:
                    tipo = identificar_tipo_arquivo(caminho, self.loc)
                    metadados["tipo"] = tipo

                    ext = os.path.splitext(caminho)[1].lower()
                    if ext == '.dat':
                        from Observador.GerenciamentoMetadados.gmet_17_ExtrairMetadadosDadosEstruturados import extrair_metadados_dados_estruturados
                        metadados_dat = extrair_metadados_dados_estruturados(caminho, self.loc)
                        metadados.update(metadados_dat)

                    elif os.path.isfile(caminho):
                        if tipo == self.loc.get_text("file_image"):
                            metadados.update(extrair_metadados_imagem(caminho))

                        elif tipo == self.loc.get_text("file_audio"):
                            metadados.update(extrair_metadados_audio(caminho))

                        elif tipo == self.loc.get_text("file_video"):
                            metadados.update(extrair_metadados_video(caminho))

                        elif tipo == self.loc.get_text("file_document"):
                            metadados.update(extrair_metadados_documento(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_spreadsheet"):
                            metadados.update(extrair_metadados_planilha(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_presentation"):
                            metadados.update(extrair_metadados_apresentacao(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_database"):
                            metadados.update(extrair_metadados_banco_dados(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_executable"):
                            metadados.update(extrair_metadados_executavel(caminho, self.loc))
                            try:
                                tamanho_bytes = os.path.getsize(caminho)
                                metadados["binary_file_b"] = int(tamanho_bytes)
                                metadados["binary_file_kb"] = round(tamanho_bytes / 1024, 2)
                                metadados["binary_file_mb"] = round(tamanho_bytes / 1024**2, 2)
                                metadados["binary_file_gb"] = round(tamanho_bytes / 1024**3, 2)
                                metadados["binary_file_tb"] = round(tamanho_bytes / 1024**4, 2)

                            except Exception as e:
                                print(f"Erro ao calcular tamanho do executável: {e}")

                        elif tipo == self.loc.get_text("file_source_code"):
                            metadados.update(extrair_metadados_codigo_fonte(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_temp"):
                            metadados.update(extrair_metadados_temporario(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_compressed"):
                            metadados_compactados = extrair_metadados_compactados(caminho, self.loc)
                            metadados.update(metadados_compactados)
                            t_unzipped = metadados_compactados.get("tamanho_descompactado_bytes")
                            if t_unzipped is not None:
                                metadados["unzipped_b"] = int(t_unzipped)
                                metadados["unzipped_kb"] = round(t_unzipped / 1024, 2)
                                metadados["unzipped_mb"] = round(t_unzipped / 1024**2, 2)
                                metadados["unzipped_gb"] = round(t_unzipped / 1024**3, 2)
                                metadados["unzipped_tb"] = round(t_unzipped / 1024**4, 2)

                        elif tipo == self.loc.get_text("file_backup"):
                            metadados.update(extrair_metadados_backup(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_log"):
                            metadados.update(extrair_metadados_log(caminho, self.loc))

                        elif tipo == self.loc.get_text("file_config"):
                            metadados.update(extrair_metadados_config(caminho, self.loc))

                        ext = os.path.splitext(caminho)[1].lower()
                        if ext in ['.doc', '.xls', '.ppt', '.msg']:
                            metadados.update(extrair_metadados_olefile(caminho, self.loc))

                    metadados["atributos"] = get_atributos_arquivo(item, self.loc)
                    metadados["autor"] = get_autor_arquivo(item, self.loc)
                    metadados["protegido"] = get_protecao_arquivo(self, item, self.loc)

                    get_dimensoes_arquivo(self, item, self.loc)

                    with self.lock_cache:
                        if caminho in self.cache_metadados:
                            for campo in [
                                "paginas", 
                                "linhas", 
                                "palavras", 
                                "paginas_estimadas", 
                                "linhas_codigo", 
                                "total_linhas", 
                                "slides_estimadas", 
                                "arquivos", 
                                "unzipped_b", 
                                "unzipped_kb", 
                                "unzipped_mb", 
                                "unzipped_gb", 
                                "unzipped_tb", 
                                "slides", 
                                "binary_file_b", 
                                "binary_file_kb", 
                                "binary_file_mb", 
                                "binary_file_gb", 
                                "binary_file_tb", 
                                "planilhas", 
                                "colunas", 
                                "registros", 
                                "tabelas"
                                ]:
                                if campo in self.cache_metadados[caminho]:
                                    metadados[campo] = self.cache_metadados[caminho][campo]
                                    item[campo] = self.cache_metadados[caminho][campo]

                except Exception as e:
                    print(f"Erro ao extrair metadados específicos: {e}")

                with self.lock_cache:
                    self.cache_metadados[caminho] = metadados

                for campo, valor in metadados.items():
                    item[campo] = valor

                return metadados

            return {}

        except Exception as e:
            print(f"Erro ao obter metadados: {e}")
            return {}

    def identificar_tipo_arquivo(self, caminho):
        from Observador.GerenciamentoMetadados import identificar_tipo_arquivo
        return identificar_tipo_arquivo(caminho, self.loc)

    def adicionar_metadados_ao_item(self, item):
        try:
            metadados = self.get_metadados(item)
            if metadados:
                for campo, valor in metadados.items():
                    if campo not in item or not item[campo]:
                        item[campo] = valor

            return item

        except Exception as e:
            print(f"Erro ao adicionar metadados ao item: {e}")
            return item

    def processar_coluna_thread(self, coluna_key):
        while True:
            try:
                item = self.filas_colunas[coluna_key].get(timeout=1)
                getter = self.COLUNAS_DISPONIVEIS[coluna_key].get("getter")
                if getter:
                    valor = getter(item)
                    with self.lock_resultados:
                        if coluna_key not in self.resultados_colunas:
                            self.resultados_colunas[coluna_key] = []

                        self.resultados_colunas[coluna_key].append((item, valor))

                    QMetaObject.invokeMethod(self.interface, "atualizar_coluna_interface", Qt.QueuedConnection,)

            except queue.Empty:
                continue

            except Exception as e:
                print(f"Erro na thread da coluna '{coluna_key}': {e}")

    def adicionar_item_para_coluna(self, coluna_key, item):
        if coluna_key in self.filas_colunas:
            self.filas_colunas[coluna_key].put(item)

    def atualizar_coluna_interface(self, coluna_key=None):
        with self.lock_resultados:
            if coluna_key and coluna_key in self.resultados_colunas:
                resultados = self.resultados_colunas[coluna_key]
                for item, valor in resultados:
                    pass

                self.resultados_colunas[coluna_key] = []

    def extrair_metadados_em_lote(self, lista_itens):
        futuros = []
        for item in lista_itens:
            futuros.append(self.executor_metadados.submit(self.get_metadados, item))

        for futuro in futuros:
            futuro.add_done_callback(self._metadados_extraidos_callback)

    def _metadados_extraidos_callback(self, futuro):
        metadados = futuro.result()
        QMetaObject.invokeMethod(self.interface, "atualizar_colunas_tabela", Qt.QueuedConnection)

    def _get_size_unit(self, item, unidade):
        tamanho_bytes = self._get_tamanho_bytes(item)
        if unidade == "B":
            return int(tamanho_bytes)

        elif unidade == "KB":
            return round(tamanho_bytes / 1024, 2)

        elif unidade == "MB":
            return round(tamanho_bytes / 1024**2, 2)

        elif unidade == "GB":
            return round(tamanho_bytes / 1024**3, 2)

        elif unidade == "TB":
            return round(tamanho_bytes / 1024**4, 2)

        return 0

    def _get_tamanho_bytes(self, item):
        caminho = item.get("dir_atual") or item.get("dir_anterior")
        if caminho and os.path.exists(caminho):
            if os.path.isfile(caminho):
                return os.path.getsize(caminho)

            elif os.path.isdir(caminho):
                total = 0
                for root, dirs, files in os.walk(caminho):
                    for f in files:
                        try:
                            total += os.path.getsize(os.path.join(root, f))

                        except Exception:
                            pass

                return total

        return 0

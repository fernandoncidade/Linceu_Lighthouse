from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class EventTableModel(QAbstractTableModel):
    def __init__(self, interface, parent=None):
        super().__init__(parent)
        self.interface = interface
        self.colunas_disponiveis = [(key, col) for key, col in sorted(
            self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(),
            key=lambda x: x[1]["ordem"]
        )]
        self._data = []
        self._getters = {key: getattr(self.interface.gerenciador_colunas, f"get_{key}", None)
                         for key, _ in self.colunas_disponiveis}

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.colunas_disponiveis)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            key, meta = self.colunas_disponiveis[section]
            try:
                return self.interface.loc.traduzir_metadados(meta.get("titulo", key), key)

            except Exception:
                return meta.get("titulo", key)

        else:
            return str(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role not in (Qt.DisplayRole,):
            return None

        try:
            evento = self._data[index.row()]
            key, _ = self.colunas_disponiveis[index.column()]
            getter = self._getters.get(key)
            valor = getter(evento) if getter else evento.get(key, "")

            if key == "tipo_operacao" and valor:
                valor = self.interface.loc.traduzir_tipo_operacao(valor)

            elif key in [
                "tipo_operacao", 
                "nome", 
                "dir_anterior", 
                "dir_atual",
                "data_criacao", 
                "data_modificacao", 
                "data_acesso",
                "tipo", 
                "size_b", 
                "size_kb", 
                "size_mb", 
                "size_gb", 
                "size_tb",
                "atributos", 
                "autor", 
                "dimensoes", 
                "duracao", 
                "taxa_bits",
                "protegido", 
                "paginas", 
                "linhas", 
                "palavras",
                "paginas_estimadas", 
                "linhas_codigo", 
                "total_linhas",
                "slides_estimados", 
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
                valor = self.interface.loc.traduzir_metadados(valor, key)

            if key in ("dir_anterior", "dir_atual") and valor:
                import os
                valor = os.path.normpath(str(valor)).replace('/', '\\')
                if valor == ".":
                    valor = ""

            return str(valor)

        except Exception as e:
            logger.debug(f"Falha ao exibir dado [{index.row()},{index.column()}]: {e}", exc_info=True)
            return ""

    def prepend_event(self, evento):
        try:
            self.beginInsertRows(QModelIndex(), 0, 0)
            self._data.insert(0, evento)
            self.endInsertRows()

        except Exception as e:
            logger.error(f"Erro ao inserir evento no modelo: {e}", exc_info=True)

    def append_events(self, eventos):
        if not eventos:
            return

        try:
            first = len(self._data)
            last = first + len(eventos) - 1
            self.beginInsertRows(QModelIndex(), first, last)
            self._data.extend(eventos)
            self.endInsertRows()

        except Exception as e:
            logger.error(f"Erro ao anexar eventos no modelo: {e}", exc_info=True)

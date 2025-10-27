from PySide6.QtCore import Qt, QCoreApplication, Signal
from PySide6.QtWidgets import (QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QFrame)
from .GerenciadorEstruturaDiretoriosWidget.gedw_01_configurar_atalhos import _configurar_atalhos
from .GerenciadorEstruturaDiretoriosWidget.gedw_02_mostrar_menu_contexto import mostrar_menu_contexto
from .GerenciadorEstruturaDiretoriosWidget.gedw_03_obter_selecionados import obter_selecionados
from .GerenciadorEstruturaDiretoriosWidget.gedw_04_copiar_selecionados import copiar_selecionados
from .GerenciadorEstruturaDiretoriosWidget.gedw_05_cortar_selecionados import cortar_selecionados
from .GerenciadorEstruturaDiretoriosWidget.gedw_06_colar_items import colar_items
from .GerenciadorEstruturaDiretoriosWidget.gedw_07_excluir_selecionados import excluir_selecionados
from .GerenciadorEstruturaDiretoriosWidget.gedw_08_renomear_selecionado import renomear_selecionado
from .GerenciadorEstruturaDiretoriosWidget.gedw_09_criar_nova_pasta import criar_nova_pasta
from .GerenciadorEstruturaDiretoriosWidget.gedw_10_criar_novo_arquivo import criar_novo_arquivo
from .GerenciadorEstruturaDiretoriosWidget.gedw_11_abrir_item import abrir_item
from .GerenciadorEstruturaDiretoriosWidget.gedw_12_changeEvent import changeEvent
from .GerenciadorEstruturaDiretoriosWidget.gedw_13_customize_icons import _customize_icons
from .GerenciadorEstruturaDiretoriosWidget.gedw_14_atualizar_status import atualizar_status
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

# Ajustáveis: margens da árvore (left, top, right, bottom) e margens do viewport (left, top, right, bottom)
TREE_LAYOUT_MARGINS = (10, 50, 10, 4)       # alterar aqui para ajustar recuo superior/geral
TREE_VIEWPORT_MARGINS = (6, 6, 0, 0)      # alterar aqui para ajustar recuo interno do QTreeView

# Ajustáveis: contorno do painel de estrutura
STRUCT_VIEW_BORDER_WIDTH = 1               # espessura da borda
STRUCT_VIEW_BORDER_RADIUS = 6              # raio dos cantos (0 para cantos retos)
STRUCT_VIEW_BORDER_COLOR = "palette(mid)"  # cor; use palette(mid) para seguir o tema


class FileSystemModelTraduzido(QFileSystemModel):
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            mapping = {
                0: "name",
                1: "size", 
                2: "type",
                3: "modification_date",
            }
            if section in mapping:
                return QCoreApplication.translate("LinceuLighthouse", mapping[section])

        return super().headerData(section, orientation, role)

    def data(self, index, role=Qt.DisplayRole):
        try:
            if role == Qt.DisplayRole and index.column() == 2:
                try:
                    info = self.fileInfo(index)
                    if info.isDir():
                        translated = QCoreApplication.translate("LinceuLighthouse", "folder")
                        if translated and translated.lower() != "folder":
                            return translated

                        return QCoreApplication.translate("QFileSystemModel", "Folder")

                except Exception:
                    try:
                        if hasattr(self, "isDir") and self.isDir(index):
                            translated = QCoreApplication.translate("LinceuLighthouse", "folder")
                            if translated and translated.lower() != "folder":
                                return translated

                            return QCoreApplication.translate("QFileSystemModel", "Folder")

                    except Exception:
                        pass

                try:
                    info = self.fileInfo(index)
                    suffix = info.suffix()
                    if suffix:
                        return suffix.lower()

                except Exception:
                    pass

                return super().data(index, role)

            return super().data(index, role)

        except Exception as e:
            logger.error(f"Erro ao fornecer dado traduzido para QFileSystemModel: {e}", exc_info=True)
            return super().data(index, role)

    def retranslate(self):
        try:
            self.headerDataChanged.emit(Qt.Horizontal, 0, 3)
            try:
                rows = self.rowCount()
                if rows > 0:
                    top = self.index(0, 2)
                    bottom = self.index(max(0, rows - 1), 2)
                    self.dataChanged.emit(top, bottom, [Qt.DisplayRole])

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao reemitir headerDataChanged/dataChanged: {e}", exc_info=True)


class EstruturaDiretoriosWidget(QWidget):
    arquivo_operacao_realizada = Signal(str, str, str)
    selecionar_diretorio_solicitado = Signal(str)

    def __init__(self, root_path, status_map=None, parent=None):
        super().__init__(parent)
        self.status_map = status_map or {}
        self.root_path = root_path
        self.clipboard_items = []
        self.shortcuts = []

        self.model = FileSystemModelTraduzido()
        self.model.setRootPath(root_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(root_path))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionMode(QTreeView.ExtendedSelection)

        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.mostrar_menu_contexto)

        self.tree.doubleClicked.connect(self.abrir_item)

        layout = QVBoxLayout(self)
        try:
            left, top, right, bottom = TREE_LAYOUT_MARGINS

        except Exception:
            left, top, right, bottom = (10, 8, 4, 4)

        layout.setContentsMargins(left, top, right, bottom)

        try:
            v_left, v_top, v_right, v_bottom = TREE_VIEWPORT_MARGINS
            self.tree.setViewportMargins(v_left, v_top, v_right, v_bottom)

        except Exception as e:
            logger.error(f"Erro ao configurar margens da viewport: {e}", exc_info=True)

        frame = QFrame(self)
        frame.setObjectName("estruturaFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.tree)

        frame.setStyleSheet(
            f"#estruturaFrame {{"
            f"  border: {STRUCT_VIEW_BORDER_WIDTH}px solid {STRUCT_VIEW_BORDER_COLOR};"
            f"  border-radius: {STRUCT_VIEW_BORDER_RADIUS}px;"
            f"}}"
        )

        layout.addWidget(frame)
        self.setLayout(layout)

        self._configurar_atalhos()
        self._customize_icons()

    _configurar_atalhos = _configurar_atalhos
    mostrar_menu_contexto = mostrar_menu_contexto
    obter_selecionados = obter_selecionados
    copiar_selecionados = copiar_selecionados
    cortar_selecionados = cortar_selecionados
    colar_items = colar_items
    excluir_selecionados = excluir_selecionados
    renomear_selecionado = renomear_selecionado
    criar_nova_pasta = criar_nova_pasta
    criar_novo_arquivo = criar_novo_arquivo
    abrir_item = abrir_item
    changeEvent = changeEvent
    _customize_icons = _customize_icons
    atualizar_status = atualizar_status

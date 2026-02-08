from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QSplitter, QSizePolicy
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
from source.ui.ui_15_Manual import get_manual_blocks, get_manual_title, ManualBlock
logger = LogManager.get_logger()


class ManualDialog(QDialog):
    def __init__(self, parent, titulo, lang=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(titulo)
            self.setWindowFlags(
                Qt.Window
                | Qt.WindowTitleHint
                | Qt.WindowSystemMenuHint
                | Qt.WindowCloseButtonHint
                | Qt.WindowMinimizeButtonHint
                | Qt.WindowMaximizeButtonHint
            )
            self.setModal(False)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(6, 6, 6, 6)

            splitter = QSplitter(Qt.Horizontal, self)

            self.toc_list = QListWidget(self)
            self.toc_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            splitter.addWidget(self.toc_list)

            self.browser = QTextBrowser(self)
            self.browser.setOpenExternalLinks(True)
            self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            splitter.addWidget(self.browser)

            splitter.setStretchFactor(0, 1)
            splitter.setStretchFactor(1, 3)
            splitter.setCollapsible(0, False)
            splitter.setCollapsible(1, False)
            splitter.setSizes([280, 820])

            layout.addWidget(splitter, 1)

            footer = QWidget(self)
            footer_layout = QHBoxLayout(footer)
            footer_layout.addStretch()
            btn_ok = QPushButton(self.tr('OK'), self)
            btn_ok.clicked.connect(self.close)
            footer_layout.addWidget(btn_ok)
            layout.addWidget(footer)

            self.setSizeGripEnabled(True)
            self.setMinimumSize(700, 480)
            self.resize(1000, 720)

            self._current_lang = lang or (getattr(parent, 'loc').idioma_atual if hasattr(parent, 'loc') else 'pt_BR')

            self._btn_ok = btn_ok
            self._build_manual_content(self._current_lang)

            try:
                loc = getattr(parent, 'loc', None)
                if loc is not None and hasattr(loc, 'idioma_alterado'):
                    loc.idioma_alterado.connect(self._on_idioma_alterado)

            except Exception:
                pass

            def on_toc_clicked(item: QListWidgetItem):
                sid = item.data(Qt.UserRole)
                if sid:
                    try:
                        self.browser.scrollToAnchor(sid)

                    except Exception:
                        pass

            self.toc_list.itemClicked.connect(on_toc_clicked)

        except Exception as e:
            logger.error(f"Erro ao inicializar ManualDialog: {e}", exc_info=True)

    def _on_idioma_alterado(self, novo_idioma: str):
        try:
            self._current_lang = novo_idioma
            titulo = get_manual_title(novo_idioma)
            self.setWindowTitle(titulo)

            try:
                self._btn_ok.setText(self.tr('OK'))

            except Exception:
                pass

            self._build_manual_content(novo_idioma)

        except Exception:
            pass

    def _build_manual_content(self, lang: str | None):
        try:
            blocks, order = get_manual_blocks(lang)
            html_parts = []

            def render_block(b: 'ManualBlock'):
                if b.kind == 'toc_title':
                    html_parts.append(f"<h3>{b.text}</h3>")

                elif b.kind == 'toc_item':
                    html_parts.append(f"<p><a href=\"#{b.section_id}\">{b.text}</a></p>")

                elif b.kind == 'section_title':
                    html_parts.append(f"<h2 id=\"{b.section_id}\">{b.text}</h2>")

                elif b.kind == 'detail_title':
                    html_parts.append(f"<h4>{b.text}</h4>")

                elif b.kind == 'paragraph' or b.kind == 'line':
                    html_parts.append(f"<p>{b.text}</p>")

                elif b.kind == 'bullet':
                    html_parts.append(f"<li>{b.text}</li>")

                elif b.kind == 'divider':
                    html_parts.append(f"<hr />")

                elif b.kind == 'blank':
                    html_parts.append("")

            self.toc_list.clear()
            for b in blocks:
                if b.kind == 'toc_item' and b.section_id:
                    item = QListWidgetItem(b.text)
                    item.setData(Qt.UserRole, b.section_id)
                    self.toc_list.addItem(item)

            for b in blocks:
                if b.kind == 'bullet':
                    html_parts.append(f"<ul><li>{b.text}</li></ul>")

                else:
                    render_block(b)

            html = "\n".join(html_parts)
            self.browser.setHtml(html)

        except Exception:
            pass

def _exibir_manual(self):
    try:
        lang = getattr(self.loc, 'idioma_atual', 'pt_BR') if hasattr(self, 'loc') else 'pt_BR'
        titulo = get_manual_title(lang)
        dialog = ManualDialog(None, titulo, lang=lang)

        try:
            dialog._parent = self.interface
            dialog._loc = getattr(self, 'loc', None)
            if getattr(self, 'loc', None) is not None and hasattr(self.loc, 'idioma_alterado') and hasattr(dialog, '_on_idioma_alterado'):
                self.loc.idioma_alterado.connect(dialog._on_idioma_alterado)

        except Exception:
            pass

        self.interface._manual_dialog = dialog
        self.interface._manual_dialog.show()

    except Exception as e:
        logger.error(f"Erro ao exibir manual: {e}", exc_info=True)

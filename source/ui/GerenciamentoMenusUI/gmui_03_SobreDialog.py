from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSizePolicy, QHBoxLayout, QWidget, QTabWidget
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class SobreDialog(QDialog):
    def __init__(self, parent, titulo, texto_fixo, texto_history, detalhes, licencas, sites_licencas, 
                 show_history_text, hide_history_text, 
                 show_details_text, hide_details_text, 
                 show_licenses_text, hide_licenses_text, 
                 ok_text, site_oficial_text, avisos=None, 
                 show_notices_text=None, hide_notices_text=None, 
                 Privacy_Policy=None, 
                 show_privacy_policy_text=None, hide_privacy_policy_text=None, 
                 info_not_available_text="Information not available", release_notes=None, 
                 show_release_notes_text=None, hide_release_notes_text=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(titulo)
            self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
            self.setModal(False)

            layout = QVBoxLayout(self)

            header_widget = QWidget()
            header_layout = QVBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(5)

            self.fixed_label = QLabel(texto_fixo)
            self.fixed_label.setTextFormat(Qt.TextFormat.RichText)
            self.fixed_label.setWordWrap(True)
            self.fixed_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.fixed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            header_layout.addWidget(self.fixed_label)

            header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(header_widget)

            self.tabs = QTabWidget()
            self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self._tab_labels = []

            # Aba: History
            history_browser = QTextBrowser()
            history_browser.setReadOnly(True)
            history_browser.setOpenExternalLinks(True)
            if texto_history:
                history_browser.setPlainText(texto_history)

            else:
                history_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(history_browser, show_history_text or "Show")
            self._tab_labels.append((show_history_text or "Show", hide_history_text or "Hide"))

            # Aba: Details
            detalhes_browser = QTextBrowser()
            detalhes_browser.setReadOnly(True)
            detalhes_browser.setOpenExternalLinks(True)
            if detalhes:
                detalhes_browser.setPlainText(detalhes)

            else:
                detalhes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(detalhes_browser, show_details_text or "Show")
            self._tab_labels.append((show_details_text or "Show", hide_details_text or "Hide"))

            # Aba: Licenses
            licencas_browser = QTextBrowser()
            licencas_browser.setReadOnly(True)
            licencas_browser.setOpenExternalLinks(True)
            if licencas:
                texto_html = licencas.replace('\n', '<br>')
                texto_html += f"<br><br><h3>{site_oficial_text}</h3><ul>"
                for site in (sites_licencas or "").strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'

                texto_html += "</ul>"
                licencas_browser.setHtml(texto_html)

            else:
                licencas_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(licencas_browser, show_licenses_text or "Show")
            self._tab_labels.append((show_licenses_text or "Show", hide_licenses_text or "Hide"))

            # Aba: Notices
            avisos_browser = QTextBrowser()
            avisos_browser.setReadOnly(True)
            avisos_browser.setOpenExternalLinks(True)
            if avisos:
                avisos_browser.setPlainText(avisos)

            else:
                avisos_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(avisos_browser, show_notices_text or "Show")
            self._tab_labels.append((show_notices_text or "Show", hide_notices_text or "Hide"))

            # Aba: Privacy Policy
            privacidade_browser = QTextBrowser()
            privacidade_browser.setReadOnly(True)
            privacidade_browser.setOpenExternalLinks(True)
            if Privacy_Policy:
                privacidade_browser.setPlainText(Privacy_Policy)

            else:
                privacidade_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(privacidade_browser, show_privacy_policy_text or "Show")
            self._tab_labels.append((show_privacy_policy_text or "Show", hide_privacy_policy_text or "Hide"))

            # Aba: Release Notes
            release_notes_browser = QTextBrowser()
            release_notes_browser.setReadOnly(True)
            release_notes_browser.setOpenExternalLinks(True)
            if release_notes:
                release_notes_browser.setPlainText(release_notes)

            else:
                release_notes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            idx = self.tabs.addTab(release_notes_browser, (show_release_notes_text or "Show"))
            self._tab_labels.append((show_release_notes_text or "Show", hide_release_notes_text or "Hide"))

            layout.addWidget(self.tabs)

            button_layout = QHBoxLayout()
            self.ok_button = QPushButton(ok_text)
            self.ok_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.ok_button.clicked.connect(self.accept)
            button_layout.addStretch(1)
            button_layout.addWidget(self.ok_button)
            layout.addLayout(button_layout)

            self.setMinimumSize(400, 200)

            self.tabs.currentChanged.connect(self._update_tab_labels)
            self._update_tab_labels(self.tabs.currentIndex())

        except Exception as e:
            logger.error(f"Erro ao criar dialog sobre: {e}", exc_info=True)

    def _update_tab_labels(self, current_index: int):
        try:
            for i in range(self.tabs.count()):
                show_text, hide_text = self._tab_labels[i] if i < len(self._tab_labels) else ("Show", "Hide")
                self.tabs.setTabText(i, hide_text if i == current_index else show_text)

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos das abas: {e}", exc_info=True)

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
            self._history_browser = history_browser

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
            self._detalhes_browser = detalhes_browser

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
            self._licencas_browser = licencas_browser
            self._sites_licencas = sites_licencas

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
            self._avisos_browser = avisos_browser

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
            self._privacidade_browser = privacidade_browser

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
            self._release_notes_browser = release_notes_browser

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

            self._parent = parent
            self._loc = getattr(parent, 'loc', None)

            try:
                if self._loc is not None and hasattr(self._loc, 'idioma_alterado'):
                    self._loc.idioma_alterado.connect(self._on_idioma_alterado)

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao criar dialog sobre: {e}", exc_info=True)

    def _on_idioma_alterado(self, novo_idioma: str | None = None):
        try:
            try:
                from source.ui.ui_14_OpcoesSobre import (
                    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US, LICENSE_TEXT_ES_ES,
                    LICENSE_TEXT_FR_FR, LICENSE_TEXT_IT_IT, LICENSE_TEXT_DE_DE,
                    NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US, NOTICE_TEXT_ES_ES,
                    NOTICE_TEXT_FR_FR, NOTICE_TEXT_IT_IT, NOTICE_TEXT_DE_DE,
                    ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US, ABOUT_TEXT_ES_ES,
                    ABOUT_TEXT_FR_FR, ABOUT_TEXT_IT_IT, ABOUT_TEXT_DE_DE,
                    Privacy_Policy_pt_BR, Privacy_Policy_en_US,
                    Privacy_Policy_es_ES, Privacy_Policy_fr_FR,
                    Privacy_Policy_it_IT, Privacy_Policy_de_DE,
                    History_APP_pt_BR, History_APP_en_US, History_APP_es_ES,
                    History_APP_fr_FR, History_APP_it_IT, History_APP_de_DE,
                    RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US, RELEASE_NOTES_es_ES,
                    RELEASE_NOTES_fr_FR, RELEASE_NOTES_it_IT, RELEASE_NOTES_de_DE
                )

                textos_sobre = {
                    "pt_BR": ABOUT_TEXT_PT_BR,
                    "en_US": ABOUT_TEXT_EN_US,
                    "es_ES": ABOUT_TEXT_ES_ES,
                    "fr_FR": ABOUT_TEXT_FR_FR,
                    "it_IT": ABOUT_TEXT_IT_IT,
                    "de_DE": ABOUT_TEXT_DE_DE
                }
                textos_licenca = {
                    "pt_BR": LICENSE_TEXT_PT_BR,
                    "en_US": LICENSE_TEXT_EN_US,
                    "es_ES": LICENSE_TEXT_ES_ES,
                    "fr_FR": LICENSE_TEXT_FR_FR,
                    "it_IT": LICENSE_TEXT_IT_IT,
                    "de_DE": LICENSE_TEXT_DE_DE
                }
                textos_aviso = {
                    "pt_BR": NOTICE_TEXT_PT_BR,
                    "en_US": NOTICE_TEXT_EN_US,
                    "es_ES": NOTICE_TEXT_ES_ES,
                    "fr_FR": NOTICE_TEXT_FR_FR,
                    "it_IT": NOTICE_TEXT_IT_IT,
                    "de_DE": NOTICE_TEXT_DE_DE
                }
                textos_privacidade = {
                    "pt_BR": Privacy_Policy_pt_BR,
                    "en_US": Privacy_Policy_en_US,
                    "es_ES": Privacy_Policy_es_ES,
                    "fr_FR": Privacy_Policy_fr_FR,
                    "it_IT": Privacy_Policy_it_IT,
                    "de_DE": Privacy_Policy_de_DE
                }
                history_texts = {
                    "pt_BR": History_APP_pt_BR,
                    "en_US": History_APP_en_US,
                    "es_ES": History_APP_es_ES,
                    "fr_FR": History_APP_fr_FR,
                    "it_IT": History_APP_it_IT,
                    "de_DE": History_APP_de_DE
                }
                release_notes_texts = {
                    "pt_BR": RELEASE_NOTES_pt_BR,
                    "en_US": RELEASE_NOTES_en_US,
                    "es_ES": RELEASE_NOTES_es_ES,
                    "fr_FR": RELEASE_NOTES_fr_FR,
                    "it_IT": RELEASE_NOTES_it_IT,
                    "de_DE": RELEASE_NOTES_de_DE
                }

            except Exception:
                textos_sobre = textos_licenca = textos_aviso = textos_privacidade = {}
                history_texts = release_notes_texts = {}

            loc = getattr(self, '_loc', None) or (getattr(self, '_parent', None).loc if getattr(self, '_parent', None) is not None else None)
            idioma = None

            try:
                idioma = loc.idioma_atual

            except Exception:
                idioma = novo_idioma or 'en_US'

            try:
                cabecalho_fixo = (
                    f"<h3>LINCEU LIGHTHOUSE</h3>"
                    f"<p><b>{loc.get_text('version')}:</b> 0.1.3.0</p>"
                    f"<p><b>{loc.get_text('authors')}:</b> Fernando Nillsson Cidade</p>"
                    f"<p><b>{loc.get_text('description')}:</b> {loc.get_text('description_text')}</p>"
                )
                self.fixed_label.setText(cabecalho_fixo)

                try:
                    self.setWindowTitle(f"{loc.get_text('about')} - LINCEU LIGHTHOUSE")

                except Exception:
                    pass

            except Exception:
                pass

            try:
                texto_history = history_texts.get(idioma, history_texts.get('en_US', ''))
                self._history_browser.setPlainText(texto_history or '')

            except Exception:
                pass

            try:
                texto_detalhes = textos_sobre.get(idioma, textos_sobre.get('en_US', ''))
                self._detalhes_browser.setPlainText(texto_detalhes or '')

            except Exception:
                pass

            try:
                texto_licenca = textos_licenca.get(idioma, textos_licenca.get('en_US', ''))
                texto_html = (texto_licenca or '').replace('\n', '<br>')
                texto_html += f"<br><br><h3>{loc.get_text('site_oficial')}</h3><ul>"
                for site in (getattr(self, '_sites_licencas', '') or '').strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'

                texto_html += "</ul>"
                self._licencas_browser.setHtml(texto_html)

            except Exception:
                pass

            try:
                texto_aviso = textos_aviso.get(idioma, textos_aviso.get('en_US', ''))
                self._avisos_browser.setPlainText(texto_aviso or '')

            except Exception:
                pass

            try:
                texto_priv = textos_privacidade.get(idioma, textos_privacidade.get('en_US', ''))
                self._privacidade_browser.setPlainText(texto_priv or '')

            except Exception:
                pass

            try:
                texto_release = release_notes_texts.get(idioma, release_notes_texts.get('en_US', ''))
                self._release_notes_browser.setPlainText(texto_release or '')

            except Exception:
                pass

            try:
                labels = [
                    (loc.get_text('show_history'), loc.get_text('hide_history')),
                    (loc.get_text('show_details'), loc.get_text('hide_details')),
                    (loc.get_text('show_licenses'), loc.get_text('hide_licenses')),
                    (loc.get_text('show_notices'), loc.get_text('hide_notices')),
                    (loc.get_text('show_privacy_policy'), loc.get_text('hide_privacy_policy')),
                    (loc.get_text('show_release_notes'), loc.get_text('hide_release_notes')),
                ]

                for i, pair in enumerate(labels):
                    try:
                        show_t = pair[0] or self._tab_labels[i][0]
                        hide_t = pair[1] or self._tab_labels[i][1]
                        self._tab_labels[i] = (show_t, hide_t)

                    except Exception:
                        pass

                self._update_tab_labels(self.tabs.currentIndex())

            except Exception:
                pass

            try:
                self.ok_button.setText(loc.get_text('ok'))

            except Exception:
                try:
                    self.ok_button.setText(self.tr('OK'))

                except Exception:
                    pass

        except Exception as e:
            logger.error(f"Erro ao aplicar tradução dinâmica no diálogo Sobre: {e}", exc_info=True)

    def _update_tab_labels(self, current_index: int):
        try:
            for i in range(self.tabs.count()):
                show_text, hide_text = self._tab_labels[i] if i < len(self._tab_labels) else ("Show", "Hide")
                self.tabs.setTabText(i, hide_text if i == current_index else show_text)

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos das abas: {e}", exc_info=True)

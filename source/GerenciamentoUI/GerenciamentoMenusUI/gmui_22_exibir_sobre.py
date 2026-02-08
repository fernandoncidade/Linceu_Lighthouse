from PySide6.QtWidgets import QMessageBox
from source.GerenciamentoUI.GerenciamentoMenusUI.gmui_03_SobreDialog import SobreDialog
from source.GerenciamentoUI.ui_14_OpcoesSobre import (
    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US, LICENSE_TEXT_ES_ES,
    LICENSE_TEXT_FR_FR, LICENSE_TEXT_IT_IT, LICENSE_TEXT_DE_DE,
    SITE_LICENSES, NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US,
    NOTICE_TEXT_ES_ES, NOTICE_TEXT_FR_FR, NOTICE_TEXT_IT_IT,
    NOTICE_TEXT_DE_DE, ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US,
    ABOUT_TEXT_ES_ES, ABOUT_TEXT_FR_FR, ABOUT_TEXT_IT_IT,
    ABOUT_TEXT_DE_DE, Privacy_Policy_pt_BR, Privacy_Policy_en_US,
    Privacy_Policy_es_ES, Privacy_Policy_fr_FR, Privacy_Policy_it_IT,
    Privacy_Policy_de_DE, History_APP_pt_BR, History_APP_en_US,
    History_APP_es_ES, History_APP_fr_FR, History_APP_it_IT,
    History_APP_de_DE, RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US, RELEASE_NOTES_es_ES,
    RELEASE_NOTES_fr_FR, RELEASE_NOTES_it_IT, RELEASE_NOTES_de_DE
)
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _exibir_sobre(self):
    try:
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
        texto_sobre = textos_sobre.get(self.loc.idioma_atual, textos_sobre["en_US"])
        texto_licenca = textos_licenca.get(self.loc.idioma_atual, textos_licenca["en_US"])
        texto_aviso = textos_aviso.get(self.loc.idioma_atual, textos_aviso["en_US"])
        texto_privacidade = textos_privacidade.get(self.loc.idioma_atual, textos_privacidade["en_US"])
        texto_history = history_texts.get(self.loc.idioma_atual, history_texts["en_US"])
        texto_release_notes = release_notes_texts.get(self.loc.idioma_atual, release_notes_texts["en_US"])
        cabecalho_fixo = (
            "<h3>LINCEU LIGHTHOUSE</h3>"
            f"<p><b>{self.loc.get_text('version')}:</b> 0.0.7.0</p>"
            f"<p><b>{self.loc.get_text('authors')}:</b> Fernando Nillsson Cidade</p>"
            f"<p><b>{self.loc.get_text('description')}:</b> {self.loc.get_text('description_text')}</p>"
        )
        show_history_text = self.loc.get_text("show_history") or "Justificativa do Nome"
        dialog = SobreDialog(
            self.interface,
            titulo=f"{self.loc.get_text('about')} - LINCEU LIGHTHOUSE",
            texto_fixo=cabecalho_fixo,
            texto_history=texto_history,
            detalhes=texto_sobre,
            licencas=texto_licenca,
            sites_licencas=SITE_LICENSES,
            show_history_text=show_history_text,
            show_details_text=self.loc.get_text("show_details"),
            hide_details_text=self.loc.get_text("hide_details"),
            show_licenses_text=self.loc.get_text("show_licenses"),
            hide_licenses_text=self.loc.get_text("hide_licenses"),
            ok_text=self.loc.get_text("ok"),
            site_oficial_text=self.loc.get_text("site_oficial"),
            avisos=texto_aviso,
            show_notices_text=self.loc.get_text("show_notices"),
            hide_notices_text=self.loc.get_text("hide_notices"),
            Privacy_Policy=texto_privacidade,
            show_privacy_policy_text=self.loc.get_text("show_privacy_policy"),
            hide_privacy_policy_text=self.loc.get_text("hide_privacy_policy"),
            info_not_available_text=self.loc.get_text("information_not_available"),
            release_notes=texto_release_notes,
            show_release_notes_text=self.loc.get_text("show_release_notes") or "Release Notes"
        )
        tamanho_base_largura = 900
        tamanho_base_altura = 500
        largura_dialog = int(tamanho_base_largura * 1)
        altura_dialog = int(tamanho_base_altura * 1.8)
        dialog.resize(largura_dialog, altura_dialog)
        dialog.show()

    except Exception as e:
        logger.error(f"Erro ao exibir o diálogo 'Sobre': {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

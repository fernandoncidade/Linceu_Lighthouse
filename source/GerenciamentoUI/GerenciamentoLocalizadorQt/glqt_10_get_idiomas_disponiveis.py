from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_idiomas_disponiveis(self):
    try:
        if self.idioma_atual == "pt_BR":
            return {
                "pt_BR": "Português Brasileiro | Brazilian Portuguese",
                "en_US": "Inglês (EUA) | English (US)",
                "es_ES": "Espanhol | Español",
                "fr_FR": "Francês | Français",
                "it_IT": "Italiano | Italiano",
                "de_DE": "Alemão | Deutsch"
            }

        elif self.idioma_atual == "en_US":
            return {
                "pt_BR": "Brazilian Portuguese | Português Brasileiro",
                "en_US": "English (US) | Inglês (US)",
                "es_ES": "Spanish | Español",
                "fr_FR": "French | Français",
                "it_IT": "Italian | Italiano",
                "de_DE": "German | Deutsch"
            }

        elif self.idioma_atual == "es_ES":
            return {
                "pt_BR": "Portugués Brasileño | Português Brasileiro",
                "en_US": "Inglés (EEUU) | English (US)",
                "es_ES": "Español | Spanish",
                "fr_FR": "Francés | Français",
                "it_IT": "Italiano | Italiano",
                "de_DE": "Alemán | Deutsch"
            }

        elif self.idioma_atual == "fr_FR":
            return {
                "pt_BR": "Portugais Brésilien | Português Brasileiro",
                "en_US": "Anglais (États-Unis) | English (US)",
                "es_ES": "Espagnol | Español",
                "fr_FR": "Français | French",
                "it_IT": "Italien | Italiano",
                "de_DE": "Allemand | Deutsch"
            }

        elif self.idioma_atual == "it_IT":
            return {
                "pt_BR": "Portoghese Brasiliano | Português Brasileiro",
                "en_US": "Inglese (Stati Uniti) | English (US)",
                "es_ES": "Spagnolo | Español",
                "fr_FR": "Francese | Français",
                "it_IT": "Italiano | Italian",
                "de_DE": "Tedesco | Deutsch"
            }

        elif self.idioma_atual == "de_DE":
            return {
                "pt_BR": "Brasilianisches Portugiesisch | Português Brasileiro",
                "en_US": "Englisch (USA) | English (US)",
                "es_ES": "Spanisch | Español",
                "fr_FR": "Französisch | Français",
                "it_IT": "Italienisch | Italiano",
                "de_DE": "Deutsch | German"
            }

        else:
            return self.idiomas_suportados.copy()

    except Exception as e:
        logger.error(f"Erro ao obter idiomas disponíveis: {e}", exc_info=True)

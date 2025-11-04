from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_dialogo_cores(self, dialogo):
    try:
        from PySide6.QtWidgets import QLabel, QPushButton, QGroupBox

        mapeamento_traducoes = {
            "Basic colors": self.loc.get_text("basic_colors"),
            "&Basic colors": self.loc.get_text("basic_colors"),
            "Custom colors": self.loc.get_text("custom_colors"),
            "&Custom colors": self.loc.get_text("custom_colors"),
            "Pick Screen Color": self.loc.get_text("pick_screen_color"),
            "&Pick Screen Color": self.loc.get_text("pick_screen_color"),
            "Add to Custom Colors": self.loc.get_text("add_to_custom_colors"),
            "&Add to Custom Colors": self.loc.get_text("add_to_custom_colors"),
            "Hue:": f"{self.loc.get_text('hue')}",
            "&Hue:": f"{self.loc.get_text('hue')}",
            "Hue": self.loc.get_text("hue"),
            "&Hue": self.loc.get_text("hue"),
            "Sat:": f"{self.loc.get_text('sat')}",
            "&Sat:": f"{self.loc.get_text('sat')}",
            "Sat": self.loc.get_text("sat"),
            "&Sat": self.loc.get_text("sat"),
            "Val:": f"{self.loc.get_text('val')}",
            "&Val:": f"{self.loc.get_text('val')}",
            "Val": self.loc.get_text("val"),
            "&Val": self.loc.get_text("val"),
            "Red:": f"{self.loc.get_text('red')}",
            "&Red:": f"{self.loc.get_text('red')}",
            "Red": self.loc.get_text("red"),
            "&Red": self.loc.get_text("red"),
            "Green:": f"{self.loc.get_text('green')}",
            "&Green:": f"{self.loc.get_text('green')}",
            "Green": self.loc.get_text("green"),
            "&Green": self.loc.get_text("green"),
            "Blue:": f"{self.loc.get_text('blue')}",
            "&Blue:": f"{self.loc.get_text('blue')}",
            "Blue": self.loc.get_text("blue"),
            "&Blue": self.loc.get_text("blue"),
            "HTML:": f"{self.loc.get_text('html')}",
            "&HTML:": f"{self.loc.get_text('html')}",
            "HTML": self.loc.get_text("html"),
            "&HTML": self.loc.get_text("html"),
            "OK": self.loc.get_text("ok"),
            "&OK": self.loc.get_text("ok"),
            "Cancel": self.loc.get_text("cancel"),
            "&Cancel": self.loc.get_text("cancel")
        }

        def normalizar(texto):
            return texto.strip().replace(":", "").replace("&", "")

        for label in dialogo.findChildren(QLabel):
            texto_original = label.text().strip()
            texto_norm = normalizar(texto_original)
            for chave, traducao in mapeamento_traducoes.items():
                if normalizar(chave) == texto_norm:
                    label.setText(traducao if ":" not in texto_original else f"{traducao}:")
                    break

        for button in dialogo.findChildren(QPushButton):
            texto_original = button.text().strip()
            texto_norm = normalizar(texto_original)
            for chave, traducao in mapeamento_traducoes.items():
                if normalizar(chave) == texto_norm:
                    button.setText(traducao)
                    break

        for groupbox in dialogo.findChildren(QGroupBox):
            texto_original = groupbox.title().strip()
            texto_norm = normalizar(texto_original)
            for chave, traducao in mapeamento_traducoes.items():
                if normalizar(chave) == texto_norm:
                    groupbox.setTitle(traducao)
                    break

        elementos_por_nome = {
            "qt_colorname_label": self.loc.get_text("html"),
        }

        for nome, traducao in elementos_por_nome.items():
            elemento = dialogo.findChild(QLabel, nome)
            if elemento:
                elemento.setText(f"{traducao}:")

    except Exception as e:
        logger.error(f"Erro ao traduzir diálogo de cores: {e}", exc_info=True)

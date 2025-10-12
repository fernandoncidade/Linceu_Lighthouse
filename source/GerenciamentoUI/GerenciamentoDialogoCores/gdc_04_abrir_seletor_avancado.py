from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import Qt
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _abrir_seletor_avancado(self):
    try:
        from PySide6.QtCore import QLocale, QTranslator
        from PySide6.QtWidgets import QApplication
        import os

        app = QApplication.instance()
        if app:
            locale_map = {
                "pt_BR": "pt_BR",
                "en_US": "en_US", 
                "es_ES": "es_ES",
                "fr_FR": "fr_FR",
                "it_IT": "it_IT",
                "de_DE": "de_DE"
            }

            translations_paths = [
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations", "qt"),
                "/usr/share/qt6/translations",
                "C:/Qt/Tools/QtCreator/share/qtcreator/translations",
            ]

            def aplicar_qt_translator(locale_code):
                try:
                    qt_locale = QLocale(locale_code)
                    QLocale.setDefault(qt_locale)
                    try:
                        if hasattr(self, "_qt_translator") and self._qt_translator is not None:
                            app.removeTranslator(self._qt_translator)

                    except Exception:
                        pass

                    novo_trans = QTranslator()
                    carregado = False
                    for path in translations_paths:
                        try:
                            if os.path.exists(path):
                                if novo_trans.load(qt_locale, "qtbase", "_", path):
                                    carregado = True
                                    break

                        except Exception:
                            continue

                    if carregado:
                        app.installTranslator(novo_trans)
                        self._qt_translator = novo_trans

                    else:
                        self._qt_translator = None

                except Exception as e:
                    logger.error(f"Erro ao aplicar tradutor Qt para locale {locale_code}: {e}", exc_info=True)

            locale_code = locale_map.get(self.loc.idioma_atual, "en_US")
            aplicar_qt_translator(locale_code)

        dialogo = QColorDialog(self.cor_atual, self)
        dialogo.setOption(QColorDialog.DontUseNativeDialog, True)
        dialogo.setOption(QColorDialog.ShowAlphaChannel, False)
        dialogo.setWindowTitle(self.loc.get_text("advanced_color_picker"))
        dialogo.setModal(False)
        dialogo.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

        self._dialogo_avancado = dialogo

        app.processEvents()

        try:
            self._traduzir_dialogo_cores(dialogo)

        except Exception:
            pass

        try:
            if hasattr(self.loc, "traducoes_carregadas"):
                def _on_traducoes_carregadas():
                    try:
                        locale_code = locale_map.get(self.loc.idioma_atual, "en_US")
                        aplicar_qt_translator(locale_code)
                        self._traduzir_dialogo_cores(dialogo)
                        try:
                            dialogo.setWindowTitle(self.loc.get_text("advanced_color_picker"))

                        except Exception:
                            pass

                    except Exception as e:
                        logger.error(f"Erro no handler de traduções do seletor avançado: {e}", exc_info=True)

                self._on_traducoes_carregadas_qcolor = _on_traducoes_carregadas
                self.loc.traducoes_carregadas.connect(self._on_traducoes_carregadas_qcolor)

        except Exception as e:
            logger.error(f"Não foi possível conectar sinal de traduções ao seletor avançado: {e}", exc_info=True)

        def cleanup_dialog_translator():
            try:
                try:
                    if hasattr(self, "_on_traducoes_carregadas_qcolor") and hasattr(self.loc, "traducoes_carregadas"):
                        self.loc.traducoes_carregadas.disconnect(self._on_traducoes_carregadas_qcolor)

                except Exception:
                    pass

                try:
                    if hasattr(self, "_qt_translator") and self._qt_translator is not None:
                        app.removeTranslator(self._qt_translator)
                        self._qt_translator = None

                except Exception:
                    pass

            except Exception as e:
                logger.error(f"Erro ao limpar tradutor do seletor avançado: {e}", exc_info=True)

        if app:
            try:
                dialogo.finished.connect(lambda code: cleanup_dialog_translator())
                dialogo.destroyed.connect(lambda obj=None: cleanup_dialog_translator())

            except Exception:
                pass

        if self.loc.idioma_atual != "en_US":
            from PySide6.QtCore import QTimer
            self._traducao_timer = QTimer()
            QTimer.singleShot(50, lambda: self._traduzir_dialogo_cores(dialogo))
            self._traduzir_dialogo_cores(dialogo)

        def on_color_selected(color):
            if color.isValid():
                self.preview_nova.setStyleSheet(f"background-color: {color.name()};")
                self.cor_selecionada = color
                try:
                    dialogo.close()

                except Exception as e:
                    logger.error(f"Erro ao fechar diálogo de cor: {e}", exc_info=True)

        dialogo.colorSelected.connect(on_color_selected)
        dialogo.show()
        try:
            dialogo.raise_()
            dialogo.activateWindow()

        except Exception as e:
            logger.error(f"Erro ao ativar janela do seletor de cor: {e}", exc_info=True)

        from PySide6.QtCore import QTimer
        def _checar_visibilidade():
            try:
                if not dialogo.isVisible():
                    dialogo.exec()

            except Exception as e:
                logger.error(f"Erro no fallback de exibição do seletor: {e}", exc_info=True)

        QTimer.singleShot(150, _checar_visibilidade)

    except Exception as e:
        logger.error(f"Erro ao abrir seletor avançado de cores: {e}", exc_info=True)

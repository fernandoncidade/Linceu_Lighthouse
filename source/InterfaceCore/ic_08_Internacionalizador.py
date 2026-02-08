import os
from PySide6.QtCore import QLocale
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class Internacionalizador:
    @staticmethod
    def inicializar_sistema_traducao(app, idioma_inicial="pt_BR"):
        try:
            locale = QLocale(idioma_inicial)
            QLocale.setDefault(locale)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            locale_dir = os.path.join(base_dir, "locale")
            if not os.path.exists(locale_dir):
                os.makedirs(locale_dir, exist_ok=True)

            return True

        except Exception as e:
            logger.error(f"Erro ao inicializar sistema de tradução: {e}", exc_info=True)
            return False

    @staticmethod
    def atualizar_tradutor_qt(interface, idioma):
        try:
            if hasattr(interface, 'loc') and hasattr(interface.loc, 'set_idioma'):
                interface.loc.set_idioma(idioma)

        except Exception as e:
            logger.error(f"Erro ao atualizar tradutor Qt: {e}", exc_info=True)

    @staticmethod
    def inicializar_tradutor_qt(app, idioma):
        try:
            return Internacionalizador.inicializar_sistema_traducao(app, idioma)

        except Exception as e:
            logger.error(f"Erro ao inicializar tradutor Qt: {e}", exc_info=True)
            return False

    @staticmethod
    def extrair_strings_para_traducao():
        try:
            import subprocess
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            locale_dir = os.path.join(base_dir, "locale")
            pro_file = os.path.join(locale_dir, "linceu.pro")
            if os.path.exists(pro_file):
                result = subprocess.run(
                    ["lupdate", pro_file], 
                    cwd=locale_dir,
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    logger.error(f"lupdate retornou código {result.returncode}: {result.stderr}")

            else:
                logger.error(f"Arquivo .pro não encontrado: {pro_file}")

        except FileNotFoundError:
            logger.error("lupdate não encontrado. Instale o Qt Linguist Tools", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao extrair strings: {e}", exc_info=True)

    @staticmethod 
    def compilar_traducoes():
        try:
            import subprocess
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            locale_dir = os.path.join(base_dir, "locale")
            ts_files = [f for f in os.listdir(locale_dir) if f.endswith('.ts')]
            for ts_file in ts_files:
                ts_path = os.path.join(locale_dir, ts_file)
                qm_file = ts_file.replace('.ts', '.qm')
                qm_path = os.path.join(locale_dir, qm_file)
                result = subprocess.run(
                    ["lrelease", ts_path, "-qm", qm_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    logger.error(f"Erro ao compilar {ts_file}: {result.stderr}")

        except FileNotFoundError:
            logger.error("lrelease não encontrado. Instale o Qt Linguist Tools", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao compilar traduções: {e}", exc_info=True)

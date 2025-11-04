import os
from PySide6.QtCore import QLocale
from utils.LogManager import LogManager


class Internacionalizador:
    @staticmethod
    def inicializar_sistema_traducao(app, idioma_inicial="pt_BR"):
        logger = LogManager.get_logger()
        try:
            logger.info(f"Inicializando sistema de tradução para {idioma_inicial}")
            locale = QLocale(idioma_inicial)
            QLocale.setDefault(locale)
            translations_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "translations"
            )
            if not os.path.exists(translations_dir):
                os.makedirs(translations_dir, exist_ok=True)
                logger.info(f"Diretório de traduções criado: {translations_dir}")

            logger.info(f"Sistema de tradução inicializado para {idioma_inicial}")
            return True

        except Exception as e:
            logger.error(f"Erro ao inicializar sistema de tradução: {e}", exc_info=True)
            return False

    @staticmethod
    def atualizar_tradutor_qt(interface, idioma):
        logger = LogManager.get_logger()
        logger.info(f"Redirecionando atualização de tradutor Qt para LocalizadorQt: {idioma}")
        if hasattr(interface, 'loc') and hasattr(interface.loc, 'set_idioma'):
            interface.loc.set_idioma(idioma)

    @staticmethod
    def inicializar_tradutor_qt(app, idioma):
        logger = LogManager.get_logger()
        logger.info(f"Inicializando tradutor Qt via sistema nativo: {idioma}")
        return Internacionalizador.inicializar_sistema_traducao(app, idioma)

    @staticmethod
    def extrair_strings_para_traducao():
        logger = LogManager.get_logger()
        try:
            import subprocess
            translations_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "translations"
            )
            pro_file = os.path.join(translations_dir, "linceu.pro")
            if os.path.exists(pro_file):
                result = subprocess.run(
                    ["lupdate", pro_file], 
                    cwd=translations_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info("Strings extraídas com sucesso usando lupdate")

                else:
                    logger.warning(f"lupdate retornou código {result.returncode}: {result.stderr}")

            else:
                logger.warning(f"Arquivo .pro não encontrado: {pro_file}")

        except FileNotFoundError:
            logger.warning("lupdate não encontrado. Instale o Qt Linguist Tools")

        except Exception as e:
            logger.error(f"Erro ao extrair strings: {e}", exc_info=True)

    @staticmethod 
    def compilar_traducoes():
        logger = LogManager.get_logger()
        try:
            import subprocess
            translations_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "translations"
            )
            ts_files = [f for f in os.listdir(translations_dir) if f.endswith('.ts')]
            for ts_file in ts_files:
                ts_path = os.path.join(translations_dir, ts_file)
                qm_file = ts_file.replace('.ts', '.qm')
                qm_path = os.path.join(translations_dir, qm_file)
                result = subprocess.run(
                    ["lrelease", ts_path, "-qm", qm_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info(f"Tradução compilada: {qm_file}")

                else:
                    logger.warning(f"Erro ao compilar {ts_file}: {result.stderr}")

        except FileNotFoundError:
            logger.warning("lrelease não encontrado. Instale o Qt Linguist Tools")

        except Exception as e:
            logger.error(f"Erro ao compilar traduções: {e}", exc_info=True)

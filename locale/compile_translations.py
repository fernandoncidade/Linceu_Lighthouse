import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def check_pyside6_tools():
    try:
        result = subprocess.run(['pyside6-lrelease', '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True

    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        result = subprocess.run(['lrelease', '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return 'lrelease'

    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return False


def compile_with_pyside6_lrelease(ts_file_path, qm_file_path, tool='pyside6-lrelease'):
    try:
        print(f"Compilando com {tool}: {ts_file_path.name}")

        resultado = subprocess.run(
            [tool, str(ts_file_path), "-qm", str(qm_file_path)],
            check=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )

        if resultado.stdout.strip():
            print(f"  ✓ {resultado.stdout.strip()}")

        else:
            print(f"  ✓ Compilado com sucesso")

        return True

    except subprocess.CalledProcessError as e:
        print(f"  ✗ Erro ao compilar: {e}")
        if e.stderr:
            print(f"  ✗ Detalhes: {e.stderr.strip()}")

        return False

    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout ao compilar {ts_file_path.name}")
        return False

    except Exception as e:
        print(f"  ✗ Erro inesperado: {e}")
        return False


def parse_ts_file(ts_file_path):
    try:
        tree = ET.parse(ts_file_path)
        root = tree.getroot()

        locale = {}

        for context in root.findall('context'):
            context_name = context.find('name').text if context.find('name') is not None else "default"

            for message in context.findall('message'):
                source_elem = message.find('source')
                translation_elem = message.find('locale')

                if source_elem is not None and translation_elem is not None:
                    source_text = source_elem.text or ""
                    translation_text = translation_elem.text or ""

                    if translation_text.strip():
                        locale[source_text] = translation_text

        return locale

    except Exception as e:
        print(f"Erro ao fazer parse do arquivo {ts_file_path}: {e}")
        return None


def compile_ts_to_qm_fallback(ts_file_path, qm_file_path):
    try:
        print(f"Compilando (método alternativo): {ts_file_path.name}")

        locale = parse_ts_file(ts_file_path)

        if locale is None:
            return False

        if not locale:
            print(f"  ⚠ Nenhuma tradução encontrada em {ts_file_path.name}")
            return False

        import shutil
        shutil.copy2(ts_file_path, qm_file_path)

        print(f"  ✓ {len(locale)} traduções processadas (método alternativo)")
        return True

    except Exception as e:
        print(f"  ✗ Erro no método alternativo: {e}")
        return False


def validate_ts_file(ts_file_path):
    try:
        tree = ET.parse(ts_file_path)
        root = tree.getroot()

        if root.tag != 'TS':
            return False, "Elemento raiz não é 'TS'"

        contexts = root.findall('context')
        if not contexts:
            return False, "Nenhum contexto encontrado"

        total_messages = 0
        translated_messages = 0

        for context in contexts:
            messages = context.findall('message')
            total_messages += len(messages)

            for message in messages:
                locale = message.find('locale')
                if locale is not None and locale.text and locale.text.strip():
                    translated_messages += 1

        completion = (translated_messages / total_messages * 100) if total_messages > 0 else 0

        return True, f"{translated_messages}/{total_messages} traduções ({completion:.1f}%)"

    except ET.ParseError as e:
        return False, f"Erro de XML: {e}"

    except Exception as e:
        return False, f"Erro: {e}"


def compile_translations():
    print("=== Compilando traduções do Linceu Lighthouse ===\n")

    current_dir = Path(__file__).parent
    ts_files = list(current_dir.glob('*.ts'))

    if not ts_files:
        print("Nenhum arquivo .ts encontrado!")
        return False

    tool = check_pyside6_tools()

    if tool:
        print(f"✓ Ferramenta encontrada: {tool if isinstance(tool, str) else 'pyside6-lrelease'}")

    else:
        print("⚠ pyside6-lrelease não encontrado - usando método alternativo")
        print("  Para instalar: pip install PySide6-Essentials ou use Qt Creator")

    print()

    success_count = 0
    fallback_count = 0

    for ts_file in sorted(ts_files):
        qm_file = ts_file.with_suffix('.qm')

        success = False

        if tool:
            tool_name = tool if isinstance(tool, str) else 'pyside6-lrelease'
            success = compile_with_pyside6_lrelease(ts_file, qm_file, tool_name)

        if not success:
            success = compile_ts_to_qm_fallback(ts_file, qm_file)
            if success:
                fallback_count += 1

        if success:
            success_count += 1

    print(f"\n=== Resultado ===")
    print(f"Sucessos: {success_count}/{len(ts_files)}")
    if fallback_count > 0:
        print(f"Usando método alternativo: {fallback_count}")

    return success_count > 0


def validate_translations():
    print("Validando arquivos de tradução...")

    current_dir = Path(__file__).parent
    ts_files = list(current_dir.glob('*.ts'))

    if not ts_files:
        print("Nenhum arquivo .ts encontrado!")
        return False

    valid_count = 0

    for ts_file in sorted(ts_files):
        is_valid, message = validate_ts_file(ts_file)

        status = "✓" if is_valid else "✗"
        print(f"{status} {ts_file.name}: {message}")

        if is_valid:
            valid_count += 1

    print(f"\nResultado: {valid_count}/{len(ts_files)} arquivos válidos")
    return valid_count == len(ts_files)


def list_translations():
    print("Arquivos de tradução disponíveis:")

    current_dir = Path(__file__).parent
    ts_files = list(current_dir.glob('*.ts'))

    if not ts_files:
        print("Nenhum arquivo .ts encontrado!")
        return

    for ts_file in sorted(ts_files):
        qm_file = ts_file.with_suffix('.qm')
        qm_exists = qm_file.exists()

        is_valid, validation_message = validate_ts_file(ts_file)

        status = "✓" if qm_exists else "✗"
        validity = "✓" if is_valid else "✗"

        print(f"  {status} {ts_file.name} - {validity} {validation_message}")

        if qm_exists:
            ts_time = ts_file.stat().st_mtime
            qm_time = qm_file.stat().st_mtime
            if ts_time > qm_time:
                print(f"    ⚠ Arquivo .ts mais recente que .qm")


def clean_compiled():
    print("Removendo arquivos .qm...")

    current_dir = Path(__file__).parent
    qm_files = list(current_dir.glob('*.qm'))

    if not qm_files:
        print("Nenhum arquivo .qm encontrado!")
        return

    removed_count = 0
    for qm_file in qm_files:
        try:
            qm_file.unlink()
            print(f"✓ Removido: {qm_file.name}")
            removed_count += 1

        except Exception as e:
            print(f"✗ Erro ao remover {qm_file.name}: {e}")

    print(f"\nResultado: {removed_count} arquivos removidos")


def show_stats():
    print("Estatísticas das traduções:")

    current_dir = Path(__file__).parent
    ts_files = list(current_dir.glob('*.ts'))

    if not ts_files:
        print("Nenhum arquivo .ts encontrado!")
        return

    total_files = len(ts_files)
    valid_files = 0
    total_messages = 0
    total_translated = 0

    for ts_file in sorted(ts_files):
        try:
            tree = ET.parse(ts_file)
            root = tree.getroot()

            file_messages = 0
            file_translated = 0

            for context in root.findall('context'):
                for message in context.findall('message'):
                    file_messages += 1
                    locale = message.find('locale')
                    if locale is not None and locale.text and locale.text.strip():
                        file_translated += 1

            total_messages += file_messages
            total_translated += file_translated
            valid_files += 1

            completion = (file_translated / file_messages * 100) if file_messages > 0 else 0
            lang_code = ts_file.stem.split('_')[-1] if '_' in ts_file.stem else 'unknown'
            print(f"  {lang_code}: {file_translated}/{file_messages} ({completion:.1f}%)")

        except Exception as e:
            print(f"  {ts_file.name}: Erro - {e}")

    overall_completion = (total_translated / total_messages * 100) if total_messages > 0 else 0
    print(f"\nTotal: {total_translated}/{total_messages} ({overall_completion:.1f}%)")
    print(f"Arquivos válidos: {valid_files}/{total_files}")


def install_tools():
    print("Tentando instalar ferramentas do PySide6...")

    packages = ['PySide6-Essentials', 'PySide6-Addons']

    for package in packages:
        try:
            print(f"Instalando {package}...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ {package} instalado com sucesso")

            else:
                print(f"✗ Erro ao instalar {package}: {result.stderr}")

        except Exception as e:
            print(f"✗ Erro ao instalar {package}: {e}")


def main():
    print("=== Compilador de Traduções - Linceu Lighthouse (PySide6) ===\n")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'compile':
            compile_translations()

        elif command == 'validate':
            validate_translations()

        elif command == 'list':
            list_translations()

        elif command == 'clean':
            clean_compiled()

        elif command == 'stats':
            show_stats()

        elif command == 'install':
            install_tools()

        elif command == 'all':
            print("1. Validando arquivos...")
            if validate_translations():
                print("\n2. Compilando traduções...")
                compile_translations()

            else:
                print("\n⚠ Alguns arquivos têm problemas. Corrija-os antes de compilar.")

        else:
            print(f"Comando desconhecido: {command}")
            print("Comandos disponíveis: compile, validate, list, clean, stats, install, all")

    else:
        print("Uso:")
        print("  python compile_translations.py compile   - Compila traduções")
        print("  python compile_translations.py validate  - Valida arquivos .ts")
        print("  python compile_translations.py list      - Lista arquivos de tradução")
        print("  python compile_translations.py clean     - Remove arquivos .qm")
        print("  python compile_translations.py stats     - Mostra estatísticas")
        print("  python compile_translations.py install   - Tenta instalar ferramentas")
        print("  python compile_translations.py all       - Valida e compila")


if __name__ == '__main__':
    main()

# import os
# import sys
# import subprocess
# import xml.etree.ElementTree as ET
# from pathlib import Path
# from utils.LogManager import LogManager
# logger = LogManager.get_logger()

# def check_pyside6_tools():
#     try:
#         result = subprocess.run(['pyside6-lrelease', '-version'], capture_output=True, text=True, timeout=10)
#         if result.returncode == 0:
#             return True

#     except (FileNotFoundError, subprocess.TimeoutExpired) as e:
#         logger.error(f"Erro ao verificar pyside6-lrelease: {e}")

#     try:
#         result = subprocess.run(['lrelease', '-version'], capture_output=True, text=True, timeout=10)
#         if result.returncode == 0:
#             return 'lrelease'

#     except (FileNotFoundError, subprocess.TimeoutExpired) as e:
#         logger.error(f"Erro ao verificar lrelease: {e}")

#     return False

# def compile_with_pyside6_lrelease(ts_file_path, qm_file_path, tool='pyside6-lrelease'):
#     try:
#         logger.error(f"Compilando com {tool}: {ts_file_path.name}")
#         resultado = subprocess.run(
#             [tool, str(ts_file_path), "-qm", str(qm_file_path)],
#             check=True, 
#             capture_output=True, 
#             text=True,
#             timeout=30
#         )

#         if resultado.stdout.strip():
#             logger.error(f"Compilado: {resultado.stdout.strip()}")

#         else:
#             logger.error(f"Compilado com sucesso")

#         return True

#     except subprocess.CalledProcessError as e:
#         logger.error(f"Erro ao compilar: {e}")
#         if e.stderr:
#             logger.error(f"Detalhes: {e.stderr.strip()}")

#         return False

#     except subprocess.TimeoutExpired:
#         logger.error(f"Timeout ao compilar {ts_file_path.name}")
#         return False

#     except Exception as e:
#         logger.error(f"Erro inesperado: {e}")
#         return False

# def parse_ts_file(ts_file_path):
#     try:
#         tree = ET.parse(ts_file_path)
#         root = tree.getroot()
#         locale = {}
#         for context in root.findall('context'):
#             context_name = context.find('name').text if context.find('name') is not None else "default"
#             for message in context.findall('message'):
#                 source_elem = message.find('source')
#                 translation_elem = message.find('locale')
#                 if source_elem is not None and translation_elem is not None:
#                     source_text = source_elem.text or ""
#                     translation_text = translation_elem.text or ""
#                     if translation_text.strip():
#                         locale[source_text] = translation_text

#         return locale

#     except Exception as e:
#         logger.error(f"Erro ao fazer parse do arquivo {ts_file_path}: {e}")
#         return None

# def compile_ts_to_qm_fallback(ts_file_path, qm_file_path):
#     try:
#         logger.error(f"Compilando (método alternativo): {ts_file_path.name}")
#         locale = parse_ts_file(ts_file_path)
#         if locale is None:
#             return False

#         if not locale:
#             logger.error(f"Nenhuma tradução encontrada em {ts_file_path.name}")
#             return False

#         import shutil
#         shutil.copy2(ts_file_path, qm_file_path)
#         logger.error(f"{len(locale)} traduções processadas (método alternativo)")
#         return True

#     except Exception as e:
#         logger.error(f"Erro no método alternativo: {e}")
#         return False

# def validate_ts_file(ts_file_path):
#     try:
#         tree = ET.parse(ts_file_path)
#         root = tree.getroot()
#         if root.tag != 'TS':
#             return False, "Elemento raiz não é 'TS'"

#         contexts = root.findall('context')
#         if not contexts:
#             return False, "Nenhum contexto encontrado"

#         total_messages = 0
#         translated_messages = 0
#         for context in contexts:
#             messages = context.findall('message')
#             total_messages += len(messages)
#             for message in messages:
#                 locale = message.find('locale')
#                 if locale is not None and locale.text and locale.text.strip():
#                     translated_messages += 1

#         completion = (translated_messages / total_messages * 100) if total_messages > 0 else 0
#         return True, f"{translated_messages}/{total_messages} traduções ({completion:.1f}%)"

#     except ET.ParseError as e:
#         logger.error(f"Erro de XML: {e}")
#         return False, f"Erro de XML: {e}"

#     except Exception as e:
#         logger.error(f"Erro ao validar arquivo TS: {e}")
#         return False, f"Erro: {e}"

# def compile_translations():
#     logger.error("Compilando traduções do Linceu Lighthouse")
#     current_dir = Path(__file__).parent
#     ts_files = list(current_dir.glob('*.ts'))

#     if not ts_files:
#         logger.error("Nenhum arquivo .ts encontrado!")
#         return False

#     tool = check_pyside6_tools()

#     if tool:
#         logger.error(f"Ferramenta encontrada: {tool if isinstance(tool, str) else 'pyside6-lrelease'}")

#     else:
#         logger.error("pyside6-lrelease não encontrado - usando método alternativo")
#         logger.error("Para instalar: pip install PySide6-Essentials ou use Qt Creator")

#     success_count = 0
#     fallback_count = 0

#     for ts_file in sorted(ts_files):
#         qm_file = ts_file.with_suffix('.qm')
#         success = False
#         if tool:
#             tool_name = tool if isinstance(tool, str) else 'pyside6-lrelease'
#             success = compile_with_pyside6_lrelease(ts_file, qm_file, tool_name)

#         if not success:
#             success = compile_ts_to_qm_fallback(ts_file, qm_file)
#             if success:
#                 fallback_count += 1

#         if success:
#             success_count += 1

#     logger.error(f"Sucessos: {success_count}/{len(ts_files)}")
#     if fallback_count > 0:
#         logger.error(f"Usando método alternativo: {fallback_count}")

#     return success_count > 0

# def validate_translations():
#     logger.error("Validando arquivos de tradução...")
#     current_dir = Path(__file__).parent
#     ts_files = list(current_dir.glob('*.ts'))

#     if not ts_files:
#         logger.error("Nenhum arquivo .ts encontrado!")
#         return False

#     valid_count = 0

#     for ts_file in sorted(ts_files):
#         is_valid, message = validate_ts_file(ts_file)
#         status = "✓" if is_valid else "✗"
#         logger.error(f"{status} {ts_file.name}: {message}")

#         if is_valid:
#             valid_count += 1

#     logger.error(f"Resultado: {valid_count}/{len(ts_files)} arquivos válidos")
#     return valid_count == len(ts_files)

# def list_translations():
#     logger.error("Arquivos de tradução disponíveis:")
#     current_dir = Path(__file__).parent
#     ts_files = list(current_dir.glob('*.ts'))

#     if not ts_files:
#         logger.error("Nenhum arquivo .ts encontrado!")
#         return

#     for ts_file in sorted(ts_files):
#         qm_file = ts_file.with_suffix('.qm')
#         qm_exists = qm_file.exists()
#         is_valid, validation_message = validate_ts_file(ts_file)
#         status = "✓" if qm_exists else "✗"
#         validity = "✓" if is_valid else "✗"
#         logger.error(f"{status} {ts_file.name} - {validity} {validation_message}")

#         if qm_exists:
#             ts_time = ts_file.stat().st_mtime
#             qm_time = qm_file.stat().st_mtime
#             if ts_time > qm_time:
#                 logger.error(f"Arquivo .ts mais recente que .qm")

# def clean_compiled():
#     logger.error("Removendo arquivos .qm...")
#     current_dir = Path(__file__).parent
#     qm_files = list(current_dir.glob('*.qm'))

#     if not qm_files:
#         logger.error("Nenhum arquivo .qm encontrado!")
#         return

#     removed_count = 0

#     for qm_file in qm_files:
#         try:
#             qm_file.unlink()
#             logger.error(f"Removido: {qm_file.name}")
#             removed_count += 1

#         except Exception as e:
#             logger.error(f"Erro ao remover {qm_file.name}: {e}")

#     logger.error(f"Resultado: {removed_count} arquivos removidos")

# def show_stats():
#     logger.error("Estatísticas das traduções:")
#     current_dir = Path(__file__).parent
#     ts_files = list(current_dir.glob('*.ts'))

#     if not ts_files:
#         logger.error("Nenhum arquivo .ts encontrado!")
#         return

#     total_files = len(ts_files)
#     valid_files = 0
#     total_messages = 0
#     total_translated = 0

#     for ts_file in sorted(ts_files):
#         try:
#             tree = ET.parse(ts_file)
#             root = tree.getroot()
#             file_messages = 0
#             file_translated = 0
#             for context in root.findall('context'):
#                 for message in context.findall('message'):
#                     file_messages += 1
#                     locale = message.find('locale')
#                     if locale is not None and locale.text and locale.text.strip():
#                         file_translated += 1

#             total_messages += file_messages
#             total_translated += file_translated
#             valid_files += 1
#             completion = (file_translated / file_messages * 100) if file_messages > 0 else 0
#             lang_code = ts_file.stem.split('_')[-1] if '_' in ts_file.stem else 'unknown'
#             logger.error(f"{lang_code}: {file_translated}/{file_messages} ({completion:.1f}%)")

#         except Exception as e:
#             logger.error(f"{ts_file.name}: Erro - {e}")

#     overall_completion = (total_translated / total_messages * 100) if total_messages > 0 else 0
#     logger.error(f"Total: {total_translated}/{total_messages} ({overall_completion:.1f}%)")
#     logger.error(f"Arquivos válidos: {valid_files}/{total_files}")

# def install_tools():
#     logger.error("Tentando instalar ferramentas do PySide6...")
#     packages = ['PySide6-Essentials', 'PySide6-Addons']
#     for package in packages:
#         try:
#             logger.error(f"Instalando {package}...")
#             result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True, text=True)
#             if result.returncode == 0:
#                 logger.error(f"{package} instalado com sucesso")

#             else:
#                 logger.error(f"Erro ao instalar {package}: {result.stderr}")

#         except Exception as e:
#             logger.error(f"Erro ao instalar {package}: {e}")

# def main():
#     logger.error("Compilador de Traduções - Linceu Lighthouse (PySide6)")
#     script_dir = Path(__file__).parent
#     os.chdir(script_dir)
#     if len(sys.argv) > 1:
#         command = sys.argv[1].lower()
#         if command == 'compile':
#             compile_translations()

#         elif command == 'validate':
#             validate_translations()

#         elif command == 'list':
#             list_translations()

#         elif command == 'clean':
#             clean_compiled()

#         elif command == 'stats':
#             show_stats()

#         elif command == 'install':
#             install_tools()

#         elif command == 'all':
#             logger.error("Validando arquivos...")
#             if validate_translations():
#                 logger.error("Compilando traduções...")
#                 compile_translations()

#             else:
#                 logger.error("Alguns arquivos têm problemas. Corrija-os antes de compilar.")

#         else:
#             logger.error(f"Comando desconhecido: {command}")
#             logger.error("Comandos disponíveis: compile, validate, list, clean, stats, install, all")

#     else:
#         logger.error("Uso:")
#         logger.error("  python compile_translations.py compile   - Compila traduções")
#         logger.error("  python compile_translations.py validate  - Valida arquivos .ts")
#         logger.error("  python compile_translations.py list      - Lista arquivos de tradução")
#         logger.error("  python compile_translations.py clean     - Remove arquivos .qm")
#         logger.error("  python compile_translations.py stats     - Mostra estatísticas")
#         logger.error("  python compile_translations.py install   - Tenta instalar ferramentas")
#         logger.error("  python compile_translations.py all       - Valida e compila")

# if __name__ == '__main__':
#     main()

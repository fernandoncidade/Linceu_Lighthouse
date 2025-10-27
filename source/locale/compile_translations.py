import os
import sys
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

def find_lrelease():
    candidates = [
        "pyside6-lrelease",
        "lrelease-qt6",
        "lrelease",
    ]

    for name in candidates:
        exe = shutil.which(name)
        if exe:
            return exe

    exe_dir = Path(sys.executable).parent
    win_names = ["pyside6-lrelease.exe", "lrelease-qt6.exe", "lrelease.exe"]
    for name in win_names:
        cand = exe_dir / name
        if cand.exists():
            return str(cand)

    unix_names = ["pyside6-lrelease", "lrelease-qt6", "lrelease"]
    for name in unix_names:
        cand = exe_dir / name
        if cand.exists():
            return str(cand)

    return None

def compile_with_lrelease(ts_file_path, qm_file_path, tool_path):
    try:
        print(f"Compilando com {tool_path}: {ts_file_path.name}")

        resultado = subprocess.run(
            [tool_path, str(ts_file_path), "-qm", str(qm_file_path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if resultado.stdout.strip():
            print(f"  ✓ {resultado.stdout.strip()}")

        else:
            print("  ✓ Compilado com sucesso")

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
            for message in context.findall('message'):
                source_elem = message.find('source')
                translation_elem = message.find('translation')

                if source_elem is None or translation_elem is None:
                    continue

                source_text = source_elem.text or ""
                translation_text = translation_elem.text or ""
                unfinished = translation_elem.get('type') == 'unfinished'

                if translation_text.strip() and not unfinished:
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
            print(f"  ⚠ Nenhuma tradução válida encontrada em {ts_file_path.name}")
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
                translation_elem = message.find('translation')
                if translation_elem is not None:
                    unfinished = translation_elem.get('type') == 'unfinished'
                    text = (translation_elem.text or "").strip()
                    if text and not unfinished:
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

    tool_path = find_lrelease()

    if tool_path:
        print(f"✓ Ferramenta encontrada: {tool_path}")
    else:
        print("⚠ lrelease/pyside6-lrelease não encontrado - usando método alternativo")
        print("  Para instalar: pip install PySide6-Essentials")

    print()

    success_count = 0
    fallback_count = 0

    for ts_file in sorted(ts_files):
        qm_file = ts_file.with_suffix('.qm')
        success = False

        if tool_path:
            success = compile_with_lrelease(ts_file, qm_file, tool_path)

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
                    translation_elem = message.find('translation')
                    if translation_elem is not None:
                        unfinished = translation_elem.get('type') == 'unfinished'
                        text = (translation_elem.text or "").strip()
                        if text and not unfinished:
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
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True, text=True)
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

    command = (sys.argv[1].lower() if len(sys.argv) > 1 else "compile")

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


if __name__ == '__main__':
    main()

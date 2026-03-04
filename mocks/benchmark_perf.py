import os
import sys
import time
import types
import sqlite3
import tempfile
import threading
import subprocess
import shutil
import argparse
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SCAN_PATH = ROOT / "source" / "services" / "GerenciamentoDiretorioScanner" / "gscanner_02_scan_directory.py"
DBW_PATH = ROOT / "source" / "services" / "GerenciamentoBaseEvento" / "gbank_20_db_writer.py"


def load_module_from_source(source: str, module_name: str):
    mod = types.ModuleType(module_name)
    mod.__file__ = module_name
    exec(compile(source, module_name, "exec"), mod.__dict__)
    return mod


def load_baseline_source(git_path: str) -> str:
    cmd = ["git", "show", f"HEAD:{git_path}"]
    out = subprocess.check_output(cmd, cwd=str(ROOT), text=True, encoding="utf-8")
    return out


def load_current_source(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def prepare_dataset(base_dir: Path, n_dirs: int = 40, files_per_dir: int = 120):
    data_dir = base_dir / "dataset"
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = ("abc123\n" * 30).encode("utf-8")

    for d in range(n_dirs):
        sub = data_dir / f"dir_{d:03d}"
        sub.mkdir(exist_ok=True)
        for f in range(files_per_dir):
            ext = ".txt" if f % 3 else ".log"
            p = sub / f"file_{f:04d}{ext}"
            p.write_bytes(payload)

    return data_dir


def create_schema(db_path: Path):
    colunas = [
        "tipo_operacao TEXT", "nome TEXT", "dir_anterior TEXT", "dir_atual TEXT",
        "data_criacao TEXT", "data_modificacao TEXT", "data_acesso TEXT", "tipo TEXT",
        "size_b TEXT", "size_kb TEXT", "size_mb TEXT", "size_gb TEXT", "size_tb TEXT",
        "atributos TEXT", "autor TEXT", "dimensoes TEXT", "duracao TEXT", "taxa_bits TEXT",
        "protegido TEXT", "paginas TEXT", "linhas TEXT", "palavras TEXT", "paginas_estimadas TEXT",
        "linhas_codigo TEXT", "total_linhas TEXT", "slides_estimados TEXT", "arquivos TEXT",
        "unzipped_b TEXT", "unzipped_kb TEXT", "unzipped_mb TEXT", "unzipped_gb TEXT", "unzipped_tb TEXT",
        "slides TEXT", "binary_file_b TEXT", "binary_file_kb TEXT", "binary_file_mb TEXT",
        "binary_file_gb TEXT", "binary_file_tb TEXT", "planilhas TEXT", "colunas TEXT",
        "registros TEXT", "tabelas TEXT", "timestamp TEXT"
    ]
    tables = ["monitoramento", "adicionado", "excluido", "modificado", "renomeado", "movido", "escaneado", "snapshot"]
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        for t in tables:
            if t == "snapshot":
                cur.execute("CREATE TABLE IF NOT EXISTS snapshot (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, dir_atual TEXT)")
            else:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {t} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(colunas)})")
        conn.commit()


class DummyThread:
    @staticmethod
    def currentThread():
        return DummyThread()

    def isInterruptionRequested(self):
        return False


class Emitter:
    def __init__(self):
        self.count = 0

    def emit(self, *args, **kwargs):
        self.count += 1


class LocStub:
    def get_text(self, key):
        mp = {
            "op_scanned": "SCANNED"
        }
        return mp.get(key, key)


class ColStub:
    @staticmethod
    def get_metadados(item):
        p = item.get("dir_atual") or item.get("dir_anterior")
        try:
            st = os.stat(p)
            size = st.st_size if os.path.isfile(p) else 0
        except Exception:
            size = 0
        return {
            "tipo": "arquivo" if os.path.isfile(p) else "diretorio",
            "size_b": size,
            "size_kb": round(size / 1024, 2),
            "size_mb": round(size / (1024**2), 4),
            "size_gb": 0,
            "size_tb": 0,
        }


class EventBaseCounter:
    def __init__(self):
        self.count = 0

    def registrar_evento_no_banco(self, evento):
        self.count += 1


class ObsStub:
    def __init__(self):
        self.desligando = False
        self.loc = LocStub()
        self.evento_base = EventBaseCounter()


class ScannerStub:
    def __init__(self, db_path):
        self.total_arquivos = 0
        self.db_path = str(db_path)
        self._pause_event = threading.Event()
        self._pause_event.set()
        self.observador = ObsStub()
        self.gerenciador_colunas = ColStub()
        self.progresso_atualizado = Emitter()
        self.scan_finalizado = Emitter()

    @staticmethod
    def get_file_type(path):
        return "diretorio" if os.path.isdir(path) else "arquivo"


def benchmark_scan(scan_module, dataset_path: Path, rounds: int = 3):
    scan_module.QThread = DummyThread
    fn = scan_module.scan_directory
    times = []
    events = 0

    for _ in range(rounds):
        db = dataset_path.parent / f"scan_{int(time.time()*1000000)}.db"
        create_schema(db)
        scanner = ScannerStub(db)
        t0 = time.perf_counter()
        fn(scanner, str(dataset_path))
        dt = time.perf_counter() - t0
        times.append(dt)
        events = scanner.observador.evento_base.count

    avg = sum(times) / len(times)
    std = statistics.pstdev(times) if len(times) > 1 else 0.0
    return {
        "avg_s": avg,
        "std_s": std,
        "events": events,
        "events_per_s": events / avg if avg else 0,
        "runs": times,
    }


def make_event(i: int):
    return {
        "tipo_operacao": "SCANNED",
        "nome": f"f{i}",
        "dir_anterior": "",
        "dir_atual": f"C:/tmp/f{i}",
        "data_criacao": "",
        "data_modificacao": "",
        "data_acesso": "",
        "tipo": "arquivo",
        "size_b": "123",
        "size_kb": "0.12",
        "size_mb": "0",
        "size_gb": "0",
        "size_tb": "0",
        "atributos": "",
        "autor": "",
        "dimensoes": "",
        "duracao": "",
        "taxa_bits": "",
        "protegido": "",
        "paginas": "",
        "linhas": "",
        "palavras": "",
        "paginas_estimadas": "",
        "linhas_codigo": "",
        "total_linhas": "",
        "slides_estimados": "",
        "arquivos": "",
        "unzipped_b": "",
        "unzipped_kb": "",
        "unzipped_mb": "",
        "unzipped_gb": "",
        "unzipped_tb": "",
        "slides": "",
        "binary_file_b": "",
        "binary_file_kb": "",
        "binary_file_mb": "",
        "binary_file_gb": "",
        "binary_file_tb": "",
        "planilhas": "",
        "colunas": "",
        "registros": "",
        "tabelas": "",
        "timestamp": "2026-03-03 00:00:00.000001",
    }


def benchmark_writer(dbw_module, db_path: Path, n_events: int = 30000):
    create_schema(db_path)
    dbw_module._instance = None
    w = dbw_module.DatabaseWriter.get_instance(str(db_path))

    t0 = time.perf_counter()
    for i in range(n_events):
        w.enqueue_event("escaneado", make_event(i))

    while True:
        try:
            qsize = w._q.qsize()
        except Exception:
            qsize = 0
        if qsize == 0:
            break
        time.sleep(0.01)

    time.sleep(0.2)
    w.stop()
    dt = time.perf_counter() - t0

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM escaneado")
        c1 = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM monitoramento")
        c2 = cur.fetchone()[0]

    return {
        "seconds": dt,
        "enqueued": n_events,
        "rows_escaneado": c1,
        "rows_monitoramento": c2,
        "events_per_s": n_events / dt if dt else 0,
    }


def pct_gain(before, after):
    if before == 0:
        return 0.0
    return ((after - before) / before) * 100.0


def run_scan_comparison(dataset: Path, rounds: int):
    baseline_scan_src = load_baseline_source("source/services/GerenciamentoDiretorioScanner/gscanner_02_scan_directory.py")
    current_scan_src = load_current_source(SCAN_PATH)
    baseline_scan_mod = load_module_from_source(baseline_scan_src, "baseline_scan_mod")
    current_scan_mod = load_module_from_source(current_scan_src, "current_scan_mod")

    print("=== BENCHMARK SCAN (tempo + throughput) ===")
    b_scan = benchmark_scan(baseline_scan_mod, dataset, rounds=rounds)
    c_scan = benchmark_scan(current_scan_mod, dataset, rounds=rounds)
    print(
        f"Baseline scan avg: {b_scan['avg_s']:.4f}s (std {b_scan['std_s']:.4f}) "
        f"| eventos: {b_scan['events']} | ev/s: {b_scan['events_per_s']:.2f}"
    )
    print(
        f"Atual    scan avg: {c_scan['avg_s']:.4f}s (std {c_scan['std_s']:.4f}) "
        f"| eventos: {c_scan['events']} | ev/s: {c_scan['events_per_s']:.2f}"
    )
    print(f"Ganho scan (ev/s): {pct_gain(b_scan['events_per_s'], c_scan['events_per_s']):.2f}%")


def main():
    parser = argparse.ArgumentParser(description="Benchmark de desempenho do Linceu Lighthouse")
    parser.add_argument("--real-dir", type=str, default="", help="Diretório real para benchmark de scan")
    parser.add_argument("--rounds", type=int, default=3, help="Quantidade de rodadas")
    args = parser.parse_args()

    temp_root = Path(tempfile.mkdtemp(prefix="bench_linceu_"))
    try:
        rounds = max(1, int(args.rounds))

        if args.real_dir:
            dataset = Path(args.real_dir)
            if not dataset.exists() or not dataset.is_dir():
                raise ValueError(f"Diretório inválido: {dataset}")

            print(f"Diretório real: {dataset}")

        else:
            dataset = prepare_dataset(temp_root)
            print(f"Dataset sintético: {dataset}")

        run_scan_comparison(dataset, rounds)

        baseline_dbw_src = load_baseline_source("source/services/GerenciamentoBaseEvento/gbank_20_db_writer.py")
        current_dbw_src = load_current_source(DBW_PATH)
        baseline_dbw_mod = load_module_from_source(baseline_dbw_src, "baseline_dbw_mod")
        current_dbw_mod = load_module_from_source(current_dbw_src, "current_dbw_mod")

        print("\n=== BENCHMARK EVENTOS (DatabaseWriter throughput) ===")
        b_db = benchmark_writer(baseline_dbw_mod, temp_root / "baseline_writer.db")
        c_db = benchmark_writer(current_dbw_mod, temp_root / "current_writer.db")
        print(f"Baseline writer: {b_db['seconds']:.4f}s | ev/s: {b_db['events_per_s']:.2f} | rows: esc={b_db['rows_escaneado']} mon={b_db['rows_monitoramento']}")
        print(f"Atual    writer: {c_db['seconds']:.4f}s | ev/s: {c_db['events_per_s']:.2f} | rows: esc={c_db['rows_escaneado']} mon={c_db['rows_monitoramento']}")
        print(f"Ganho writer (ev/s): {pct_gain(b_db['events_per_s'], c_db['events_per_s']):.2f}%")

    finally:
        try:
            shutil.rmtree(temp_root, ignore_errors=True)

        except Exception:
            pass


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()

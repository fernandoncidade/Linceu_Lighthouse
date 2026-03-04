import os
import sqlite3
import time
from PySide6.QtCore import QThread
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def scan_directory(self, directory):
    try:
        ultimo_emit_progresso = 0.0

        def emitir_progresso(contador_local, forcar=False):
            nonlocal ultimo_emit_progresso
            agora = time.monotonic()
            if not forcar and (agora - ultimo_emit_progresso) < 0.05 and (contador_local % 200) != 0:
                return

            ultimo_emit_progresso = agora
            total = self.total_arquivos or 1
            self.progresso_atualizado.emit(int(contador_local * 100 / total), contador_local, total)

        def montar_evento(nome_item, caminho_item, metadados_item):
            return {
                "tipo_operacao": self.observador.loc.get_text("op_scanned"),
                "nome": nome_item,
                "dir_anterior": "",
                "dir_atual": caminho_item,
                "data_criacao": metadados_item.get("data_criacao", ""),
                "data_modificacao": metadados_item.get("data_modificacao", ""),
                "data_acesso": metadados_item.get("data_acesso", ""),
                "tipo": metadados_item.get("tipo", ""),
                "size_b": metadados_item.get("size_b", ""),
                "size_kb": metadados_item.get("size_kb", ""),
                "size_mb": metadados_item.get("size_mb", ""),
                "size_gb": metadados_item.get("size_gb", ""),
                "size_tb": metadados_item.get("size_tb", ""),
                "atributos": metadados_item.get("atributos", ""),
                "autor": metadados_item.get("autor", ""),
                "dimensoes": metadados_item.get("dimensoes", ""),
                "duracao": metadados_item.get("duracao", ""),
                "taxa_bits": metadados_item.get("taxa_bits", ""),
                "protegido": metadados_item.get("protegido", ""),
                "paginas": metadados_item.get("paginas", ""),
                "linhas": metadados_item.get("linhas", ""),
                "palavras": metadados_item.get("palavras", ""),
                "paginas_estimadas": metadados_item.get("paginas_estimadas", ""),
                "linhas_codigo": metadados_item.get("linhas_codigo", ""),
                "total_linhas": metadados_item.get("total_linhas", ""),
                "slides_estimados": metadados_item.get("slides_estimados", ""),
                "arquivos": metadados_item.get("arquivos", ""),
                "unzipped_b": metadados_item.get("unzipped_b", ""),
                "unzipped_kb": metadados_item.get("unzipped_kb", ""),
                "unzipped_mb": metadados_item.get("unzipped_mb", ""),
                "unzipped_gb": metadados_item.get("unzipped_gb", ""),
                "unzipped_tb": metadados_item.get("unzipped_tb", ""),
                "slides": metadados_item.get("slides", ""),
                "binary_file_b": metadados_item.get("binary_file_b", ""),
                "binary_file_kb": metadados_item.get("binary_file_kb", ""),
                "binary_file_mb": metadados_item.get("binary_file_mb", ""),
                "binary_file_gb": metadados_item.get("binary_file_gb", ""),
                "binary_file_tb": metadados_item.get("binary_file_tb", ""),
                "planilhas": metadados_item.get("planilhas", ""),
                "colunas": metadados_item.get("colunas", ""),
                "registros": metadados_item.get("registros", ""),
                "tabelas": metadados_item.get("tabelas", ""),
            }

        self.total_arquivos = 0
        for _, dirs, files in os.walk(directory):
            self.total_arquivos += len(files) + len(dirs)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM snapshot")
            conn.commit()

        contador = 0
        for root, dirs, files in os.walk(directory):
            while hasattr(self, "_pause_event") and not self._pause_event.is_set():
                if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                    return

                time.sleep(0.1)

            if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                return

            for d in dirs:
                while hasattr(self, "_pause_event") and not self._pause_event.is_set():
                    if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                        return

                    time.sleep(0.1)

                if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                    return

                caminho = os.path.join(root, d)
                item = {
                    "nome": d,
                    "dir_atual": caminho
                }
                metadados = self.gerenciador_colunas.get_metadados(item)
                evento = montar_evento(d, caminho, metadados)
                self.observador.evento_base.registrar_evento_no_banco(evento)
                contador += 1
                emitir_progresso(contador)

            for f in files:
                while hasattr(self, "_pause_event") and not self._pause_event.is_set():
                    if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                        return

                    time.sleep(0.1)

                if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                    return

                caminho = os.path.join(root, f)
                item = {
                    "nome": f,
                    "dir_atual": caminho
                }
                metadados = self.gerenciador_colunas.get_metadados(item)
                evento = montar_evento(f, caminho, metadados)
                self.observador.evento_base.registrar_evento_no_banco(evento)
                contador += 1
                emitir_progresso(contador)

        emitir_progresso(contador, forcar=True)
        self.scan_finalizado.emit()

    except Exception as e:
        logger.error(f"Erro no scan_directory: {e}", exc_info=True)
        raise

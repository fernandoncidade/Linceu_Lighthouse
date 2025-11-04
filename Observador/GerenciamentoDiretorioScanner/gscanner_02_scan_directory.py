import os
import sqlite3
from PySide6.QtCore import QThread
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def scan_directory(self, directory):
    try:
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
                    logger.info("Scan interrompido durante pausa por requestInterruption ou desligando")
                    return

                import time; time.sleep(0.1)

            if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                logger.info("Scan interrompido por requestInterruption ou desligando")
                return

            for d in dirs:
                while hasattr(self, "_pause_event") and not self._pause_event.is_set():
                    if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                        logger.info("Scan interrompido durante pausa por requestInterruption ou desligando")
                        return

                    import time; time.sleep(0.1)

                if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                    logger.info("Scan interrompido por requestInterruption ou desligando")
                    return

                caminho = os.path.join(root, d)
                tipo = self.get_file_type(caminho)
                item = {
                    "nome": d,
                    "dir_atual": caminho
                }
                metadados = self.gerenciador_colunas.get_metadados(item)
                evento = {
                    "tipo_operacao": self.observador.loc.get_text("op_scanned"),
                    "nome": d,
                    "dir_anterior": "",
                    "dir_atual": caminho,
                    "data_criacao": metadados.get("data_criacao", ""),
                    "data_modificacao": metadados.get("data_modificacao", ""),
                    "data_acesso": metadados.get("data_acesso", ""),
                    "tipo": tipo,
                    "size_b": metadados.get("size_b", ""),
                    "size_kb": metadados.get("size_kb", ""),
                    "size_mb": metadados.get("size_mb", ""),
                    "size_gb": metadados.get("size_gb", ""),
                    "size_tb": metadados.get("size_tb", ""),
                    "atributos": metadados.get("atributos", ""),
                    "autor": metadados.get("autor", ""),
                    "dimensoes": metadados.get("dimensoes", ""),
                    "duracao": metadados.get("duracao", ""),
                    "taxa_bits": metadados.get("taxa_bits", ""),
                    "protegido": metadados.get("protegido", ""),
                    "paginas": metadados.get("paginas", ""),
                    "linhas": metadados.get("linhas", ""),
                    "palavras": metadados.get("palavras", ""),
                    "paginas_estimadas": metadados.get("paginas_estimadas", ""),
                    "linhas_codigo": metadados.get("linhas_codigo", ""),
                    "total_linhas": metadados.get("total_linhas", ""),
                    "slides_estimados": metadados.get("slides_estimados", ""),
                    "arquivos": metadados.get("arquivos", ""),
                    "unzipped_b": metadados.get("unzipped_b", ""),
                    "unzipped_kb": metadados.get("unzipped_kb", ""),
                    "unzipped_mb": metadados.get("unzipped_mb", ""),
                    "unzipped_gb": metadados.get("unzipped_gb", ""),
                    "unzipped_tb": metadados.get("unzipped_tb", ""),
                    "slides": metadados.get("slides", ""),
                    "binary_file_b": metadados.get("binary_file_b", ""),
                    "binary_file_kb": metadados.get("binary_file_kb", ""),
                    "binary_file_mb": metadados.get("binary_file_mb", ""),
                    "binary_file_gb": metadados.get("binary_file_gb", ""),
                    "binary_file_tb": metadados.get("binary_file_tb", ""),
                    "planilhas": metadados.get("planilhas", ""),
                    "colunas": metadados.get("colunas", ""),
                    "registros": metadados.get("registros", ""),
                    "tabelas": metadados.get("tabelas", ""),
                }
                self.observador.evento_base.registrar_evento_no_banco(evento)
                contador += 1
                self.progresso_atualizado.emit(int(contador * 100 / self.total_arquivos), contador, self.total_arquivos)

            for f in files:
                while hasattr(self, "_pause_event") and not self._pause_event.is_set():
                    if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                        logger.info("Scan interrompido durante pausa por requestInterruption ou desligando")
                        return

                    import time; time.sleep(0.1)

                if QThread.currentThread().isInterruptionRequested() or self.observador.desligando:
                    logger.info("Scan interrompido por requestInterruption ou desligando")
                    return

                caminho = os.path.join(root, f)
                tipo = self.get_file_type(caminho)
                item = {
                    "nome": f,
                    "dir_atual": caminho
                }
                metadados = self.gerenciador_colunas.get_metadados(item)
                evento = {
                    "tipo_operacao": self.observador.loc.get_text("op_scanned"),
                    "nome": f,
                    "dir_anterior": "",
                    "dir_atual": caminho,
                    "data_criacao": metadados.get("data_criacao", ""),
                    "data_modificacao": metadados.get("data_modificacao", ""),
                    "data_acesso": metadados.get("data_acesso", ""),
                    "tipo": tipo,
                    "size_b": metadados.get("size_b", ""),
                    "size_kb": metadados.get("size_kb", ""),
                    "size_mb": metadados.get("size_mb", ""),
                    "size_gb": metadados.get("size_gb", ""),
                    "size_tb": metadados.get("size_tb", ""),
                    "atributos": metadados.get("atributos", ""),
                    "autor": metadados.get("autor", ""),
                    "dimensoes": metadados.get("dimensoes", ""),
                    "duracao": metadados.get("duracao", ""),
                    "taxa_bits": metadados.get("taxa_bits", ""),
                    "protegido": metadados.get("protegido", ""),
                    "paginas": metadados.get("paginas", ""),
                    "linhas": metadados.get("linhas", ""),
                    "palavras": metadados.get("palavras", ""),
                    "paginas_estimadas": metadados.get("paginas_estimadas", ""),
                    "linhas_codigo": metadados.get("linhas_codigo", ""),
                    "total_linhas": metadados.get("total_linhas", ""),
                    "slides_estimados": metadados.get("slides_estimados", ""),
                    "arquivos": metadados.get("arquivos", ""),
                    "unzipped_b": metadados.get("unzipped_b", ""),
                    "unzipped_kb": metadados.get("unzipped_kb", ""),
                    "unzipped_mb": metadados.get("unzipped_mb", ""),
                    "unzipped_gb": metadados.get("unzipped_gb", ""),
                    "unzipped_tb": metadados.get("unzipped_tb", ""),
                    "slides": metadados.get("slides", ""),
                    "binary_file_b": metadados.get("binary_file_b", ""),
                    "binary_file_kb": metadados.get("binary_file_kb", ""),
                    "binary_file_mb": metadados.get("binary_file_mb", ""),
                    "binary_file_gb": metadados.get("binary_file_gb", ""),
                    "binary_file_tb": metadados.get("binary_file_tb", ""),
                    "planilhas": metadados.get("planilhas", ""),
                    "colunas": metadados.get("colunas", ""),
                    "registros": metadados.get("registros", ""),
                    "tabelas": metadados.get("tabelas", ""),
                }
                self.observador.evento_base.registrar_evento_no_banco(evento)
                contador += 1
                self.progresso_atualizado.emit(int(contador * 100 / self.total_arquivos), contador, self.total_arquivos)

        self.scan_finalizado.emit()

    except Exception as e:
        logger.error(f"Erro no scan_directory: {e}", exc_info=True)
        raise

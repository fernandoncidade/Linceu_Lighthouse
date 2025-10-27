import time
from PySide6.QtCore import QMutexLocker, QTimer
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_exclusoes_pendentes(interfaceMonitor):
    try:
        eventos_para_processar = []
        tempo_atual = time.time()
        with QMutexLocker(interfaceMonitor.mutex):
            nomes_para_remover = []
            for nome, eventos_lista in interfaceMonitor.excluidos_recentemente.items():
                eventos_a_remover = []
                for registro in eventos_lista:
                    timestamp, dir_anterior, evento = registro
                    tempo_limite = 5 if nome.lower().endswith(('.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mkv', '.mov', '.avi', '.xml', '.exe')) else 0.5
                    if tempo_atual - timestamp > tempo_limite:
                        novo_evento = evento.copy()
                        novo_evento.pop("_temporario", None)
                        novo_evento["id_exclusao_unico"] = f"{nome}_{timestamp}_{id(registro)}"
                        eventos_para_processar.append(novo_evento)
                        eventos_a_remover.append(registro)

                for registro in eventos_a_remover:
                    eventos_lista.remove(registro)

                if not eventos_lista:
                    nomes_para_remover.append(nome)

            for nome in nomes_para_remover:
                del interfaceMonitor.excluidos_recentemente[nome]

        if len(eventos_para_processar) > 1:
            QTimer.singleShot(0, lambda: interfaceMonitor.processador_evento.eventos_em_lote_processados.emit(eventos_para_processar))

        elif eventos_para_processar:
            for evento in eventos_para_processar:
                QTimer.singleShot(0, lambda e=evento: interfaceMonitor.processador_evento.evento_processado.emit(e))

    except Exception as e:
        logger.error(f"Erro ao processar exclusões pendentes: {e}", exc_info=True)

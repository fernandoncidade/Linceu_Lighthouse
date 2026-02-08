import os
import time
from PySide6.QtCore import QMutexLocker
from concurrent.futures import ThreadPoolExecutor
from source.Observador.GerenciamentoEventoMovido.gevmov_03_remover_exclusao import _remover_exclusao
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def normalizar_caminho(caminho):
    return os.path.normpath(caminho).replace('/', '\\')

def verificar_movimentacao(interfaceMonitor, evento):
    try:
        if not isinstance(evento, dict) or "tipo_operacao" not in evento or "nome" not in evento:
            return evento

        if "dir_atual" in evento and evento["dir_atual"]:
            evento["dir_atual"] = normalizar_caminho(evento["dir_atual"])

        if "dir_anterior" in evento and evento["dir_anterior"]:
            evento["dir_anterior"] = normalizar_caminho(evento["dir_anterior"])

        with QMutexLocker(interfaceMonitor.mutex):
            if evento["tipo_operacao"] == interfaceMonitor.loc.get_text("op_deleted"):
                evento["exclusao_id"] = str(time.time())
                interfaceMonitor.excluidos_recentemente.setdefault(evento["nome"], []).append((time.time(), evento.get("dir_anterior", ""), evento))
                evento["_temporario"] = True
                return None

            elif evento["tipo_operacao"] == interfaceMonitor.loc.get_text("op_added"):
                if evento["nome"] in interfaceMonitor.excluidos_recentemente:
                    lista_exclusoes = interfaceMonitor.excluidos_recentemente[evento["nome"]]
                    lista_exclusoes.sort(key=lambda x: x[0], reverse=True)

                    for exclusao in lista_exclusoes:
                        excl_time, excl_dir, evento_exclusao = exclusao
                        tempo_limite = 5 if evento["nome"].lower().endswith(('.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mkv', '.mov', '.avi', '.xml', '.exe')) else 0.5
                        if time.time() - excl_time < tempo_limite:
                            if excl_dir != evento["dir_atual"]:
                                lista_exclusoes.remove(exclusao)
                                if not lista_exclusoes:
                                    del interfaceMonitor.excluidos_recentemente[evento["nome"]]

                                exclusao_id = evento_exclusao.get("exclusao_id")
                                with ThreadPoolExecutor(max_workers=1) as executor:
                                    executor.submit(_remover_exclusao, interfaceMonitor, evento["nome"], excl_dir, exclusao_id)

                                evento["tipo_operacao"] = interfaceMonitor.loc.get_text("op_moved")
                                evento["dir_anterior"] = excl_dir
                                return evento

                    if not lista_exclusoes:
                        del interfaceMonitor.excluidos_recentemente[evento["nome"]]

        return evento

    except Exception as e:
        logger.error(f"Erro geral em verificar_movimentacao: {e}", exc_info=True)
        return evento

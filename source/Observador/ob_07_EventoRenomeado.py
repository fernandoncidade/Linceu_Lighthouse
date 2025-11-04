import os
import time
from .ob_02_BaseEvento import BaseEvento


class EventoRenomeado(BaseEvento):
    def __init__(self, observador):
        super().__init__(observador)
        self.renomeacao_em_andamento = {}

    def processar(self, nome_arquivo, caminho_completo, acao):
        tempo_atual = time.time()

        if acao == 4:
            self.observador.registros_anteriores[caminho_completo] = nome_arquivo
            self.observador.registros_anteriores[nome_arquivo] = caminho_completo
            return True

        elif acao == 5:
            dir_atual = caminho_completo
            dir_base = os.path.dirname(dir_atual)

            nome_antigo = None
            dir_anterior = None

            for caminho_reg, nome_reg in list(self.observador.registros_anteriores.items()):
                if isinstance(caminho_reg, str) and isinstance(nome_reg, str):
                    if os.path.dirname(caminho_reg) == dir_base:
                        nome_antigo = nome_reg
                        dir_anterior = caminho_reg
                        self.observador.registros_anteriores.pop(caminho_reg)
                        self.observador.registros_anteriores.pop(nome_antigo, None)
                        break

            if not nome_antigo and self.observador.registros_anteriores:
                for key in list(self.observador.registros_anteriores.keys()):
                    if isinstance(key, str) and not key.startswith("/") and not key.startswith("\\"):
                        nome_antigo = key
                        dir_anterior = self.observador.registros_anteriores.pop(nome_antigo)
                        break

            if nome_antigo and dir_anterior:
                self.observador.arquivos_recem_renomeados[nome_arquivo] = tempo_atual
                self.observador.arquivos_recem_adicionados[nome_arquivo] = tempo_atual
                self.observador.ultima_modificacao[nome_arquivo] = tempo_atual

                self.notificar_evento(self.observador.loc.get_text("op_renamed"), nome_arquivo, dir_anterior, caminho_completo)
                return True

        return True

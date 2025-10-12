from utils.LogManager import LogManager
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_01_desconectar_sinais import desconectar_sinais
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_02_aplicar_filtros import aplicar_filtros
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_03_limpar_filtros import limpar_filtros
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_04_sincronizar_menu_principal_com_filtros import sincronizar_menu_principal_com_filtros
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_05_atualizar_contagem import atualizar_contagem
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_06_atualizar_contagem_eventos_monitorados import atualizar_contagem_eventos_monitorados
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_07_verificar_filtro_operacao import verificar_filtro_operacao
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_08_atualizar_contagem_apos_idioma import atualizar_contagem_apos_idioma
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_09_notificar_alteracao_idioma import notificar_alteracao_idioma
from source.Filtros.GerenciamentoAdministradorFiltros.gadmfil_10_salvar_estado_checkboxes import salvar_estado_checkboxes
logger = LogManager.get_logger()


class AdministradorFiltros:
    try:
        filtros_estado = {
            "ignorar_mover": True,
            "ignorar_renomeados": True,
            "ignorar_adicionados": True,
            "ignorar_excluidos": True,
            "ignorar_data_modificados": True,
            "ignorar_escaneados": True
        }

        def __init__(self, parent):
            self.parent = parent
            self.conexoes_sinais = []
            self.contadores = {
                "op_moved": 0,
                "op_renamed": 0, 
                "op_added": 0,
                "op_deleted": 0,
                "op_modified": 0,
                "op_scanned": 0
            }
            self.contadores_originais = {
                "op_moved": 0,
                "op_renamed": 0, 
                "op_added": 0,
                "op_deleted": 0,
                "op_modified": 0,
                "op_scanned": 0
            }

            from PySide6.QtWidgets import QApplication
            for widget in QApplication.topLevelWidgets():
                if hasattr(widget, 'loc') and hasattr(widget.loc, 'idioma_alterado'):
                    conexao = widget.loc.idioma_alterado.connect(self.atualizar_contagem_apos_idioma)
                    self.conexoes_sinais.append((widget.loc.idioma_alterado, conexao))
                    break

            if hasattr(self.parent, 'loc') and hasattr(self.parent.loc, 'idioma_alterado'):
                conexao = self.parent.loc.idioma_alterado.connect(self.atualizar_contagem_apos_idioma)
                self.conexoes_sinais.append((self.parent.loc.idioma_alterado, conexao))

            if hasattr(parent, "destroyed"):
                parent.destroyed.connect(self.desconectar_sinais)

    except Exception as e:
        logger.error(f"Erro ao inicializar o AdministradorFiltros: {e}", exc_info=True)

    desconectar_sinais = desconectar_sinais
    aplicar_filtros = aplicar_filtros
    limpar_filtros = limpar_filtros
    sincronizar_menu_principal_com_filtros = sincronizar_menu_principal_com_filtros
    atualizar_contagem = atualizar_contagem
    atualizar_contagem_eventos_monitorados = atualizar_contagem_eventos_monitorados
    verificar_filtro_operacao = verificar_filtro_operacao
    atualizar_contagem_apos_idioma = atualizar_contagem_apos_idioma
    notificar_alteracao_idioma = notificar_alteracao_idioma
    salvar_estado_checkboxes = salvar_estado_checkboxes

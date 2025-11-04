import os
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QMenu
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, posicao):
    try:
        index = self.tree.indexAt(posicao)
        menu = QMenu(self)

        if index.isValid():
            info = self.model.fileInfo(index)
            caminho = info.absoluteFilePath()

            acao_abrir = QAction(QCoreApplication.translate("LinceuLighthouse", "open"), self)
            acao_abrir.triggered.connect(lambda: self.abrir_item(index))
            menu.addAction(acao_abrir)

            menu.addSeparator()

            acao_copiar = QAction(QCoreApplication.translate("LinceuLighthouse", "copy"), self)
            acao_copiar.setShortcut(QKeySequence.Copy)
            acao_copiar.triggered.connect(self.copiar_selecionados)
            menu.addAction(acao_copiar)

            acao_cortar = QAction(QCoreApplication.translate("LinceuLighthouse", "cut"), self)
            acao_cortar.setShortcut(QKeySequence.Cut)
            acao_cortar.triggered.connect(self.cortar_selecionados)
            menu.addAction(acao_cortar)

            if self.clipboard_items:
                acao_colar = QAction(QCoreApplication.translate("LinceuLighthouse", "paste"), self)
                acao_colar.setShortcut(QKeySequence.Paste)
                acao_colar.triggered.connect(lambda: self.colar_items(caminho if info.isDir() else os.path.dirname(caminho)))
                menu.addAction(acao_colar)

            menu.addSeparator()

            acao_renomear = QAction(QCoreApplication.translate("LinceuLighthouse", "rename"), self)
            acao_renomear.setShortcut(Qt.Key_F2)
            acao_renomear.triggered.connect(self.renomear_selecionado)
            menu.addAction(acao_renomear)

            acao_excluir = QAction(QCoreApplication.translate("LinceuLighthouse", "delete"), self)
            acao_excluir.setShortcut(QKeySequence.Delete)
            acao_excluir.triggered.connect(self.excluir_selecionados)
            menu.addAction(acao_excluir)

        else:
            pasta_destino = self.root_path

            acao_nova_pasta = QAction(QCoreApplication.translate("LinceuLighthouse", "new_folder"), self)
            acao_nova_pasta.triggered.connect(lambda: self.criar_nova_pasta(pasta_destino))
            menu.addAction(acao_nova_pasta)

            acao_novo_arquivo = QAction(QCoreApplication.translate("LinceuLighthouse", "new_file"), self)
            acao_novo_arquivo.triggered.connect(lambda: self.criar_novo_arquivo(pasta_destino))
            menu.addAction(acao_novo_arquivo)

            if self.clipboard_items:
                menu.addSeparator()
                acao_colar = QAction(QCoreApplication.translate("LinceuLighthouse", "paste"), self)
                acao_colar.triggered.connect(lambda: self.colar_items(pasta_destino))
                menu.addAction(acao_colar)

        menu.exec(self.tree.mapToGlobal(posicao))

    except Exception as e:
        logger.error(f"Erro ao mostrar menu de contexto: {e}", exc_info=True)

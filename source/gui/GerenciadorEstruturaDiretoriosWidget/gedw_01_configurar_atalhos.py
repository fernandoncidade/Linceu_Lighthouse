from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_atalhos(self):
    try:
        for shortcut in self.shortcuts:
            shortcut.setParent(None)

        self.shortcuts.clear()

        shortcut_copy = QShortcut(QKeySequence.Copy, self.tree)
        shortcut_copy.activated.connect(self.copiar_selecionados)
        self.shortcuts.append(shortcut_copy)

        shortcut_cut = QShortcut(QKeySequence.Cut, self.tree)
        shortcut_cut.activated.connect(self.cortar_selecionados)
        self.shortcuts.append(shortcut_cut)

        shortcut_paste = QShortcut(QKeySequence.Paste, self.tree)
        shortcut_paste.activated.connect(self.colar_items)
        self.shortcuts.append(shortcut_paste)

        shortcut_delete = QShortcut(QKeySequence.Delete, self.tree)
        shortcut_delete.activated.connect(self.excluir_selecionados)
        self.shortcuts.append(shortcut_delete)

        shortcut_rename = QShortcut(Qt.Key_F2, self.tree)
        shortcut_rename.activated.connect(self.renomear_selecionado)
        self.shortcuts.append(shortcut_rename)

        shortcut_new = QShortcut(QKeySequence.New, self.tree)
        shortcut_new.activated.connect(self.criar_nova_pasta)
        self.shortcuts.append(shortcut_new)

    except Exception as e:
        logger.error(f"Erro ao configurar atalhos: {e}", exc_info=True)

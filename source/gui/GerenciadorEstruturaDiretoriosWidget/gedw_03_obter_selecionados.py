from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_selecionados(self):
    try:
        indices = self.tree.selectionModel().selectedIndexes()
        caminhos = []
        for index in indices:
            if index.column() == 0:
                info = self.model.fileInfo(index)
                caminhos.append(info.absoluteFilePath())

        return caminhos

    except Exception as e:
        logger.error(f"Erro ao obter selecionados: {e}", exc_info=True)
        return []

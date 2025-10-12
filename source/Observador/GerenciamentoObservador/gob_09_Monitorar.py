import time
import win32file
import win32con
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def monitorar(self):
    try:
        BUFFER_SIZE = 16777216
        FILE_LIST_DIRECTORY = 0x0001
        try:
            self.handle_dir = None
            self.handle_dir = win32file.CreateFile(
                self.diretorio,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ |
                win32con.FILE_SHARE_WRITE |
                win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS |
                win32con.FILE_FLAG_OVERLAPPED,
                None
            )

        except Exception as e:
            logger.error(f"Erro ao criar handle de diretório: {e}", exc_info=True)
            self.handle_dir = None
            return

        while self.ativo:
            if not self._pause_event.is_set():
                time.sleep(0.1)
                continue

            try:
                self._pause_event.wait()
                results = win32file.ReadDirectoryChangesW(
                    self.handle_dir,
                    BUFFER_SIZE,
                    True,
                    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                    win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                    win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                    win32con.FILE_NOTIFY_CHANGE_SIZE |
                    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                    win32con.FILE_NOTIFY_CHANGE_SECURITY |
                    win32con.FILE_NOTIFY_CHANGE_CREATION,
                    None,
                    None
                )

                tempo_batch = time.time()
                self.total_eventos_recebidos += len(results)

                for action, file in results:
                        self._processar_evento_interno(action, file, tempo_batch)

            except win32file.error as e:
                if self.desligando:
                    break

                logger.error(f"Erro no monitoramento: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro desconhecido: {e}", exc_info=True)

        try:
            if (hasattr(self, 'handle_dir') and 
                self.handle_dir is not None and 
                self.handle_dir != win32file.INVALID_HANDLE_VALUE and
                self.handle_dir != 0):

                win32file.CloseHandle(self.handle_dir)

            self.handle_dir = None

        except Exception as e:
            logger.error(f"Erro ao fechar handle de diretório: {e}", exc_info=True)
            self.handle_dir = None

    except Exception as e:
        logger.error(f"Erro desconhecido: {e}", exc_info=True)

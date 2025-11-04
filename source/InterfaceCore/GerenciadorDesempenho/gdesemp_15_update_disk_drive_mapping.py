from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_disk_drive_mapping(self):
    try:
        if not self.psutil:
            return

        self._disk_drive_letters.clear()
        partitions = self.psutil.disk_partitions()

        for part in partitions:
            try:
                device = getattr(part, 'device', '')
                mountpoint = getattr(part, 'mountpoint', '')

                if mountpoint and len(mountpoint) >= 2 and mountpoint[1] == ':':
                    drive_letter = mountpoint[0].upper()

                    for disk_key in self.disk_keys:
                        if disk_key.lower().startswith('physicaldrive'):
                            try:
                                disk_num = int(disk_key.lower().replace('physicaldrive', ''))
                                if disk_num not in [v[1] for v in self._disk_drive_letters.values()]:
                                    self._disk_drive_letters[disk_key] = (drive_letter, disk_num)
                                    break

                            except Exception:
                                continue

                        else:
                            if device and (device in disk_key or disk_key in device):
                                self._disk_drive_letters[disk_key] = (drive_letter, 0)

            except Exception:
                continue

    except Exception as e:
        logger.debug(f"Erro ao mapear letras de unidade: {e}")

from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar(self):
    try:
        cpu = float(self.psutil.cpu_percent(interval=None))
        mem = float(self.psutil.virtual_memory().percent)
        disks = self._obter_percentual_disco()
        if len(self.disk_data) < len(disks):
            for _ in range(len(disks) - len(self.disk_data)):
                self.disk_data.append([])

        elif len(self.disk_data) > len(disks):
            self.disk_data = self.disk_data[:len(disks)]

        self.cpu_data.append(cpu)
        self.mem_data.append(mem)
        if len(self.cpu_data) > self.max_pontos:
            del self.cpu_data[0:len(self.cpu_data) - self.max_pontos]

        if len(self.mem_data) > self.max_pontos:
            del self.mem_data[0:len(self.mem_data) - self.max_pontos]

        for i, val in enumerate(disks):
            if i >= len(self.disk_data):
                self.disk_data.append([])

            self.disk_data[i].append(float(val))
            if len(self.disk_data[i]) > self.max_pontos:
                del self.disk_data[i][0:len(self.disk_data[i]) - self.max_pontos]

        self._atualizar_series(self.cpu_data, self.mem_data, self.disk_data)

    except Exception as e:
        logger.error(f"Erro em atualização de desempenho: {e}", exc_info=True)

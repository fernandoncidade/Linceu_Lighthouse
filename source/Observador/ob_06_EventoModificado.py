from .ob_02_BaseEvento import BaseEvento
from source.Observador.GerenciamentoEventoModificado.gevmod_01_calcular_intervalo import calcular_intervalo
from source.Observador.GerenciamentoEventoModificado.gevmod_02_calcular_intervalo_original import _calcular_intervalo_original
from source.Observador.GerenciamentoEventoModificado.gevmod_03_is_arquivo_codigo_grande import is_arquivo_codigo_grande
from source.Observador.GerenciamentoEventoModificado.gevmod_04_limpar_cache_metadados import _limpar_cache_metadados
from source.Observador.GerenciamentoEventoModificado.gevmod_05_processar import processar
from source.Observador.GerenciamentoEventoModificado.gevmod_06_processar_massivo import _processar_massivo
from source.Observador.GerenciamentoEventoModificado.gevmod_07_processar_normal import _processar_normal
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class EventoModificado(BaseEvento):
    def __init__(self, observador):
        super().__init__(observador)
        try:
            self.intervalo_base = 0.1
            self.tamanho_threshold = 100 * 1024 * 1024
            self.max_intervalo = 5
            self.exclusao_threshold = 0.1
            self.min_intervalo = 0.01
            self.modificacoes_recentes = {}
            self.count_modificacoes = {}
            self.eventos_grandes = {}
            self.grande_arquivo_threshold = 50 * 1024 * 1024
            self.tempo_espera_grande_arquivo = 3
            self.arquivos_em_processamento = set()

            self.EXTENSOES_VIDEO = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mts', '.m2ts', '.mpeg', '.m4v'}

            self.EXTENSOES_RAPIDAS = {'.txt', '.log', '.json', '.xml', '.csv', '.ini', '.cfg', '.conf', '.dat'}

            self.EXTENSOES_CODIGO = {'.tmp', '.temp', '.~', '.bak', '.swp', '.swo', '.$$', '.old', '.part', '.cache', 
                                    '.crdownload', '.download', '.partial', '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                                    '.tiff', '.tif', '.psd', '.svg', '.webp', '.raw', '.heic', '.heif', '.cr2', '.nef', 
                                    '.arw', '.wav', '.mp3', '.aac', '.flac', '.ogg', '.aiff', '.wma', '.m4a', '.aif',  
                                    '.py', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.js', '.html', '.htm', 
                                    '.mht', '.xhtml', '.mhml', '.css', '.php', '.sql', '.json', '.xml', '.yaml', '.yml', 
                                    '.ini', '.cfg', '.conf', '.log', '.md', '.rst', '.bat', '.sh', '.ps1', '.psm1', 
                                    '.psd1', '.ps1xml', '.pssc', '.psc1', '.doc', '.docx', '.pdf', '.rtf', '.txt', 
                                    '.odt', '.wpd', '.pages', '.xls', '.xlsx', '.ods', '.csv', '.tsv', '.numbers', 
                                    '.ppt', '.pptx', '.odp', '.key', '.db', '.sqlite', '.mdb', '.accdb', '.sav', 
                                    '.spss', '.exe', '.dll', '.bin', '.app', '.apk', '.msi', '.run', '.bat', '.cmd', 
                                    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.cab', '.dat'}

            self.CODIGO_LINHA_THRESHOLD = 1000

        except Exception as e:
            logger.error(f"Erro ao inicializar EventoModificado: {e}")

    calcular_intervalo = calcular_intervalo
    _calcular_intervalo_original = _calcular_intervalo_original
    is_arquivo_codigo_grande = is_arquivo_codigo_grande
    _limpar_cache_metadados = _limpar_cache_metadados
    processar = processar
    _processar_massivo = _processar_massivo
    _processar_normal = _processar_normal

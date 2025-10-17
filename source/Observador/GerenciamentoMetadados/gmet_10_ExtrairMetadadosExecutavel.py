import os
import ctypes
from ctypes import wintypes
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]

    def __init__(self, guid_string):
        import uuid
        guid = uuid.UUID(guid_string)
        ctypes.Structure.__init__(self)
        self.Data1 = guid.fields[0]
        self.Data2 = guid.fields[1]
        self.Data3 = guid.fields[2]
        for i in range(8):
            self.Data4[i] = guid.bytes[8 + i]

def verificar_assinatura_executavel(caminho):
    WINTRUST_ACTION_GENERIC_VERIFY_V2 = GUID('{00AAC56B-CD44-11d0-8CC2-00C04FC295EE}')

    class WINTRUST_FILE_INFO(ctypes.Structure):
        _fields_ = [
            ('cbStruct', wintypes.DWORD),
            ('pcwszFilePath', wintypes.LPCWSTR),
            ('hFile', wintypes.HANDLE),
            ('pgKnownSubject', ctypes.c_void_p)
        ]

    class WINTRUST_DATA(ctypes.Structure):
        _fields_ = [
            ('cbStruct', wintypes.DWORD),
            ('pPolicyCallbackData', ctypes.c_void_p),
            ('pSIPClientData', ctypes.c_void_p),
            ('dwUIChoice', wintypes.DWORD),
            ('fdwRevocationChecks', wintypes.DWORD),
            ('dwUnionChoice', wintypes.DWORD),
            ('pFile', ctypes.POINTER(WINTRUST_FILE_INFO)),
            ('dwStateAction', wintypes.DWORD),
            ('hWVTStateData', wintypes.HANDLE),
            ('pwszURLReference', wintypes.LPCWSTR),
            ('dwProvFlags', wintypes.DWORD),
            ('dwUIContext', wintypes.DWORD),
            ('pSignatureSettings', ctypes.c_void_p)
        ]

    WTD_UI_NONE = 2
    WTD_REVOKE_NONE = 0
    WTD_CHOICE_FILE = 1
    WTD_STATEACTION_VERIFY = 1
    WTD_PROV_FLAGS = 0x00000020

    WinVerifyTrust = ctypes.windll.wintrust.WinVerifyTrust
    WinVerifyTrust.argtypes = [
        wintypes.HWND,
        ctypes.POINTER(GUID),
        ctypes.POINTER(WINTRUST_DATA)
    ]
    WinVerifyTrust.restype = wintypes.LONG

    file_info = WINTRUST_FILE_INFO(
        cbStruct=ctypes.sizeof(WINTRUST_FILE_INFO),
        pcwszFilePath=caminho,
        hFile=None,
        pgKnownSubject=None
    )

    trust_data = WINTRUST_DATA(
        cbStruct=ctypes.sizeof(WINTRUST_DATA),
        pPolicyCallbackData=None,
        pSIPClientData=None,
        dwUIChoice=WTD_UI_NONE,
        fdwRevocationChecks=WTD_REVOKE_NONE,
        dwUnionChoice=WTD_CHOICE_FILE,
        pFile=ctypes.pointer(file_info),
        dwStateAction=WTD_STATEACTION_VERIFY,
        hWVTStateData=None,
        pwszURLReference=None,
        dwProvFlags=WTD_PROV_FLAGS,
        dwUIContext=0,
        pSignatureSettings=None
    )

    try:
        result = WinVerifyTrust(
            None,
            ctypes.pointer(WINTRUST_ACTION_GENERIC_VERIFY_V2),
            ctypes.pointer(trust_data)
        )

        if result == 0:
            return "Sim"

        elif result == 0x800B0100:
            return "Não"

        else:
            return "Erro"

    except Exception as e:
        logger.error(f"Erro ao verificar assinatura do executável {caminho}: {e}", exc_info=True)
        return "Erro"

def extrair_metadados_executavel(caminho, loc=None):
    metadados = {}

    if not os.path.exists(caminho):
        return metadados

    try:
        with open(caminho, 'rb') as f:
            header = f.read(2)
            if header != b'MZ':
                logger.error(f"Arquivo {caminho} não é um executável válido (cabeçalho não encontrado)")
                return metadados

    except Exception as e:
        logger.error(f"Erro ao verificar cabeçalho do arquivo: {e}", exc_info=True)
        return metadados

    try:
        import pefile
        import win32api
        import pywintypes

        info = None
        try:
            info = win32api.GetFileVersionInfo(caminho, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            versao = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"

            try:
                lang, codepage = win32api.GetFileVersionInfo(caminho, '\\VarFileInfo\\Translation')[0]
                str_info = {}
                for entry in ['CompanyName', 'FileDescription', 'InternalName', 'LegalCopyright', 'OriginalFilename', 'ProductName', 'ProductVersion', 'FileVersion']:
                    try:
                        str_path = f'\\StringFileInfo\\{lang:04x}{codepage:04x}\\{entry}'
                        str_info[entry] = win32api.GetFileVersionInfo(caminho, str_path)

                    except Exception as e:
                        logger.debug(f"Não foi possível ler string de versão {entry}: {e}")

                if 'FileVersion' in str_info and str_info['FileVersion']:
                    metadados['versao'] = str_info['FileVersion']

                else:
                    metadados['versao'] = versao

                if 'CompanyName' in str_info and str_info['CompanyName']:
                    metadados['empresa'] = str_info['CompanyName']

                if 'FileDescription' in str_info and str_info['FileDescription']:
                    metadados['descricao'] = str_info['FileDescription']

                if 'ProductName' in str_info and str_info['ProductName']:
                    metadados['produto'] = str_info['ProductName']

                if 'LegalCopyright' in str_info and str_info['LegalCopyright']:
                    metadados['copyright'] = str_info['LegalCopyright']

            except Exception as e:
                logger.debug(f"Erro ao extrair strings de versão via win32api (fallback para pefile): {e}")
                metadados['versao'] = versao

        except pywintypes.error as w32_err:
            winerr = getattr(w32_err, 'winerror', None)
            if winerr == 13 or (isinstance(w32_err.args, tuple) and w32_err.args and w32_err.args[0] == 13):
                logger.debug(f"GetFileVersionInfo retornou dados inválidos para {caminho}: {w32_err}. Usando fallback pefile.")

            else:
                logger.warning(f"win32api.GetFileVersionInfo falhou para {caminho}: {w32_err}")

            info = None

        except Exception as e:
            logger.warning(f"Erro ao usar win32api para obter versão: {e}")
            info = None

        try:
            if info is None:
                pe = pefile.PE(caminho, fast_load=True)

            else:
                pe = pefile.PE(caminho)

            info_pf = None
            if hasattr(pe, 'VS_FIXEDFILEINFO') and pe.VS_FIXEDFILEINFO:
                if isinstance(pe.VS_FIXEDFILEINFO, (list, tuple)):
                    info_pf = pe.VS_FIXEDFILEINFO[0]

                else:
                    info_pf = pe.VS_FIXEDFILEINFO

            if info_pf and hasattr(info_pf, 'FileVersionMS') and hasattr(info_pf, 'FileVersionLS'):
                versao = f"{info_pf.FileVersionMS >> 16}.{info_pf.FileVersionMS & 0xFFFF}.{info_pf.FileVersionLS >> 16}.{info_pf.FileVersionLS & 0xFFFF}"
                metadados['versao'] = versao

            if hasattr(pe, 'FileInfo') and pe.FileInfo:
                for fileinfo in pe.FileInfo:
                    for entry in fileinfo:
                        if hasattr(entry, 'StringTable'):
                            for st in entry.StringTable:
                                for key, value in st.entries.items():
                                    try:
                                        key_str = key.decode('utf-8', errors='ignore') if isinstance(key, (bytes, bytearray)) else str(key)
                                        val_str = value.decode('utf-8', errors='ignore') if isinstance(value, (bytes, bytearray)) else str(value)

                                    except Exception:
                                        continue

                                    if key_str == 'FileVersion':
                                        metadados['versao'] = val_str

                                    elif key_str == 'CompanyName':
                                        metadados['empresa'] = val_str

                                    elif key_str == 'FileDescription':
                                        metadados['descricao'] = val_str

                                    elif key_str == 'ProductName':
                                        metadados['produto'] = val_str

                                    elif key_str == 'LegalCopyright':
                                        metadados['copyright'] = val_str

            try:
                pe.close()

            except Exception:
                pass

        except Exception as pe_error:
            logger.debug(f"pefile não conseguiu extrair versão/strings: {pe_error}", exc_info=True)

        try:
            metadados['assinado'] = verificar_assinatura_executavel(caminho)

        except Exception as sig_error:
            logger.error(f"Erro ao verificar assinatura: {sig_error}", exc_info=True)
            metadados['assinado'] = 'Erro'

    except Exception as sig_error:
        logger.error(f"Erro ao extrair metadados: {sig_error}", exc_info=True)
        metadados['assinado'] = 'Erro'

    return metadados

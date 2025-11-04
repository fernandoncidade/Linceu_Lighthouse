import os
import ctypes
from ctypes import wintypes


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

    result = WinVerifyTrust(
        None,
        ctypes.byref(WINTRUST_ACTION_GENERIC_VERIFY_V2),
        ctypes.byref(trust_data)
    )

    if result == 0:
        return "Sim"

    elif result == 0x800B0100:
        return "Não"

    else:
        return "Erro"

def extrair_metadados_executavel(caminho, loc=None):
    metadados = {}

    if not os.path.exists(caminho):
        return metadados

    try:
        with open(caminho, 'rb') as f:
            header = f.read(2)
            if header != b'MZ':
                print(f"Arquivo {caminho} não é um executável válido (cabeçalho não encontrado)")
                return metadados

    except Exception as e:
        print(f"Erro ao verificar cabeçalho do arquivo: {e}")
        return metadados

    try:
        import pefile
        import win32api

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

                    except:
                        pass

                if 'FileVersion' in str_info:
                    metadados['versao'] = str_info['FileVersion']

                else:
                    metadados['versao'] = versao

                if 'CompanyName' in str_info:
                    metadados['empresa'] = str_info['CompanyName']

                if 'FileDescription' in str_info:
                    metadados['descricao'] = str_info['FileDescription']

                if 'ProductName' in str_info:
                    metadados['produto'] = str_info['ProductName']

                if 'LegalCopyright' in str_info:
                    metadados['copyright'] = str_info['LegalCopyright']

            except Exception as e:
                print(f"Erro ao extrair strings de versão: {e}")
                metadados['versao'] = versao

        except Exception as e:
            if "1813" in str(e) or "Não foi possível encontrar o tipo de recurso" in str(e):
                print(f"Arquivo {os.path.basename(caminho)} não possui informações de versão incorporadas")
                metadados['versao'] = 'Não disponível'

            else:
                print(f"Erro com win32api: {e}")

            try:
                pe = pefile.PE(caminho)
                if hasattr(pe, 'VS_FIXEDFILEINFO'):
                    info = pe.VS_FIXEDFILEINFO
                    versao = f"{info.FileVersionMS >> 16}.{info.FileVersionMS & 0xFFFF}.{info.FileVersionLS >> 16}.{info.FileVersionLS & 0xFFFF}"
                    metadados['versao'] = versao

                if hasattr(pe, 'FileInfo'):
                    for fileinfo in pe.FileInfo:
                        for entry in fileinfo:
                            if hasattr(entry, 'StringTable'):
                                for st in entry.StringTable:
                                    for key, value in st.entries.items():
                                        key_str = key.decode('utf-8', errors='ignore')
                                        val_str = value.decode('utf-8', errors='ignore')
                                        if key_str == 'FileVersion':
                                            metadados['versao'] = val_str

                                        elif key_str == 'CompanyName':
                                            metadados['empresa'] = val_str

                                        elif key_str == 'FileDescription':
                                            metadados['descricao'] = val_str

                                        elif key_str == 'ProductName':
                                            metadados['produto'] = val_str

                pe.close()

            except Exception as pe_error:
                print(f"Erro com pefile: {pe_error}")

        try:
            metadados['assinado'] = verificar_assinatura_executavel(caminho)

        except Exception as sig_error:
            print(f"Erro ao verificar assinatura: {sig_error}")
            metadados['assinado'] = 'Erro'

    except Exception as sig_error:
        print(f"Erro ao extrair metadados: {sig_error}")
        metadados['assinado'] = 'Erro'

    return metadados

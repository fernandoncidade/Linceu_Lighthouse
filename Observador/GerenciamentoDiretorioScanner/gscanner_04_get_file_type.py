import os
from PySide6.QtCore import QCoreApplication

def get_file_type(self, caminho):
    if not caminho or not os.path.exists(caminho):
        return ""

    if os.path.isdir(caminho):
        return self.observador.loc.get_text("folder")

    ext = os.path.splitext(caminho)[1].lower()

    TIPOS_ARQUIVO = {
        # Documentos
        '.pdf': 'pdf', '.doc': 'doc', '.docx': 'docx', '.dotx': 'dotx', '.docm': 'docm', '.dotm': 'dotm',
        '.msg': 'msg', '.pst': 'pst', '.ost': 'ost', '.pub': 'pub', '.tex': 'tex', '.latex': 'latex', '.djvu': 'djvu',
        '.epub': 'epub', '.fb2': 'fb2', '.mobi': 'mobi', '.azw': 'azw', '.tsv': 'tsv', '.rtfd': 'rtfd',
        '.abw': 'abw', '.sxw': 'sxw', '.sdw': 'sdw', '.gdoc': 'gdoc', '.gslides': 'gslides', '.gdraw': 'gdraw',
        '.gtable': 'gtable', '.gform': 'gform', '.gmap': 'gmap', '.xps': 'xps', '.oxps': 'oxps', '.lit': 'lit',
        '.prc': 'prc', '.pdb': 'pdb', '.ps': 'ps', '.psw': 'psw', '.log': 'log', '.nfo': 'nfo', '.me': 'me',
        '.1st': '1st', '.srt': 'srt', '.sub': 'sub', '.lrc': 'lrc', '.dvi': 'dvi', '.ans': 'ans', '.azw3': 'azw3',
        '.ceb': 'ceb', '.chm': 'chm', '.cwk': 'cwk', '.dox': 'dox', '.eml': 'eml', '.etf': 'etf', '.ibooks': 'ibooks',
        '.kwd': 'kwd', '.lwp': 'lwp', '.mbp': 'mbp', '.mcw': 'mcw', '.nb': 'nb', '.odm': 'odm', '.pml': 'pml',
        '.sdw': 'sdw', '.stw': 'stw', '.tcr': 'tcr', '.wn': 'wn', '.wps': 'wps', '.zrtf': 'zrtf', '.asc': 'asc',
        '.ascii': 'ascii', '.bib': 'bib', '.diz': 'diz', '.err': 'err', '.exc': 'exc', '.faq': 'faq', '.idx': 'idx',
        '.info': 'info', '.man': 'man', '.readme': 'readme', '.rel': 'rel', '.sig': 'sig', '.uue': 'uue', '.vcf': 'vcf',
        '.vcard': 'vcard', '.wp': 'wp', '.wp5': 'wp5', '.wp6': 'wp6', '.wri': 'wri',

        # Planilhas
        '.xls': 'xls', '.xlsx': 'xlsx', '.xlsm': 'xlsm', '.ods': 'ods', '.numbers': 'numbers', '.xltx': 'xltx',
        '.xltm': 'xltm', '.xlsb': 'xlsb', '.xlr': 'xlr', '.xlt': 'xlt', '.xml': 'xml', '.sxc': 'sxc', '.slk': 'slk',
        '.dif': 'dif', '.prn': 'prn', '.gsheet': 'gsheet', '.123': '123', '.wk1': 'wk1', '.wk3': 'wk3', '.wk4': 'wk4',
        '.wks': 'wks', '.wb1': 'wb1', '.wb2': 'wb2', '.wb3': 'wb3', '.ab2': 'ab2', '.ab3': 'ab3', '.aws': 'aws',
        '.csv': 'csv', '.bcsv': 'bcsv', '.clf': 'clf', '.et': 'et', '.fm': 'fm', '.gnumeric': 'gnumeric', '.mar': 'mar',
        '.nmbtemplate': 'nmbtemplate', '.qpw': 'qpw', '.sdc': 'sdc', '.stc': 'stc', '.vc': 'vc', '.xlw': 'xlw',

        # Apresentações
        '.ppt': 'ppt', '.pptx': 'pptx', '.odp': 'odp', '.key': 'key', '.potx': 'potx', '.ppsx': 'ppsx',
        '.pptm': 'pptm', '.potm': 'potm', '.ppsm': 'ppsm', '.pps': 'pps', '.pot': 'pot', '.sxi': 'sxi',
        '.gslides': 'gslides', '.sti': 'sti', '.sdd': 'sdd', '.sdp': 'sdp', '.fods': 'fods', '.keynote': 'keynote',
        '.nb': 'nb', '.odg': 'odg', '.otp': 'otp', '.pez': 'pez', '.shf': 'shf', '.show': 'show', '.sxd': 'sxd',
        '.watch': 'watch',

        # Banco de dados
        '.dat': 'dat', '.db': 'db', '.sqlite': 'sqlite', '.mdb': 'mdb', '.accdb': 'accdb', '.sav': 'sav',
        '.spss': 'spss', '.db-journal': 'db-journal', '.sql': 'sql', '.dbf': 'dbf', '.ndb': 'ndb', '.frm': 'frm',
        '.myd': 'myd', '.myi': 'myi', '.sqlite3': 'sqlite3', '.sl3': 'sl3', '.sdb': 'sdb', '.cdb': 'cdb',
        '.pdb': 'pdb', '.gdb': 'gdb', '.ora': 'ora', '.dmp': 'dmp', '.par': 'par', '.mdf': 'mdf', '.ldf': 'ldf',
        '.idb': 'idb', '.ibd': 'ibd', '.sqlite2': 'sqlite2', '.4db': '4db', '.4dd': '4dd', '.adf': 'adf',
        '.adp': 'adp', '.alf': 'alf', '.ask': 'ask', '.btr': 'btr', '.cat': 'cat', '.daconnections': 'daconnections',
        '.daschema': 'daschema', '.db2': 'db2', '.db3': 'db3', '.dbc': 'dbc', '.kexi': 'kexi', '.kexic': 'kexic',
        '.kexis': 'kexis', '.lirs': 'lirs', '.ndf': 'ndf', '.nwdb': 'nwdb', '.pan': 'pan', '.pdm': 'pdm',
        '.pdi': 'pdi', '.pnz': 'pnz', '.rpd': 'rpd', '.rsd': 'rsd', '.sbf': 'sbf', '.sds': 'sds', '.sqlitedb': 'sqlitedb',
        '.udl': 'udl', '.wdb': 'wdb', '.abs': 'abs', '.abx': 'abx', '.adb': 'adb', '.dta': 'dta',

        # Imagens
        '.jpg': 'jpg', '.jpeg': 'jpeg', '.png': 'png', '.gif': 'gif', '.bmp': 'bmp', '.tiff': 'tiff', '.tif': 'tif',
        '.psd': 'psd', '.webp': 'webp', '.raw': 'raw', '.heic': 'heic', '.heif': 'heif', '.cr2': 'cr2', '.nef': 'nef',
        '.arw': 'arw', '.ico': 'ico', '.svg': 'svg', '.ai': 'ai', '.indd': 'indd', '.eps': 'eps', '.jfif': 'jfif',
        '.dib': 'dib', '.pbm': 'pbm', '.pgm': 'pgm', '.ppm': 'ppm', '.xbm': 'xbm', '.xpm': 'xpm', '.dds': 'dds',
        '.emf': 'emf', '.wmf': 'wmf', '.apng': 'apng', '.avif': 'avif', '.exr': 'exr', '.hdr': 'hdr', '.icns': 'icns',
        '.jpe': 'jpe', '.jif': 'jif', '.jxr': 'jxr', '.pcx': 'pcx', '.pic': 'pic', '.pct': 'pct', '.ras': 'ras',
        '.sgi': 'sgi', '.sun': 'sun', '.viff': 'viff', '.wbmp': 'wbmp', '.3fr': '3fr', '.ari': 'ari', '.bay': 'bay',
        '.cap': 'cap', '.cin': 'cin', '.dcr': 'dcr', '.dng': 'dng', '.erf': 'erf', '.fff': 'fff', '.gpr': 'gpr',
        '.iiq': 'iiq', '.k25': 'k25', '.kdc': 'kdc', '.mdc': 'mdc', '.mef': 'mef', '.mos': 'mos', '.mrw': 'mrw',
        '.nrw': 'nrw', '.orf': 'orf', '.pef': 'pef', '.ptx': 'ptx', '.pxn': 'pxn', '.r3d': 'r3d', '.raf': 'raf',
        '.rwl': 'rwl', '.rw2': 'rw2', '.sr2': 'sr2', '.srf': 'srf', '.srw': 'srw', '.x3f': 'x3f', '.art': 'art',
        '.bpg': 'bpg', '.cd5': 'cd5', '.cpt': 'cpt', '.dpx': 'dpx', '.ecw': 'ecw', '.fpx': 'fpx', '.jbig': 'jbig',
        '.jp2': 'jp2', '.jps': 'jps', '.mpo': 'mpo', '.pat': 'pat', '.tga': 'tga', '.vtf': 'vtf', '.cif': 'cif',
        '.cmyk': 'cmyk', '.dcx': 'dcx', '.djvu': 'djvu', '.drw': 'drw', '.fig': 'fig', '.flc': 'flc', '.fli': 'fli',
        '.flic': 'flic', '.fits': 'fits', '.gbr': 'gbr', '.iff': 'iff', '.lbm': 'lbm', '.mac': 'mac', '.mng': 'mng',
        '.msp': 'msp', '.nitf': 'nitf', '.otb': 'otb', '.pcd': 'pcd', '.pict': 'pict', '.pjpeg': 'pjpeg', '.psb': 'psb',
        '.qti': 'qti', '.qtif': 'qtif', '.rgb': 'rgb', '.rgba': 'rgba', '.rle': 'rle', '.sid': 'sid', '.targa': 'targa',
        '.xwd': 'xwd',

        # Áudio
        '.wav': 'wav', '.mp3': 'mp3', '.aac': 'aac', '.flac': 'flac', '.ogg': 'ogg', '.aiff': 'aiff', '.wma': 'wma',
        '.m4a': 'm4a', '.aif': 'aif', '.au': 'au', '.snd': 'snd', '.mid': 'mid', '.midi': 'midi', '.rmi': 'rmi',
        '.mpa': 'mpa', '.mpc': 'mpc', '.ape': 'ape', '.wv': 'wv', '.opus': 'opus', '.spx': 'spx', '.amr': 'amr',
        '.3ga': '3ga', '.cda': 'cda', '.ac3': 'ac3', '.adt': 'adt', '.adts': 'adts', '.mka': 'mka', '.mp1': 'mp1',
        '.mp2': 'mp2', '.oga': 'oga', '.ra': 'ra', '.ram': 'ram', '.s3m': 's3m', '.stm': 'stm', '.voc': 'voc',
        '.vqf': 'vqf', '.w64': 'w64', '.xm': 'xm', '.669': '669', '.aifc': 'aifc', '.amf': 'amf', '.ams': 'ams',
        '.dbm': 'dbm', '.dmf': 'dmf', '.dsm': 'dsm', '.far': 'far', '.it': 'it', '.mptm': 'mptm', '.mt2': 'mt2',
        '.psm': 'psm', '.ult': 'ult', '.umx': 'umx', '.xi': 'xi', '.aa': 'aa', '.aax': 'aax', '.act': 'act',
        '.ahx': 'ahx', '.aup': 'aup', '.caf': 'caf', '.dss': 'dss', '.dvf': 'dvf', '.gsm': 'gsm', '.iklax': 'iklax',
        '.ivs': 'ivs', '.m4b': 'm4b', '.m4p': 'm4p', '.mmf': 'mmf', '.mpga': 'mpga', '.msv': 'msv', '.nmf': 'nmf',
        '.qcp': 'qcp', '.sln': 'sln', '.tta': 'tta', '.vox': 'vox',

        # Vídeo
        '.mp4': 'mp4', '.mov': 'mov', '.avi': 'avi', '.mkv': 'mkv', '.wmv': 'wmv', '.flv': 'flv', '.webm': 'webm',
        '.mts': 'mts', '.m2ts': 'm2ts', '.mpeg': 'mpeg', '.m4v': 'm4v', '.3gp': '3gp', '.3g2': '3g2', '.rm': 'rm',
        '.rmvb': 'rmvb', '.vob': 'vob', '.ogv': 'ogv', '.ts': 'ts', '.mpe': 'mpe', '.mpg': 'mpg', '.asf': 'asf',
        '.f4v': 'f4v', '.mxf': 'mxf', '.yuv': 'yuv', '.divx': 'divx', '.dv': 'dv', '.svi': 'svi', '.amv': 'amv',
        '.drc': 'drc', '.mng': 'mng', '.qt': 'qt', '.nsv': 'nsv', '.nut': 'nut', '.ogm': 'ogm', '.smk': 'smk',
        '.bik': 'bik', '.trp': 'trp', '.vcd': 'vcd', '.vp6': 'vp6', '.vp7': 'vp7', '.avs': 'avs', '.bink': 'bink',
        '.dat': 'dat', '.dif': 'dif', '.ivf': 'ivf', '.m2v': 'm2v', '.mjp': 'mjp', '.roq': 'roq', '.str': 'str',
        '.vqa': 'vqa', '.y4m': 'y4m', '.h264': 'h264', '.h265': 'h265', '.hevc': 'hevc', '.264': '264', '.3gpp': '3gpp',
        '.amc': 'amc', '.cam': 'cam', '.ced': 'ced', '.dav': 'dav', '.dvr': 'dvr', '.f4p': 'f4p', '.gfp': 'gfp',
        '.gvi': 'gvi', '.h261': 'h261', '.ismv': 'ismv', '.jts': 'jts', '.m1v': 'm1v', '.m2p': 'm2p', '.mjpeg': 'mjpeg',
        '.mod': 'mod', '.moov': 'moov', '.mp2v': 'mp2v', '.mpv': 'mpv', '.ogx': 'ogx', '.pds': 'pds', '.pva': 'pva',
        '.qtvr': 'qtvr', '.rdb': 'rdb', '.rec': 'rec', '.rts': 'rts', '.scm': 'scm', '.tod': 'tod', '.tp': 'tp',
        '.vid': 'vid', '.vivo': 'vivo', '.vp8': 'vp8', '.vro': 'vro', '.wm': 'wm', '.wmp': 'wmp', '.wtv': 'wtv',
        '.xvid': 'xvid',

        # Executáveis
        '.exe': 'exe', '.dll': 'dll', '.bin': 'bin', '.app': 'app', '.apk': 'apk', '.msi': 'msi', '.run': 'run',
        '.bat': 'bat', '.cmd': 'cmd', '.pma': 'pma', '.pbtxt': 'pbtxt', '.binarypb': 'binarypb', '.tflite': 'tflite',
        '.fst': 'fst', '.otf': 'otf', '.ldb': 'ldb', '.leveldb': 'leveldb', '.blob': 'blob', '.lnk': 'lnk',
        '.hyb': 'hyb', '.msix': 'msix', '.com': 'com', '.scr': 'scr', '.jar': 'jar', '.wsf': 'wsf', '.vbs': 'vbs',
        '.gadget': 'gadget', '.pif': 'pif', '.cpl': 'cpl', '.sys': 'sys', '.drv': 'drv', '.bpl': 'bpl', '.ocx': 'ocx',
        '.so': 'so', '.out': 'out', '.elf': 'elf', '.a': 'a', '.dylib': 'dylib', '.prg': 'prg', '.appimage': 'appimage',
        '.ipa': 'ipa', '.deb': 'deb', '.rpm': 'rpm', '.pkg': 'pkg', '.msu': 'msu', '.cab': 'cab', '.bsp': 'bsp',
        '.mod': 'mod', '.xpi': 'xpi', '.crx': 'crx', '.xap': 'xap', '.action': 'action', '.cgi': 'cgi', '.dek': 'dek',
        '.ear': 'ear', '.ex_': 'ex_', '.ex4': 'ex4', '.fpi': 'fpi', '.fxp': 'fxp', '.gs': 'gs', '.ham': 'ham',
        '.ipf': 'ipf', '.isu': 'isu', '.jse': 'jse', '.mel': 'mel', '.mrc': 'mrc', '.ms': 'ms', '.mxe': 'mxe',
        '.o': 'o', '.obs': 'obs', '.paf.exe': 'paf.exe', '.phar': 'phar', '.pyc': 'pyc', '.pyo': 'pyo', '.rgs': 'rgs',
        '.scb': 'scb', '.scar': 'scar', '.scpt': 'scpt', '.sfx': 'sfx', '.shb': 'shb', '.u3p': 'u3p', '.udf': 'udf',
        '.upx': 'upx', '.vpm': 'vpm', '.widget': 'widget', '.workflow': 'workflow', '.ws': 'ws', '.zl9': 'zl9',

        # Código-fonte
        '.py': 'py', '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.h': 'h', '.hpp': 'hpp', '.cs': 'cs', '.js': 'js',
        '.html': 'html', '.htm': 'htm', '.mht': 'mht', '.xhtml': 'xhtml', '.mhtml': 'mhtml', '.css': 'css',
        '.php': 'php', '.sql': 'sql', '.json': 'json', '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yml', '.md': 'md',
        '.rst': 'rst', '.syms': 'syms', '.svg': 'svg', '.bat': 'bat', '.sh': 'sh', '.ps1': 'ps1', '.psm1': 'psm1',
        '.psd1': 'psd1', '.ps1xml': 'ps1xml', '.pssc': 'pssc', '.psc1': 'psc1', '.rb': 'rb', '.pl': 'pl', '.pm': 'pm',
        '.go': 'go', '.rs': 'rs', '.swift': 'swift', '.kt': 'kt', '.dart': 'dart', '.ts': 'ts', '.jsx': 'jsx',
        '.tsx': 'tsx', '.vb': 'vb', '.vbs': 'vbs', '.lua': 'lua', '.r': 'r', '.m': 'm', '.scala': 'scala',
        '.groovy': 'groovy', '.erl': 'erl', '.hs': 'hs', '.clj': 'clj', '.coffee': 'coffee', '.f90': 'f90',
        '.for': 'for', '.ada': 'ada', '.pas': 'pas', '.d': 'd', '.asm': 'asm', '.s': 's', '.v': 'v', '.vhdl': 'vhdl',
        '.tcl': 'tcl', '.scm': 'scm', '.lisp': 'lisp', '.pro': 'pro', '.db2': 'db2', '.cob': 'cob', '.jsp': 'jsp',
        '.asp': 'asp', '.aspx': 'aspx', '.inc': 'inc', '.hxx': 'hxx', '.cxx': 'cxx', '.cc': 'cc', '.mm': 'mm',
        '.mjs': 'mjs', '.fs': 'fs', '.fsx': 'fsx', '.fsi': 'fsi', '.ml': 'ml', '.mli': 'mli', '.cl': 'cl',
        '.cu': 'cu', '.ipynb': 'ipynb', '.jl': 'jl', '.nim': 'nim', '.vala': 'vala', '.cr': 'cr', '.hx': 'hx',
        '.ex': 'ex', '.exs': 'exs', '.elm': 'elm', '.purs': 'purs', '.rkt': 'rkt', '.ss': 'ss', '.sc': 'sc',
        '.sbt': 'sbt', '.kts': 'kts', '.psql': 'psql', '.prg': 'prg', '.abap': 'abap', '.ahk': 'ahk', '.au3': 'au3',
        '.bas': 'bas', '.cljs': 'cljs', '.e': 'e', '.ecl': 'ecl', '.el': 'el', '.fth': 'fth', '.gml': 'gml',
        '.ino': 'ino', '.l': 'l', '.lgt': 'lgt', '.lsp': 'lsp', '.n': 'n', '.p': 'p', '.pp': 'pp', '.red': 'red',
        '.sb2': 'sb2', '.sb3': 'sb3', '.scpt': 'scpt', '.vbscript': 'vbscript', '.y': 'y', '.cgi': 'cgi',
        '.fcgi': 'fcgi', '.plx': 'plx', '.pmc': 'pmc', '.pod': 'pod', '.psgi': 'psgi', '.phtml': 'phtml',

        # Compactados
        '.zip': 'zip', '.rar': 'rar', '.7z': '7z', '.tar': 'tar', '.gz': 'gz', '.bz2': 'bz2', '.xz': 'xz', '.cab': 'cab',
        '.pb': 'pb', '.pb.gz': 'pb.gz', '.tgz': 'tgz', '.tar.gz': 'tar.gz', '.tar.bz2': 'tar.bz2', '.tar.xz': 'tar.xz',
        '.ace': 'ace', '.arj': 'arj', '.lzh': 'lzh', '.lha': 'lha', '.z': 'z', '.jar': 'jar', '.war': 'war', '.ear': 'ear',
        '.apk': 'apk', '.deb': 'deb', '.rpm': 'rpm', '.pkg': 'pkg', '.img': 'img', '.iso': 'iso', '.dmg': 'dmg',
        '.cso': 'cso', '.hqx': 'hqx', '.sit': 'sit', '.sitx': 'sitx', '.bin': 'bin', '.cue': 'cue', '.001': '001',
        '.002': '002', '.alz': 'alz', '.arc': 'arc', '.ark': 'ark', '.b1': 'b1', '.ba': 'ba', '.bh': 'bh', '.car': 'car',
        '.cbr': 'cbr', '.cbz': 'cbz', '.pak': 'pak', '.partimg': 'partimg', '.pea': 'pea', '.s7z': 's7z', '.sen': 'sen',
        '.tbz2': 'tbz2', '.tlz': 'tlz', '.uc2': 'uc2', '.uha': 'uha', '.wim': 'wim', '.xar': 'xar', '.zipx': 'zipx',
        '.a00': 'a00', '.a01': 'a01', '.a02': 'a02', '.ain': 'ain', '.apa': 'apa', '.cfs': 'cfs', '.dar': 'dar',
        '.dd': 'dd', '.egg': 'egg', '.ess': 'ess', '.f': 'f', '.gbs': 'gbs', '.gza': 'gza', '.ha': 'ha', '.ice': 'ice',
        '.ipg': 'ipg', '.kgb': 'kgb', '.lbr': 'lbr', '.lqr': 'lqr', '.lz': 'lz', '.lzo': 'lzo', '.lzx': 'lzx',
        '.mbw': 'mbw', '.mpq': 'mpq', '.nth': 'nth', '.p7m': 'p7m', '.part': 'part', '.puz': 'puz', '.r00': 'r00',
        '.r01': 'r01', '.r02': 'r02', '.rk': 'rk', '.sda': 'sda', '.sea': 'sea', '.sfx': 'sfx', '.shk': 'shk',
        '.shar': 'shar', '.shr': 'shr', 'tar.z': 'tar.z', '.taz': 'taz', '.tbz': 'tbz', '.uc': 'uc', '.vsi': 'vsi',
        '.wad': 'wad', '.xef': 'xef', '.zlib': 'zlib', '.zoo': 'zoo',

        # Backup
        '.bak': 'bak', '.bkp': 'bkp', '.backup': 'backup', '.old': 'old', '.orig': 'orig', '.save': 'save',
        '.sav': 'sav', '.auto': 'auto', '.abk': 'abk', '.arc': 'arc', '.gho': 'gho', '.ibackup': 'ibackup',
        '.tib': 'tib', '.bkf': 'bkf', '.bup': 'bup', '.swm': 'swm', '.sna': 'sna', '.sn1': 'sn1', '.sn2': 'sn2',
        '.sn3': 'sn3', '.wbk': 'wbk', '.mbk': 'mbk', '.sbk': 'sbk', '.fbk': 'fbk', '.rbk': 'rbk', '.~bk': '~bk',
        '.$bk': '$bk', '.$$$': '$$$', '.@@@': '@@@', '.b@k': 'b@k', '.bac': 'bac', '.sik': 'sik', '.tmp': 'tmp',

        # Log
        '.log': 'log', '.trace': 'trace', '.dmp': 'dmp', '.dump': 'dump', '.hprof': 'hprof', '.core': 'core',
        '.err': 'err', '.out': 'out', '.blg': 'blg', '.etl': 'etl', '.evtx': 'evtx', '.glog': 'glog', '.lst': 'lst',
        '.prn': 'prn', '.trc': 'trc', '.wrn': 'wrn', '.clg': 'clg', '.audit': 'audit', '.journal': 'journal',
        '.lg': 'lg', '.txt': 'txt', '.dat': 'dat', '.svclog': 'svclog', '.history': 'history', '.evt': 'evt',

        # Configuração
        '.ini': 'ini', '.cfg': 'cfg', '.config': 'config', '.conf': 'conf', '.properties': 'properties',
        '.plist': 'plist', '.toml': 'toml', '.settings': 'settings', '.rc': 'rc', '.json': 'json', '.yaml': 'yaml',
        '.yml': 'yml', '.env': 'env', '.desktop': 'desktop', '.profile': 'profile', '.bashrc': 'bashrc',
        '.zshrc': 'zshrc', '.cshrc': 'cshrc', '.login': 'login', '.logout': 'logout', '.npmrc': 'npmrc',
        '.editorconfig': 'editorconfig', '.cf': 'cf', '.cnf': 'cnf', '.inf': 'inf', '.reg': 'reg', '.scr': 'scr',
        '.sys': 'sys', '.xml': 'xml', '.prefs': 'prefs', '.opt': 'opt', '.options': 'options', '.DS_Store': 'DS_Store',
        '.gitconfig': 'gitconfig', '.htaccess': 'htaccess', '.htpasswd': 'htpasswd', '.manifest': 'manifest',
        '.pro': 'pro', '.props': 'props', '.sln': 'sln', '.user': 'user', '.vcxproj': 'vcxproj', '.xcu': 'xcu',
        '.xmc': 'xmc',

        # Fontes
        '.fnt': 'fnt', '.fon': 'fon', '.otf': 'otf', '.ttf': 'ttf', '.dfont': 'dfont', '.eot': 'eot', '.pfb': 'pfb',
        '.pfm': 'pfm', '.woff': 'woff', '.woff2': 'woff2', '.afm': 'afm', '.bdf': 'bdf', '.pcf': 'pcf', '.snf': 'snf',

        # Sistema
        '.acm': 'acm', '.ax': 'ax', '.bpl': 'bpl', '.com': 'com', '.cpl': 'cpl', '.cur': 'cur', '.ani': 'ani',
        '.drv': 'drv', '.ds': 'ds', '.efi': 'efi', '.grd': 'grd', '.icl': 'icl', '.ime': 'ime', '.job': 'job',
        '.kbd': 'kbd', '.mui': 'mui', '.nls': 'nls', '.rom': 'rom', '.rsrc': 'rsrc', '.sdi': 'sdi', '.sfc': 'sfc',
        '.spl': 'spl', '.sve': 'sve', '.theme': 'theme', '.vxd': 'vxd', '.win': 'win',

        # GIS
        '.shp': 'shp', '.shx': 'shx', '.dbf': 'dbf', '.prj': 'prj', '.sbn': 'sbn', '.sbx': 'sbx', '.gpx': 'gpx',
        '.kml': 'kml', '.kmz': 'kmz', '.geojson': 'geojson', '.topojson': 'topojson', '.gdb': 'gdb', '.mxd': 'mxd',
        '.aprx': 'aprx', '.lyr': 'lyr', '.lyrx': 'lyrx', '.qgs': 'qgs', '.qgz': 'qgz', '.mbtiles': 'mbtiles',
        '.geotiff': 'geotiff', '.las': 'las', '.laz': 'laz',

        # Disco virtual
        '.vdi': 'vdi', '.vhd': 'vhd', '.vhdx': 'vhdx', '.vmdk': 'vmdk', '.hdd': 'hdd', '.hds': 'hds', '.pvm': 'pvm',
        '.qcow': 'qcow', '.qcow2': 'qcow2', '.qed': 'qed', '.vbox': 'vbox', '.vbox-prev': 'vbox-prev',

        # Temporários
        '.tmp': 'tmp', '.temp': 'temp', '.~': '~', '.swp': 'swp', '.swo': 'swo', '.$$': '$$', '.old': 'old',
        '.part': 'part', '.cache': 'cache', '.crdownload': 'crdownload', '.download': 'download', '.partial': 'partial',
        '.lock': 'lock', '.thumb': 'thumb', '.TMP': 'tmp', '.TEMP': 'temp'
    }

    tipo = TIPOS_ARQUIVO.get(ext, "")
    if tipo:
        try:
            traducao = QCoreApplication.translate("LinceuLighthouse", tipo)
            if traducao and traducao != tipo:
                return traducao

        except Exception:
            pass

    if tipo and hasattr(self.observador.loc, "get_text"):
        return tipo

    return tipo

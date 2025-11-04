import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def identificar_tipo_arquivo(caminho, loc, nome_arquivo=None):
    try:
        if nome_arquivo is None:
            nome_arquivo = os.path.basename(caminho)

        ext = os.path.splitext(nome_arquivo)[1]

        if ext.lower() == '.tmp' or ext.upper() == '.TMP':
            return "tmp"

        TIPOS_TEMPORARIOS = {'.tmp', '.temp', '.~', '.swp', '.swo', '.$$', '.old', '.part', 
                            '.cache', '.crdownload', '.download', '.partial', '.lock', '.thumb',
                            '.TMP', '.TEMP'}

        if ext.lower() in TIPOS_TEMPORARIOS or \
        nome_arquivo.lower().startswith(("~", "._", ".#", "~$")) or \
        nome_arquivo.lower().endswith(("~", ".lock")) or \
        "temp-index" in nome_arquivo.lower() or \
        "~index" in nome_arquivo.lower() or \
        "thumb" in nome_arquivo.lower():
            return ext[1:].lower() if ext else ""

        TIPOS_IMAGEM = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.psd', '.webp', '.raw', '.heic', '.heif',
            '.cr2', '.nef', '.arw', '.ico', '.svg', '.ai', '.indd', '.eps', '.jfif', '.dib', '.pbm', '.pgm', '.ppm',
            '.xbm', '.xpm', '.dds', '.emf', '.wmf', '.apng', '.avif', '.exr', '.hdr', '.icns', '.jpe', '.jif', '.jxr',
            '.pcx', '.pic', '.pct', '.ras', '.sgi', '.sun', '.viff', '.wbmp', '.3fr', '.ari', '.bay', '.cap', '.cin',
            '.dcr', '.dng', '.erf', '.fff', '.gpr', '.iiq', '.k25', '.kdc', '.mdc', '.mef', '.mos', '.mrw', '.nrw',
            '.orf', '.pef', '.ptx', '.pxn', '.r3d', '.raf', '.rwl', '.rw2', '.sr2', '.srf', '.srw', '.x3f', '.art',
            '.bpg', '.cd5', '.cpt', '.dpx', '.ecw', '.fpx', '.jbig', '.jp2', '.jps', '.mpo', '.pat', '.tga', '.vtf',
            '.cif', '.cmyk', '.dcx', '.djvu', '.drw', '.fig', '.flc', '.fli', '.flic', '.fits', '.gbr', '.iff', '.lbm',
            '.mac', '.mng', '.msp', '.nitf', '.otb', '.pcd', '.pict', '.pjpeg', '.psb', '.qti', '.qtif', '.rgb', '.rgba',
            '.rle', '.sid', '.targa', '.xwd'
        }
        TIPOS_AUDIO = {
            '.wav', '.mp3', '.aac', '.flac', '.ogg', '.aiff', '.wma', '.m4a', '.aif', '.au', '.snd', '.mid', '.midi',
            '.rmi', '.mpa', '.mpc', '.ape', '.wv', '.opus', '.spx', '.amr', '.3ga', '.cda', '.ac3', '.adt', '.adts',
            '.mka', '.mp1', '.mp2', '.oga', '.ra', '.ram', '.s3m', '.stm', '.voc', '.vqf', '.w64', '.xm', '.669',
            '.aifc', '.amf', '.ams', '.dbm', '.dmf', '.dsm', '.far', '.it', '.mptm', '.mt2', '.psm', '.ult', '.umx', '.xi',
            '.aa', '.aax', '.act', '.ahx', '.aup', '.caf', '.dss', '.dvf', '.gsm', '.iklax', '.ivs', '.m4b', '.m4p',
            '.mmf', '.mpga', '.msv', '.nmf', '.oga', '.qcp', '.sln', '.tta', '.vox'
        }
        TIPOS_VIDEO = {
            '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mts', '.m2ts', '.mpeg', '.m4v', '.3gp', '.3g2',
            '.rm', '.rmvb', '.vob', '.ogv', '.ts', '.mpe', '.mpg', '.asf', '.f4v', '.mxf', '.yuv', '.divx', '.dv', '.svi',
            '.amv', '.drc', '.mng', '.qt', '.nsv', '.nut', '.ogm', '.smk', '.bik', '.trp', '.vcd', '.vp6', '.vp7', '.avs',
            '.bink', '.dat', '.dif', '.ivf', '.m2v', '.mjp', '.roq', '.str', '.vqa', '.y4m', '.h264', '.h265', '.hevc',
            '.264', '.3gpp', '.amc', '.avs', '.cam', '.ced', '.dav', '.dvr', '.f4p', '.f4v', '.gfp', '.gvi', '.h261',
            '.ismv', '.jts', '.m1v', '.m2p', '.mjpeg', '.mod', '.moov', '.mp2v', '.mpv', '.ogx', '.pds', '.pva', '.qtvr',
            '.rdb', '.rec', '.rts', '.scm', '.tod', '.tp', '.vid', '.vivo', '.vp8', '.vro', '.wm', '.wmp', '.wtv', '.xvid'
        }
        TIPOS_CODIGO_FONTE = {
            '.py', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.js', '.html', '.htm', '.mht', '.xhtml', '.mhtml', '.css',
            '.php', '.sql', '.json', '.xml', '.yaml', '.yml', '.md', '.rst', '.syms', '.svg', '.bat', '.sh', '.ps1',
            '.psm1', '.psd1', '.ps1xml', '.pssc', '.psc1', '.rb', '.pl', '.pm', '.go', '.rs', '.swift', '.kt', '.dart',
            '.ts', '.jsx', '.tsx', '.vb', '.vbs', '.lua', '.r', '.m', '.scala', '.groovy', '.erl', '.hs', '.clj', '.coffee',
            '.f90', '.for', '.ada', '.pas', '.d', '.asm', '.s', '.v', '.vhdl', '.tcl', '.scm', '.lisp', '.pro',
            '.db2', '.cob', '.jsp', '.asp', '.aspx', '.inc', '.hxx', '.cxx', '.cc', '.mm', '.mjs', '.fs',
            '.fsx', '.fsi', '.ml', '.mli', '.cl', '.cu', '.ipynb', '.jl', '.nim', '.vala', '.cr', '.hx', '.ex',
            '.exs', '.elm', '.purs', '.rkt', '.ss', '.sc', '.sbt', '.kts', '.psql', '.prg', '.abap', '.ahk', '.au3',
            '.bas', '.cljs', '.e', '.ecl', '.el', '.fth', '.gml', '.ino', '.l', '.lgt', '.lsp', '.n', '.p', '.pp', '.red',
            '.sb2', '.sb3', '.scpt', '.vbscript', '.y', '.cgi', '.fcgi', '.plx', '.pmc', '.pod', '.psgi', '.phtml'
        }
        TIPOS_DOCUMENTO = {
            '.doc', '.docx', '.pdf', '.rtf', '.txt', '.odt', '.wpd', '.pages', '.map', '.md5', '.dotx', '.docm', '.dotm',
            '.msg', '.pst', '.ost', '.pub', '.tex', '.latex', '.djvu', '.epub', '.fb2', '.mobi', '.azw', '.tsv',
            '.rtfd', '.abw', '.sxw', '.sdw', '.gdoc', '.gslides', '.gdraw', '.gtable', '.gform', '.gmap', '.xps', '.oxps',
            '.lit', '.prc', '.pdb', '.ps', '.psw', '.log', '.nfo', '.me', '.1st', '.srt', '.sub', '.lrc', '.dvi', '.ans',
            '.azw3', '.ceb', '.chm', '.cwk', '.dox', '.eml', '.etf', '.ibooks', '.kwd', '.lwp', '.mbp', '.mcw', '.nb',
            '.odm', '.pml', '.sdw', '.stw', '.tcr', '.wn', '.wps', '.zrtf', '.asc', '.ascii', '.bib', '.diz', '.err',
            '.exc', '.faq', '.idx', '.info', '.man', '.readme', '.rel', '.sig', '.uue', '.vcf', '.vcard', '.wp', '.wp5', '.wp6', '.wri'
        }
        TIPOS_PLANILHA = {
            '.xls', '.xlsx', '.xlsm', '.ods', '.csv', '.tsv', '.numbers', '.xltx', '.xltm', '.xlsb', '.xlr', '.xlt', '.xml',
            '.sxc', '.slk', '.dif', '.prn', '.gsheet', '.123', '.wk1', '.wk3', '.wk4', '.wks', '.wb1', '.wb2', '.wb3',
            '.ab2', '.ab3', '.aws', '.bcsv', '.clf', '.et', '.fm', '.gnumeric', '.mar', '.nmbtemplate', '.qpw', '.sdc', '.stc', '.vc', '.xlw'
        }
        TIPOS_APRESENTACAO = {
            '.ppt', '.pptx', '.odp', '.key', '.potx', '.ppsx', '.pptm', '.potm', '.ppsm', '.pps', '.pot', '.sxi', '.gslides',
            '.sti', '.sdd', '.sdp', '.fods', '.keynote', '.nb', '.odg', '.otp', '.pez', '.shf', '.show', '.sxd', '.watch'
        }
        TIPOS_BANCO_DADOS = {
            '.dat', '.db', '.sqlite', '.mdb', '.accdb', '.sav', '.spss', '.db-journal', '.sql', '.dbf', '.ndb', '.frm',
            '.myd', '.myi', '.sqlite3', '.sl3', '.sdb', '.cdb', '.pdb', '.gdb', '.ora', '.dmp', '.par', '.mdf', '.ldf',
            '.idb', '.ibd', '.sqlite2', '.4db', '.4dd', '.adf', '.adp', '.alf', '.ask', '.btr', '.cat', '.daconnections',
            '.daschema', '.db2', '.db3', '.dbc', '.kexi', '.kexic', '.kexis', '.lirs', '.ndf', '.nwdb', '.pan', '.pdm',
            '.pdi', '.pnz', '.rpd', '.rsd', '.sbf', '.sds', '.sqlitedb', '.udl', '.wdb', '.abs', '.abx', '.adb', '.dta'
        }
        TIPOS_EXECUTAVEIS = {
            '.exe', '.dll', '.bin', '.app', '.apk', '.msi', '.run', '.bat', '.cmd', '.pma', '.pbtxt', '.binarypb', '.tflite',
            '.fst', '.otf', '.ldb', '.leveldb', '.blob', '.lnk', '.hyb', '.msix', '.com', '.scr', '.jar', '.wsf', '.vbs',
            '.gadget', '.pif', 'cpl', '.sys', '.drv', '.bpl', '.ocx', '.so', '.out', '.elf', '.a', '.dylib', '.prg',
            '.appimage', '.ipa', '.deb', '.rpm', '.pkg', '.msu', '.cab', '.bsp', '.mod', '.xpi', '.crx', '.xap', '.action',
            '.cgi', '.dek', '.ear', '.ex_', '.ex4', '.fpi', '.fxp', '.gs', '.ham', '.ipf', '.isu', '.jse', '.mel', '.mrc',
            '.ms', '.mxe', '.o', '.obs', '.paf.exe', '.phar', '.pyc', '.pyo', '.rgs', '.scb', '.scar', '.scpt', '.sfx',
            '.shb', '.u3p', '.udf', '.upx', '.vpm', '.widget', '.workflow', '.ws', '.zl9'
        }
        TIPOS_COMPACTADOS = {
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.cab', '.pb', '.pb.gz', '.tgz', '.tar.gz', '.tar.bz2',
            '.tar.xz', '.ace', '.arj', '.lzh', '.lha', '.z', '.jar', '.war', '.ear', '.apk', '.deb', '.rpm', '.pkg', '.img',
            '.iso', '.dmg', '.cso', '.hqx', '.sit', '.sitx', '.bin', '.cue', '.001', '.002', '.alz', '.arc', '.ark', '.b1',
            '.ba', '.bh', '.car', '.cbr', '.cbz', '.pak', '.partimg', '.pea', '.s7z', '.sen', '.tbz2',
            '.tlz', '.uc2', '.uha', '.wim', '.xar', '.zipx', '.a00', '.a01', '.a02', '.ain', '.apa', '.cfs', '.dar', '.dd',
            '.egg', '.ess', '.f', '.gbs', '.gza', '.ha', '.ice', '.ipg', '.kgb', '.lbr', '.lqr', '.lz', '.lzo', '.lzx',
            '.mbw', '.mpq', '.nth', '.p7m', '.part', '.puz', '.r00', '.r01', '.r02', '.rk', '.sda', '.sea', '.sfx',
            '.shk', '.shar', '.shr', 'tar.z', '.taz', '.tbz', '.uc', '.vsi', '.wad', '.xef', '.zlib', '.zoo'
        }
        TIPOS_BACKUP = {
            '.bak', '.bkp', '.backup', '.old', '.orig', '.save', '.sav', '.auto', '.abk', '.arc', '.gho', '.ibackup',
            '.tib', '.bkf', '.bup', '.swm', '.sna', '.sn1', '.sn2', '.sn3', '.wbk', '.mbk', '.sbk', '.fbk', '.rbk',
            '.~bk', '.$bk', '.$$$', '.@@@', '.b@k', '.bac', '.sik', '.tmp'
        }
        TIPOS_LOG = {
            '.log', '.trace', '.dmp', '.dump', '.hprof', '.core', '.err', '.out', '.blg', '.etl', '.evtx', '.glog', '.lst',
            '.prn', '.trc', '.wrn', '.clg', '.audit', '.journal', '.lg', '.txt', '.dat', '.svclog', '.history', '.evt'
        }
        TIPOS_CONFIGURACAO = {
            '.ini', '.cfg', '.config', '.conf', '.properties', '.plist', '.toml', '.settings', '.rc', '.json', '.yaml',
            '.yml', '.env', '.desktop', '.profile', '.bashrc', '.zshrc', '.cshrc', '.login', '.logout', '.npmrc', '.editorconfig',
            '.cf', '.cnf', '.inf', '.reg', '.scr', '.sys', '.xml', '.prefs', '.opt', '.options', '.DS_Store', '.gitconfig',
            '.htaccess', '.htpasswd', '.manifest', '.pro', '.props', '.sln', '.user', '.vcxproj', '.xcu', '.xmc'
        }
        TIPOS_FONTES = {
            '.fnt', '.fon', '.otf', '.ttf', '.dfont', '.eot', '.pfb', '.pfm', '.woff', '.woff2', '.afm', '.bdf', '.pcf', '.snf'
        }
        TIPOS_SISTEMA = {
            '.acm', '.ax', '.bpl', '.com', '.cpl', '.cur', '.ani', '.drv', '.ds', '.efi', '.grd', '.icl', '.ime', '.job',
            '.kbd', '.mui', '.nls', '.rom', '.rsrc', '.sdi', '.sfc', '.spl', '.sve', '.theme', '.vxd', '.win'
        }
        TIPOS_GIS = {
            '.shp', '.shx', '.dbf', '.prj', '.sbn', '.sbx', '.gpx', '.kml', '.kmz', '.geojson', '.topojson', '.gdb',
            '.mxd', '.aprx', '.lyr', '.lyrx', '.qgs', '.qgz', '.mbtiles', '.geotiff', '.las', '.laz'
        }
        TIPOS_DISCO_VIRTUAL = {
            '.vdi', '.vhd', '.vhdx', '.vmdk', '.hdd', '.hds', '.pvm', '.qcow', '.qcow2', '.qed', '.vbox', '.vbox-prev'
        }

        if ext in TIPOS_IMAGEM:
            return loc.get_text("file_image")

        elif ext in TIPOS_AUDIO:
            return loc.get_text("file_audio")

        elif ext in TIPOS_VIDEO:
            return loc.get_text("file_video")

        elif ext in TIPOS_CODIGO_FONTE:
            return loc.get_text("file_source_code")

        elif ext in TIPOS_DOCUMENTO:
            return loc.get_text("file_document")

        elif ext in TIPOS_PLANILHA:
            return loc.get_text("file_spreadsheet")

        elif ext in TIPOS_APRESENTACAO:
            return loc.get_text("file_presentation")

        elif ext in TIPOS_BANCO_DADOS:
            return loc.get_text("file_database")

        elif ext in TIPOS_EXECUTAVEIS:
            return loc.get_text("file_executable")

        elif ext in TIPOS_COMPACTADOS:
            return loc.get_text("file_compressed")

        elif ext in TIPOS_BACKUP:
            return loc.get_text("file_backup")

        elif ext in TIPOS_LOG:
            return loc.get_text("file_log")

        elif ext in TIPOS_CONFIGURACAO:
            return loc.get_text("file_config")

        elif ext in TIPOS_FONTES:
            return loc.get_text("file_font")

        elif ext in TIPOS_SISTEMA:
            return loc.get_text("file_system")

        elif ext in TIPOS_GIS:
            return loc.get_text("file_gis")

        elif ext in TIPOS_DISCO_VIRTUAL:
            return loc.get_text("file_virtual_disk")

        elif ext:
            return f"{ext[1:].lower()}"

        return ""

    except Exception as e:
        logger.error(f"Erro ao identificar tipo de arquivo: {e}", exc_info=True)

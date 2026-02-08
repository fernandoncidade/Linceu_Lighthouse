import os
import rawpy
import imageio
from PIL import Image
from psd_tools import PSDImage
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_imagem(caminho, loc=None):
    ext = os.path.splitext(caminho)[1].lower()
    metadados = {}

    try:
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']:
            with Image.open(caminho) as img:
                metadados['dimensoes'] = f"{img.width}x{img.height}"
                if 'dpi' in img.info:
                    metadados['resolucao'] = f"{img.info['dpi'][0]}x{img.info['dpi'][1]} DPI"

        elif ext in ['.raw', '.cr2', '.nef', '.arw']:
            with rawpy.imread(caminho) as raw:
                metadados['dimensoes'] = f"{raw.sizes.width}x{raw.sizes.height}"

        elif ext in ['.psd']:
            psd = PSDImage.open(caminho)
            metadados['dimensoes'] = f"{psd.width}x{psd.height}"

        elif ext in ['.heic', '.heif']:
            try:
                img = imageio.imread(caminho)
                metadados['dimensoes'] = f"{img.shape[1]}x{img.shape[0]}"

            except Exception as e1:
                logger.error(f"Erro com imageio: {e1}", exc_info=True)
                try:
                    import subprocess
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
                        temp_filename = temp.name

                    subprocess.run(['ffmpeg', '-i', caminho, '-y', temp_filename], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    with Image.open(temp_filename) as img:
                        metadados['dimensoes'] = f"{img.width}x{img.height}"

                    os.unlink(temp_filename)

                except Exception as e2:
                    logger.error(f"Erro com método alternativo: {e2}", exc_info=True)
                    metadados['dimensoes'] = "Não disponível"

    except Exception as e:
        logger.error(f"Erro ao extrair metadados da imagem {caminho}: {e}", exc_info=True)

    return metadados

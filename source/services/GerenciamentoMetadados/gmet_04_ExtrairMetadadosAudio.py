from tinytag import TinyTag
from pymediainfo import MediaInfo
from decimal import Decimal, ROUND_HALF_UP
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_audio(caminho, loc=None):
    metadados = {}

    def _round_to_int(value):
        try:
            return int(Decimal(str(value)).quantize(0, rounding=ROUND_HALF_UP))

        except Exception:
            return int(float(value) + 0.5) if float(value) >= 0 else int(float(value) - 0.5)

    try:
        tag = TinyTag.get(caminho)

        if tag.duration:
            duracao = int(tag.duration)
            metadados['duracao'] = f"{duracao//3600:02d}:{(duracao%3600)//60:02d}:{duracao%60:02d}"

        if tag.bitrate:
            try:
                kbps = _round_to_int(tag.bitrate)
                metadados['taxa_bits'] = f"{kbps} kbps"

            except Exception:
                pass

        if tag.artist:
            metadados['artist'] = tag.artist

        if tag.album:
            metadados['album'] = tag.album

        if tag.title:
            metadados['title'] = tag.title

    except Exception as e:
        logger.error(f"Erro ao extrair metadados do áudio {caminho}: {e}", exc_info=True)

        try:
            media_info = MediaInfo.parse(caminho)
            for track in media_info.tracks:
                if track.track_type == "Audio":
                    if hasattr(track, 'duration'):
                        duracao_ms = float(track.duration)
                        duracao_s = duracao_ms / 1000.0
                        horas = int(duracao_s // 3600)
                        minutos = int((duracao_s % 3600) // 60)
                        segundos = int(duracao_s % 60)
                        metadados['duracao'] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

                    if hasattr(track, 'bit_rate') and track.bit_rate:
                        try:
                            bit_rate_bps = float(track.bit_rate)
                            kbps = _round_to_int(bit_rate_bps / 1000.0)
                            metadados['taxa_bits'] = f"{kbps} kbps"

                        except Exception:
                            pass

                    break

        except Exception as me:
            logger.error(f"Fallback para MediaInfo também falhou: {me}", exc_info=True)

    return metadados

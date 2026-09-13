import os
from pathlib import Path

import ffmpeg
import logging
from typing import Optional

logger = logging.getLogger(__name__)

ffmpeg._run.DEFAULT_CMD = r"C:\ffmpeg-N-126475-g35b7df64a0-win64-gpl-shared\bin\ffmpeg.exe"


def extract_audio(video_path: str, out_dir: str) -> Optional[str]:
    try:
        # Создаём папку для выходного файла
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        base = Path(video_path).stem  # "demo"
        wav_path = str(Path(out_dir) / f"{base}_full_audio.wav")  # data/processed/demo_full_audio.wav

        stream = ffmpeg.input(video_path)
        output = ffmpeg.output(
            stream.audio,
            wav_path,
            format="wav",
            acodec="pcm_s16le",
        )
        ffmpeg.run(output, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        logger.info("extract audio... to %s", wav_path)
        return wav_path

    except ffmpeg.Error as e:
        stderr = e.stderr.decode("utf8", errors="replace") if e.stderr else "(no stderr)"
        logger.error("FFmpeg stderr:\n%s", stderr)
        return None
    except Exception as e:
        logger.exception("Ошибка при извлечении: %s", e)
        return None
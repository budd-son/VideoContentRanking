import os
from pathlib import Path

import ffmpeg
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def extract_audio(video_path: str, out_dir: str) -> Optional[str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    base = Path(video_path).stem
    wav_path = str(Path(video_path)/f"{base}_full_audio.wav")

    try:
        stream = ffmpeg.input(video_path)
        output = ffmpeg.output(stream.audio, wav_path, format="wav", acodec="pcm_s16le")
        ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
        logger.info("extract audio... to %s", wav_path)
        return wav_path
    except Exception as e:
        logger.exception(f"Ошбика при извлечении: {e}")
        return None

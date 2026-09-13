
from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)

from faster_whisper import WhisperModel

def transcribe_audio(wav_path, model_size):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, _ = model.transcribe(
        wav_path,
        language="ru",
        vad_filter=True,
        beam_size=5
    )

    result = []
    for seg in segments:
        result.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })
    logger.info("Audio transcription complete")
    return result


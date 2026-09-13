
from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)

def transcribe_audio(wav_path):
    model = WhisperModel("small", device="cpu", compute_type="int8")

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

    return result

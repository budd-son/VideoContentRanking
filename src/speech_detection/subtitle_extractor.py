import logging
from typing import List

from faster_whisper import WhisperModel
from src.models import SpeechSegment

logger = logging.getLogger(__name__)


def transcribe_audio(
    wav_path: str,
    model_size: str = "small",
    language: str = "ru",
) -> List[SpeechSegment]:
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, _ = model.transcribe(
        wav_path,
        language=language,
        vad_filter=True,
        beam_size=5,
    )

    result: List[SpeechSegment] = []
    for seg in segments:
        result.append(
            SpeechSegment(
                start=seg.start,
                end=seg.end,
                text=seg.text.strip(),
            )
        )

    logger.info("Transcribed %d speech segments", len(result))
    return result
import logging
from faster_whisper import WhisperModel
from typing import List, Dict

logger = logging.getLogger(__name__)

class ASRWrapper:
    def __init__(self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8"):
        logger.info("Loading ASR model %s on %s", model_size, device)
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str, language: str = "ru", vad_filter: bool = True) -> List[Dict]:
        logger.info("Transcribing %s", audio_path)
        segments, info = self.model.transcribe(audio_path, language=language, vad_filter=vad_filter, word_timestamps=False)
        segs = [{"start": float(s.start), "end": float(s.end), "text": s.text.strip()} for s in segments]
        logger.info("Transcription produced %d segments", len(segs))
        return segs

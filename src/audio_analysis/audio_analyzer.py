import logging
from typing import List, Dict, Tuple

import librosa
import numpy as np
import soundfile as sf
import pyloudnorm as pyln

"""
soundfile + ручной RMS (np.sqrt(mean(x**2)) 
по окнам) eСЛИ OOM
"""

logger = logging.getLogger(__name__)

def audio_features(wav_path, scenes):
    audio, sr = sf.read(wav_path)
    meter = pyln.Meter(sr)
    enriched = []
    for row in scenes:
        start = row["start"]
        end = row["end"]
        start_sample = int(start * sr)
        end_sample = int(end * sr)
        if start_sample >= end_sample or end_sample>len(audio):
            row["avg_rms"] = np.nan
            row["max_rms"] = np.nan
            row["lufs"] = np.nan
            enriched.append(row)
            logger.error("Something wrong with timecodes")
            continue
        segment = audio[start_sample:end_sample]

        rms = np.sqrt(np.mean(segment**2))
        max_rms = np.sqrt(np.max(segment**2))
        lufs = meter.integrated_loudness(segment)

        row["avg_rms"] = float(rms)
        row["max_rms"] = float(max_rms)
        row["lufs"] = float(lufs)

        enriched.append(row)
    logger.info("Audio processing %s complete", wav_path)
    return enriched

import logging
import numpy as np
import soundfile as sf
import pyloudnorm as pyln

logger = logging.getLogger(__name__)
"""
soundfile + ручной RMS (np.sqrt(mean(x**2)) 
по окнам) eСЛИ OOM
"""

def audio_features(wav_path, scenes):
    audio, sr = sf.read(wav_path)
    meter = pyln.Meter(sr)
    enriched = []

    for row in scenes:
        start = row["start_time"]
        end = row["end_time"]
        start_sample = int(start * sr)
        end_sample = int(end * sr)

        if start_sample >= end_sample or end_sample > len(audio):
            row["avg_rms"] = np.nan
            row["max_rms"] = np.nan
            row["lufs"] = np.nan
            row["is_silent"] = True
            enriched.append(row)
            logger.error("Something wrong with timecodes")
            continue

        segment = audio[start_sample:end_sample]

        rms = np.sqrt(np.mean(segment**2))
        max_rms = np.sqrt(np.max(segment**2))

        try:
            lufs = meter.integrated_loudness(segment)
            if not np.isfinite(lufs):
                row["lufs"] = np.nan
                row["is_silent"] = True
            else:
                row["lufs"] = float(lufs)
                row["is_silent"] = False
        except Exception:
            row["lufs"] = np.nan
            row["is_silent"] = True

        row["avg_rms"] = float(rms)
        row["max_rms"] = float(max_rms)

        enriched.append(row)

    logger.info("Audio processing %s complete", wav_path)
    return enriched


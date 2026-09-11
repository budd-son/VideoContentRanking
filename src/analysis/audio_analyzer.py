import logging
from typing import List, Dict, Tuple
import numpy as np
import soundfile as sf
import pyloudnorm as pyln

"""
soundfile + ручной RMS (np.sqrt(mean(x**2)) 
по окнам) eСЛИ OOM
"""

logger = logging.getLogger(__name__)

def compute_lufs(wav_path:str)->float:
    data, rate = sf.read(wav_path)
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)
    logger.debug("Computed lufs %s for %s", loudness, wav_path)
    return float(loudness)

def analyze_loudness_by_scenes(wav_path: str, scenes: List[Tuple[float, float]], hop_length: int = 512) -> List[Dict]:
    import librosa
    y, sr = librosa.load(wav_path, sr=None, mono=True)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    frames = np.arange(len(rms))
    times = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
    results = []
    for idx, (start, end) in enumerate(scenes, start=1):
        mask = (times >= start) & (times <= end)
        if mask.any():
            scene_rms = rms[mask]
            avg_r = float(scene_rms.mean())
            max_r = float(scene_rms.max())
        else:
            avg_r = 0.0
            max_r = 0.0
        start_sample = int(start*sr)
        end_sample = int(end*sr)
        scene_data = y[start_sample:end_sample] if end_sample > start_sample else np.array([])
        lufs = None
        lufs = None
        if scene_data.size > 0:
            meter = pyln.Meter(sr)
            try:
                lufs = float(meter.integrated_loudness(scene_data))
            except Exception:
                lufs = None

        results.append({
            "scene_id": idx,
            "start_time": float(start),
            "end_time": float(end),
            "avg_rms": avg_r,
            "max_rms": max_r,
            "lufs": lufs,
            "duration": float(end - start),
            "is_silent": (max_r < 1e-5)
        })
    logger.info("Analyzed loudness for %d scenes", len(results))
    return results
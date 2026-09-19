import numpy as np
import logging

logger = logging.getLogger(__name__)

def normalize_audio_features(scenes):
    rms_values = [s["avg_rms"] for s in scenes if np.isfinite(s["avg_rms"])]
    max_values = [s["max_rms"] for s in scenes if np.isfinite(s["max_rms"])]
    lufs_values = [s["lufs"] for s in scenes if np.isfinite(s["lufs"])]

    max_mean, rms_max_std = np.mean(max_values), np.std(max_values)
    rms_mean, rms_std = np.mean(rms_values), np.std(rms_values)
    lufs_mean, lufs_std = np.mean(lufs_values), np.std(lufs_values)

    for s in scenes:
        if not np.isnan(s["avg_rms"]):
            s["rms_z"] = (s["avg_rms"] - rms_mean) / rms_std
        else:
            s["rms_z"] = np.nan
        if not np.isnan(s["max_rms"]):
            s["rms_max_z"] = (s["max_rms"] - max_mean) / rms_max_std
        else:
            s["rms_z"] = np.nan

        if not np.isnan(s["lufs"]):
            s["lufs_z"] = (s["lufs"] - lufs_mean) / lufs_std
        else:
            s["lufs_z"] = np.nan

    logger.info("Audio features normalized")
    return scenes

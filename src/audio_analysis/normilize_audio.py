import numpy as np
import logging

logger = logging.getLogger(__name__)

def normalize_audio_features(scenes):
    rms_values = [s["avg_rms"] for s in scenes if np.isfinite(s.get("avg_rms", np.nan))]
    max_values = [s["max_rms"] for s in scenes if np.isfinite(s.get("max_rms", np.nan))]
    lufs_values = [s["lufs"] for s in scenes if np.isfinite(s.get("lufs", np.nan))]
    var_values = [s["rms_var"] for s in scenes if np.isfinite(s.get("rms_var", np.nan))]

    rms_mean, rms_std = np.mean(rms_values), np.std(rms_values)
    max_mean, max_std = np.mean(max_values), np.std(max_values)
    lufs_mean, lufs_std = np.mean(lufs_values), np.std(lufs_values)
    var_mean, var_std = np.mean(var_values), np.std(var_values)
    rms_std = rms_std if rms_std > 0 else 1.0
    max_std = max_std if max_std > 0 else 1.0
    lufs_std = lufs_std if lufs_std > 0 else 1.0
    var_std = var_std if var_std > 0 else 1.0

    for s in scenes:
        if np.isfinite(s.get("avg_rms", np.nan)):
            s["rms_z"] = (s["avg_rms"] - rms_mean) / rms_std
        else:
            s["rms_z"] = np.nan

        if np.isfinite(s.get("max_rms", np.nan)):
            s["rms_max_z"] = (s["max_rms"] - max_mean) / max_std
        else:
            s["rms_max_z"] = np.nan   # CHANGED

        if np.isfinite(s.get("lufs", np.nan)):
            s["lufs_z"] = (s["lufs"] - lufs_mean) / lufs_std
        else:
            s["lufs_z"] = np.nan

        if np.isfinite(s.get("rms_var", np.nan)):
            s["rms_var_z"] = (s["rms_var"] - var_mean) / var_std
        else:
            s["rms_var_z"] = np.nan   # CHANGED

    logger.info("Audio features normalized")
    return scenes

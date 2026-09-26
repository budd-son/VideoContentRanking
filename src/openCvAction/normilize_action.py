import numpy as np

def normalize_motion_features(scenes):
    features = {
        "motion":  [s.get("motion", np.nan)  for s in scenes],
        "camera":  [s.get("camera", np.nan)  for s in scenes],
        "object":  [s.get("object", np.nan)  for s in scenes],
        "entropy": [s.get("entropy", np.nan) for s in scenes],
    }

    stats = {}
    for key, vals in features.items():
        arr = np.array([v for v in vals if np.isfinite(v)], dtype=float)
        mean = arr.mean() if arr.size > 0 else 0.0
        std  = arr.std(ddof=0) if arr.size > 0 else 1.0
        if std <= 0 or not np.isfinite(std):
            std = 1.0
        stats[key] = (mean, std)

    for s in scenes:
        for key, (mean, std) in stats.items():
            val = s.get(key, np.nan)
            if np.isfinite(val):
                s[f"{key}_z"] = (val - mean) / std
            else:
                s[f"{key}_z"] = 0.0

    return scenes


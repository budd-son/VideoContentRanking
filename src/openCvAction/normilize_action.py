import numpy as np

def normalize_motion_features(scenes):
    keys = ["motion", "largest", "speed", "entropy"]
    for key in keys:
        vals = [s.get(key, 0.0) for s in scenes]
        arr = np.asarray(vals, dtype=float)
        mean = float(arr.mean())
        std = float(arr.std(ddof=0))
        std = std if std > 0 else 1.0
        zvals = ((arr - mean) / std).tolist()
        for s, z in zip(scenes, zvals):
            s[f"{key}_z"] = z
    return scenes

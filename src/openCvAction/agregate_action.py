import numpy as np

def aggregate_motion_features(scene, frame_rows, fps_src, frame_step):

    start_frame = int(scene["start_time"] * fps_src)
    end_frame   = int(scene["end_time"] * fps_src)

    vals = [r[1:] for r in frame_rows if start_frame <= r[0] <= end_frame]
    if not vals:
        return {"motion": 0.0, "largest": 0.0, "speed": 0.0, "entropy": 0.0}

    arr = np.array(vals)
    return {
        "motion": float(arr[:,0].mean()),
        "largest": float(arr[:,1].mean()),
        "speed": float(arr[:,2].mean()),
        "entropy": float(arr[:,3].mean())
    }

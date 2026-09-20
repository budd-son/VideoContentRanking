import numpy as np

def aggregate_motion_features(scene_rows, motion_rows, fps_src, frame_step):
    """
    scene_rows: список dict со start_time, end_time
    motion_rows: список (frame_idx, motion_ratio, largest_ratio, mean_speed, dir_entropy)
    fps_src: исходный fps видео
    frame_step: шаг кадров
    """
    for scene in scene_rows:
        start_frame = int(scene["start_time"] * fps_src)
        end_frame   = int(scene["end_time"] * fps_src)

        vals = [r[1:] for r in motion_rows if start_frame <= r[0] <= end_frame]
        if not vals:
            scene["motion"]  = np.nan
            scene["largest"] = np.nan
            scene["speed"]   = np.nan
            scene["entropy"] = np.nan
            continue

        arr = np.array(vals)
        scene["motion"]  = float(arr[:,0].mean())
        scene["largest"] = float(arr[:,1].mean())
        scene["speed"]   = float(arr[:,2].mean())
        scene["entropy"] = float(arr[:,3].mean())

    return scene_rows



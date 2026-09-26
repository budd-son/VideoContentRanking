import numpy as np

def aggregate_motion_features(scene_rows, motion_rows, fps_src, frame_step=None):
    """
    scene_rows: список dict со start_time, end_time
    motion_rows: список (frame_idx, motion_mean, camera_motion, object_motion, dir_entropy)
    fps_src: исходный fps видео
    frame_step: не используется, оставлен для совместимости
    """
    for scene in scene_rows:
        start_frame = int(scene["start_time"] * fps_src)
        end_frame   = int(scene["end_time"] * fps_src)

        vals = [r[1:] for r in motion_rows if start_frame <= r[0] <= end_frame]
        if not vals:
            scene["motion"]  = np.nan
            scene["camera"]  = np.nan
            scene["object"]  = np.nan
            scene["entropy"] = np.nan
            continue

        arr = np.array(vals)
        scene["motion"]  = float(np.median(arr[:, 0]))
        scene["camera"]  = float(np.median(arr[:, 1]))
        scene["object"]  = float(np.median(arr[:, 2]))
        scene["entropy"] = float(np.median(arr[:, 3]))

    return scene_rows



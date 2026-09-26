import csv
import os
import cv2
import numpy as np


def analise_action(video_path):
    VIDEO_PATH = video_path
    OUT_DIR    = "./data/interim"

    SCALE       = 0.5
    FRAME_STEP  = 5

    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_FAST)
    os.makedirs(OUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(VIDEO_PATH)
    video_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]
    if not cap.isOpened():
        raise SystemExit("Cannot open video")

    fps_src = cap.get(cv2.CAP_PROP_FPS) or 30

    prev_gray = None
    rows = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % FRAME_STEP != 0:
            continue

        small = cv2.resize(frame, None, fx=SCALE, fy=SCALE,
                           interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            prev_gray = gray
            continue

        flow = dis.calc(prev_gray, gray, None)
        mag = np.linalg.norm(flow, axis=2)
        motion_mean = float(mag.mean()) / SCALE

        median_flow = np.median(flow.reshape(-1, 2), axis=0)
        camera_motion = float(np.linalg.norm(median_flow)) / SCALE

        residual = flow - median_flow
        object_motion = float(np.linalg.norm(residual, axis=2).mean()) / SCALE

        ang = np.arctan2(flow[..., 1], flow[..., 0])
        hist, _ = np.histogram(ang, bins=8, range=(-np.pi, np.pi))
        p = hist / (hist.sum() + 1e-9)
        dir_entropy = float(-np.sum(p * np.log2(p + 1e-9)))

        prev_gray = gray
        rows.append((frame_idx, motion_mean, camera_motion,
                     object_motion, dir_entropy))

    cap.release()

    csv_path = os.path.join(OUT_DIR, f"{video_name}.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame", "motion_mean", "camera_motion",
                    "object_motion", "dir_entropy"])
        w.writerows(rows)
    return rows, fps_src
import cv2
import numpy as np
import os
import csv
import time

def analise_action(video_path):

    VIDEO_PATH = video_path
    OUT_DIR    = "./data/interim"

    SCALE       = 0.5     # кадр в 2 раза меньше → поток в 4 раза быстрее
    FRAME_STEP  = 5       # считать каждый 5-й кадр (6 fps из 30)
    BUF_SIZE    = 15      # окно сглаживания (15 × 5 = 75 реальных кадров ≈ 2.5 сек)

    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_FAST)

    os.makedirs(OUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(VIDEO_PATH)
    video_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]

    if not cap.isOpened():
        raise SystemExit("Cannot open video")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_src      = cap.get(cv2.CAP_PROP_FPS) or 30
    print(f"Video: {video_name}, frames: {total_frames}, fps: {fps_src:.1f}")
    print(f"Scale: {SCALE}, step: {FRAME_STEP} → ~{fps_src/FRAME_STEP:.1f} обрабатываемых fps")

    backSub = cv2.createBackgroundSubtractorMOG2(
        history=1000, varThreshold=60, detectShadows=True
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    prev_gray = None
    buf = []
    rows = []
    frame_idx = 0
    processed = 0

    t_start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1


        if frame_idx % FRAME_STEP != 0:
            continue
        processed += 1

        small = cv2.resize(frame, None, fx=SCALE, fy=SCALE,
                           interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        fg_mask = backSub.apply(gray)
        fg_mask[fg_mask == 127] = 0
        _, mask_thresh = cv2.threshold(fg_mask, 220, 255, cv2.THRESH_BINARY)
        mask_clean = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN,  kernel, iterations=2)
        mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel, iterations=2)

        motion_pixels = cv2.countNonZero(mask_clean)
        motion_ratio = motion_pixels / (gray.shape[0] * gray.shape[1])

        n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_clean, connectivity=8)
        if n_labels > 1:
            largest_area = int(stats[1:, cv2.CC_STAT_AREA].max())
        else:
            largest_area = 0
        largest_ratio = largest_area / (gray.shape[0] * gray.shape[1])

        mean_speed, dir_entropy = 0.0, 0.0
        if prev_gray is not None:
            flow = dis.calc(prev_gray, gray, None)
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            m = mask_clean > 0
            if m.any():
                mean_speed = float(mag[m].mean()) / SCALE
                hist, _ = np.histogram(ang[m], bins=8, range=(0, 2 * np.pi))
                p = hist / (hist.sum() + 1e-9)
                dir_entropy = float(-np.sum(p * np.log2(p + 1e-9)))
        prev_gray = gray

        buf.append((motion_ratio, largest_ratio, mean_speed, dir_entropy))
        if len(buf) > BUF_SIZE:
            buf.pop(0)

        mr, lr, sp, de = np.mean(buf, axis=0)
        rows.append((frame_idx, mr, lr, sp, de))


    cap.release()


    csv_path = os.path.join(OUT_DIR, f"{video_name}.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame", "motion_ratio", "largest_ratio", "mean_speed", "dir_entropy"])
        w.writerows(rows)
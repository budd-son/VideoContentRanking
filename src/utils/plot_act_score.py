import matplotlib
import matplotlib.pyplot as plt
import csv as _csv
import os

def plot_motion_debug(motion_csv, scenes, fps_src,
                      out_path=None, show=True):


    if not show:
        matplotlib.use("Agg")

    frames, motion, camera, obj, entropy = [], [], [], [], []
    with open(motion_csv, "r", newline="") as f:
        r = _csv.DictReader(f)
        for row in r:
            frames.append(int(row["frame"]))
            motion.append(float(row["motion_mean"]))
            camera.append(float(row["camera_motion"]))
            obj.append(float(row["object_motion"]))
            entropy.append(float(row["dir_entropy"]))

    if not frames:
        print("[plot_motion_debug] пустой CSV")
        return

    times = [f / fps_src for f in frames]

    all_cuts = set()
    for sc in scenes:
        ct = sc.get("cut_times")
        if isinstance(ct, list):
            for c in ct:
                all_cuts.add(round(float(c), 3))
        elif isinstance(ct, (int, float)):
            all_cuts.add(round(float(ct), 3))
    all_cuts = sorted(all_cuts)

    fig, axes = plt.subplots(4, 1, figsize=(16, 10), sharex=True)

    axes[0].plot(times, motion,  lw=0.9, color="tab:blue")
    axes[0].set_ylabel("motion")

    axes[1].plot(times, camera,  lw=0.9, color="tab:orange")
    axes[1].set_ylabel("camera")

    axes[2].plot(times, obj,     lw=0.9, color="tab:green")
    axes[2].set_ylabel("object")

    axes[3].plot(times, entropy, lw=0.9, color="tab:red")
    axes[3].set_ylabel("entropy")
    axes[3].set_xlabel("time, s")

    # --- вертикальные линии на склейках ---
    for ax in axes:
        for c in all_cuts:
            ax.axvline(c, color="red", alpha=0.35, lw=0.7)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    if out_path is None:
        out_path = os.path.splitext(motion_csv)[0] + "_debug.png"
    plt.savefig(out_path, dpi=120)
    if show:
        plt.show()
    plt.close(fig)
    print(f"[plot_motion_debug] сохранено: {out_path}")
    print(f"[plot_motion_debug] склеек: {len(all_cuts)}")
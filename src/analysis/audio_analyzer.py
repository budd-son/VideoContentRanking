import librosa
import numpy as np

from src.io.audio_extracter import extract_audio


def analyze_loudness(video_path, scenes):
    wav_path = extract_audio(video_path);
    if not wav_path:
        return []

    y, sr = librosa.load(wav_path, sr=None, mono=True)

    rms = librosa.feature.rms(y=y, hop_length=512)
    times = librosa.frames_to_time(np.arange(len(rms[0])), sr=sr, hop_length=512)


    loudness_data = []
    for i, (start_time, end_time) in enumerate(scenes):
        mask = (times >= start_time) & (times <= end_time)

        if np.any(mask):
            scene_rms = rms[0][mask]

            avg_rms = float(np.mean(scene_rms))
            max_rms = float(np.max(scene_rms))
        else:
            avg_rms = 0.0
            max_rms = 0.0

        loudness_data.append({
            'scene_id': i + 1,
            'start_time': start_time,
            'end_time': end_time,
            'avg_rms': avg_rms,
            'max_rms': max_rms,
            'is_silent': max_rms < 0.01
        })

    return loudness_data
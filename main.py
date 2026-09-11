# main.py
import os
import pandas as pd

from src.analysis.audio_analyzer import analyze_loudness
from src.analysis.scene_detector import detect_scenes
from src.subtitle_extractor import generate_subtitles


path = "data/raw/demo.mp4"


print("Этап 1: Детекция сцен...")
scenes = detect_scenes(path)
scenes_in_seconds = []
for start_frame, end_frame in scenes:
    start_sec = start_frame.seconds
    end_sec = end_frame.seconds
    scenes_in_seconds.append((start_sec, end_sec))

print("\nЭтап 2: Генерация субтитров...")
data_with_subtitles = generate_subtitles(path, scenes_in_seconds)

print("\nЭтап 3: Анализ аудио...")
loudness_data = analyze_loudness(path, scenes_in_seconds)

final_data = []
for sub in data_with_subtitles:
    matching_loudness = next((item for item in loudness_data if item['scene_id'] == sub['scene_id']), {})

    final_data.append({
        **sub,
        **matching_loudness
    })

print("\nЭтап 3: Сохранение в CSV...")
df = pd.DataFrame(final_data)
os.makedirs('data/annotations', exist_ok=True)
df.to_csv('data/annotations/scenes_with_subtitles.csv', index=False)

print(f"Готово! Сохранено строк в data/annotations/scenes_with_subtitles.csv")
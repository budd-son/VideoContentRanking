import os
from scenedetect import detect, ContentDetector
import pandas as pd
def detect_scenes(video_path):
    path = video_path
    scene_data = []
    scenes = detect(path, ContentDetector())
    for i, (scene_start, scene_end) in enumerate(scenes,1):
        scene_data.append({
            'path_name': os.path.basename(path),
            'scene_id': i,
            'start_time': scene_start,
            'end_time': scene_end

        })
    df = pd.DataFrame(scene_data)
    df.to_csv('C:/Users/Соня/PycharmProjects/PythonProject/VideoContentRanking/data/annotations/scenes_timestamp.csv', index=False)
    print(f"Saved {len(scenes)} scenes to scenes_timestamps.csv")
    return scenes

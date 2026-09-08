import os
from faster_whisper import WhisperModel


def generate_subtitles(audio_path, scenes):

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    all_segments_data = []

    print(f"Распознаю аудиодорожку: {audio_path}")

    segments, info = model.transcribe(audio_path,
                                      language="ru",
                                      vad_filter=True,
                                      word_timestamps=False)


    all_segments = list(segments)

    print(f"Распознавание завершено. Найдено {len(all_segments)} речевых сегментов.\n")

    for i, (start_time, end_time) in enumerate(scenes):
        scene_text = ""

        for segment in all_segments:

            if segment.start >= start_time and segment.end <= end_time:
                scene_text += segment.text + " "

            elif segment.start > end_time:
                break


        clean_text = scene_text.strip()
        if clean_text:
            print(f"Сцена {i + 1}: {clean_text[:70]}...")
        else:
            print(f"Сцена {i + 1}: [Тишина]")


        all_segments_data.append({
            'path_name': os.path.basename(audio_path),
            'scene_id': i,  # Нумерация с 0, если хотите с 1 - поставьте i+1
            'start_time': start_time,
            'end_time': end_time,
            'text': clean_text
        })

    return all_segments_data
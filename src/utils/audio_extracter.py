import os
import ffmpeg


def extract_audio(video_path):

    output_dir = "C:/Users/Соня/PycharmProjects/PythonProject/VideoContentRanking/data/audioVideoContent"
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(video_path).split('.')[0]
    wav_path = os.path.join(output_dir, f"{base_name}_full_audio.wav")
    try:
        stream = ffmpeg.input(video_path)
        output = ffmpeg.output(stream.audio, wav_path, format="wav", acodec="pcm_s16le")
        ffmpeg.run(output)
        return wav_path
    except Exception as e:
        print(f"Ошбика при извлечении: {e}")
        return None

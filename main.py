import argparse

from src.data_build.csv_saver import save_scene_table
from src.io.audio_extracter import extract_audio
from src.speech_detection.subtitle_extractor import *
from src.speech_detection.speech_merge import merge_speech_moments
from src.analysis.scene_detector import detect_scenes
from src.data_build.scene_builder import build_scene_data
from src.audio_analysis.audio_analyzer import audio_features



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--output", default="data/scenes/output.csv")
    return parser.parse_args()


def main():
    args = parse_args()

    wav = extract_audio(args.video, "data/audio")

    visual_scenes = detect_scenes(args.video)
    speech_raw = transcribe_audio(wav)
    speech_scenes = merge_speech_moments(speech_raw, max_gap=0.3)
    scene_rows = build_scene_data(speech_scenes, visual_scenes)
    print(scene_rows[0])
    scene_rows = audio_features(wav, scene_rows)

    save_scene_table(scene_rows, args.output)



if __name__ == "__main__":
    main()

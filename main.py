import argparse
import logging

from src.utils.config_loader import load_config
from src.analysis.scene_detector import detect_scenes
from src.io.audio_extracter import extract_audio
from src.speech_detection.subtitle_extractor import transcribe_audio
from src.speech_detection.speech_merge import merge_speech_moments
from src.data_build.scene_builder import build_scene_data
from src.audio_analysis.audio_analyzer import audio_features
from src.audio_analysis.normilize_audio import normalize_audio_features
from src.data_build.csv_saver import save_scene_table

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description="Video Content Ranking Pipeline")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    video_path = config["video"]["input_path"]
    output_csv = config["video"]["output_csv"]

    logging.info("Extracting audio...")
    wav = extract_audio(video_path, out_dir=config["paths"]["audio_out_dir"])


    logging.info("Detecting visual scenes...")
    visual_scenes = detect_scenes(video_path, threshold=config["scenes"]["threshold"])

    logging.info("Transcribing audio...")
    speech_raw = transcribe_audio(wav, model_size=config["speech"]["model_size"])

    logging.info("Merging speech segments...")
    speech_scenes = merge_speech_moments(speech_raw, max_gap=config["speech"]["max_gap"])

    logging.info("Building scene table...")
    scene_rows = build_scene_data(visual_scenes, speech_scenes, min_duration=config["scenes"]["min_duration"])

    logging.info("Extracting audio features...")
    scene_rows = audio_features(wav, scene_rows)

    if config["audio"]["normalize"]:
        logging.info("Normalizing audio features...")
        scene_rows = normalize_audio_features(scene_rows)

    logging.info("Saving CSV...")
    save_scene_table(scene_rows, output_csv)

    logging.info("Pipeline complete. Output saved to %s", output_csv)

if __name__ == "__main__":
    main()

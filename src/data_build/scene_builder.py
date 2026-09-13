import logging

logger = logging.getLogger(__name__)

def build_scene_data(visual_scenes, speech_scenes, min_duration):
    table = []
    seen = set()

    for speech in speech_scenes:
        duration = speech["end"] - speech["start"]
        if duration < min_duration:
            continue

        key = (speech["start"], speech["end"])
        if key in seen:
            continue
        seen.add(key)

        cuts = sum(
            1 for vs in visual_scenes
            if not (vs["end"] < speech["start"] or vs["start"] > speech["end"])
        )

        table.append({
            "start_time": speech["start"],
            "end_time": speech["end"],
            "duration": duration,
            "scene_source": "speech",
            "text": speech.get("text", ""),
            "cuts_inside": cuts
        })

    for vs in visual_scenes:
        duration = vs["end"] - vs["start"]
        if duration < min_duration:
            continue

        key = (vs["start"], vs["end"])
        if key in seen:
            continue


        intersect = any(
            not (row["end_time"] <= vs["start"] or row["start_time"] >= vs["end"])
            for row in table
        )
        if intersect:
            continue

        seen.add(key)
        table.append({
            "start_time": vs["start"],
            "end_time": vs["end"],
            "duration": duration,
            "scene_source": "visual",
            "text": "",
            "cuts_inside": 1
        })

    table = sorted(table, key=lambda x: x["start_time"])
    for i, row in enumerate(table, start=1):
        row["scene_id"] = f"scene_{i}"
    logger.info("Completed building scene data.")
    return table


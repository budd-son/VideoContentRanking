def merge_visual_scenes(scenes, max_duration=1.5):
    scenes = sorted(scenes, key=lambda s: s["start_time"])
    merged = []
    group = []

    def flush():
        nonlocal group
        if group:
            merged.append(_merge_group(group))
            group = []

    for scene in scenes:
        if scene["scene_source"] == "speech":
            flush()
            merged.append(scene)          # сохраняем сцену речи
            continue

        duration = scene["end_time"] - scene["start_time"]
        if duration <= max_duration:
            group.append(scene)
        else:
            flush()
            merged.append(scene)          # сохраняем длинную сцену

    flush()
    return merged


def _merge_group(group):
    start = group[0]["start_time"]
    end = group[-1]["end_time"]
    return {
        "start_time": start,
        "end_time": end,
        "duration": end - start,
        "scene_source": "visual_merged",
        "cuts_inside": len(group),
        "text": ""
    }

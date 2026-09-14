def merge_visual_scenes(scenes, max_duration=1.5):
    scenes = sorted(scenes, key=lambda scene: scene["start_time"])

    merged = []
    group = []

    for scene in scenes:
        if scene["scene_source"] == "speech":
            if len(group) > 0:
                merged.append(_merge_group(group))
                group = []
        else:
            duration = scene["end_time"] - scene["start_time"]
            if duration <= max_duration:
                group.append(scene)
            else:
                if len(group) > 0:
                    merged.append(_merge_group(group))
                    group = []

    if len(group) > 0:
        merged.append(_merge_group(group))
    else:
        merged.extend(group)

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

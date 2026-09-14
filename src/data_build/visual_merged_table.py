def rebuild_scene_table(old_table, new_visual_scenes):

    base = [
        row for row in old_table
        if row["scene_source"] == "speech"
    ]

    for vs in new_visual_scenes:
        base.append({
            "start_time": vs["start_time"],
            "end_time": vs["end_time"],
            "duration": vs["end_time"] - vs["start_time"],
            "scene_source": vs.get("scene_source", "visual"),
            "text": vs.get("text", ""),
            "cuts_inside": vs.get("cuts_inside", 1)
        })

    base = sorted(base, key=lambda x: x["start_time"])

    cleaned = []
    last_end = 0

    for row in base:
        start = row["start_time"]
        end = row["end_time"]

        if start < last_end:
            start = last_end
            if end <= start:
                continue

        row["start_time"] = start
        row["end_time"] = end
        row["duration"] = end - start

        cleaned.append(row)
        last_end = end

    return cleaned

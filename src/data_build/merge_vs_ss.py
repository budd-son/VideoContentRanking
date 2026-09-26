def build_scene_data(visual_scenes, speech_scenes):
    result = []
    ind_vs = 0
    visual_scenes.sort(key=lambda x: x["start_time"])
    speech_scenes.sort(key=lambda x: x["start_time"])
    speech_bounds = {(s["start_time"], s["end_time"]) for s in speech_scenes}
    visual_scenes = [v for v in visual_scenes
                     if (v["start_time"], v["end_time"]) not in speech_bounds]

    for s_scene in speech_scenes:
        s_start = s_scene["start_time"]
        s_end = s_scene["end_time"]
        vs_count = 0
        cut_times = []
        while ind_vs < len(visual_scenes):
            v = visual_scenes[ind_vs]
            v_start = v["start_time"]
            v_end = v["end_time"]

            if v_start >= s_end:
                break

            if v_end <= s_start:
                result.append({**v,
                               "duration": v_end - v_start,
                               "type": "visual", "cuts": 1.0, "cut_times": v_start,
                               "cut_per_sec": vs_count/(s_end - s_start)})

                ind_vs += 1
                continue

            vs_count += 1
            cut_times.append(v["start_time"])
            if v_start < s_start:
                if v_end > s_start:
                    vs_count += 1
                v_end = min(v_end, s_start)
                result.append({**v,
                               "start_time": v_start,
                               "end_time":   v_end,
                               "duration":   v_end - v_start,
                               "cuts": vs_count,
                               "type": "visual",
                               "cut_times": cut_times,
                               "cut_per_sec": vs_count/(s_end - s_start)})

            if v_end > s_end:
                visual_scenes[ind_vs] = {**v, "start_time": s_end}
                break
            else:
                ind_vs += 1

        result.append({**s_scene,
                       "duration": s_end - s_start,
                       "type": "speech", "cuts": vs_count, "cut_per_sec": vs_count/(s_end - s_start), "cut_times": cut_times})


    while ind_vs < len(visual_scenes):
        v = visual_scenes[ind_vs]
        cut_times = []
        cut_times.append(v["start_time"])
        result.append({**v,
                       "duration": v["end_time"] - v["start_time"],
                       "type": "visual", "cuts": 1.0, "cut_times": cut_times, "cut_per_sec": 1.0/(v["end_time"] - v["start_time"])})
        ind_vs += 1

    result.sort(key=lambda x: x["start_time"])
    return merge_vs(result)


def merge_vs(scenes):
    result = []
    buf = []
    maxDuration = 5.0

    for scene in scenes:
        if scene["type"] == "visual" and scene["duration"] < maxDuration:
            buf.append(scene)
            total = sum(x["duration"] for x in buf)
            if total > maxDuration:
                result.append(merge(buf))
                buf = []
        else:
            if buf:
                result.append(merge(buf))
                buf = []
            result.append(scene)

    if buf:
        result.append(merge(buf))

    return add_scene_id(result)


def merge(scenes):
    start = scenes[0]["start_time"]
    end = scenes[-1]["end_time"]
    cut_times = [x["start_time"] for x in scenes]
    duration = end - start
    cuts = len(scenes)
    return {"start_time": start, "end_time": end, "duration": duration,
            "cuts": cuts, "type": "visual", "cut_per_sec": cuts / duration, "cut_times": cut_times}
def add_scene_id(scenes):

    return [
        {"scene_id": i, **sc}
        for i, sc in enumerate(scenes)
    ]
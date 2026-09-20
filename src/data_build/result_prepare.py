def result(scenes):
    table = []
    for scene in scenes:
        table.append({
            "start_time": scene["start_time"],
            "end_time": scene["end_time"],
            "duration": scene["duration"],
            "scene_source": scene["scene_source"],
            "text":scene["text"],
            "cuts_z": scene["cuts_inside"] / scene["duration"],
            "rms_z": scene["rms_z"],
            "rms_max_z": scene["rms_max_z"],
            "lufs_z": scene["lufs_z"],
            "rms_var_z": scene["rms_var_z"],
            "motion_z": scene["motion_z"],
            "largest_z": scene["largest_z"],
            "speed_z": scene["speed_z"],
            "entropy_z": scene["entropy_z"]
        })
    return table

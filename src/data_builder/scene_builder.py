import logging

logger = logging.getLogger(__name__)

def count_cuts_inside_speech(speech, visual_scenes):
    fw_start = speech['start']
    fw_end = speech['end']
    count = 0

    for vs in visual_scenes:
        if(fw_start <= vs['start'] <= fw_end):
            count += 1
    return count

def build_scene_data(speech_scenes, visual_scenes):
    table = []
    table = sorted(table, key=lambda row: row["start_time"])
    scene_counter = 1
    for speech in speech_scenes:
        cuts = count_cuts_inside_speech(speech, visual_scenes)
        table.append({
            "start_time": speech["start"],
            "end_time": speech["end"],
            "duration": speech["end"] - speech["start"],
            "scene_source": "speech",
            "text": speech["text"],
            "cuts_inside": cuts
        })


    for visual_scene in visual_scenes:

        for vs in visual_scene:
            intersect = False
            for speech in speech_scenes:
                if not(vs['end'] <= speech['start']  or vs['start'] > speech['end']):
                    intersect = True
                    break
            if not intersect:
                table.append({
                    "start_time": vs["start"],
                    "end_time": vs["end"],
                    "duration": vs["end"] - vs["start"],
                    "scene_source": "visual",
                    "text": "",
                    "cuts_inside": 1
                })




    for i, row in enumerate(table, start=1):
        row["scene_id"] = f"scene_{i}"

    return table
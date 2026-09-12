import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

def merge_speech_segments(segments: List[Dict], max_gap: float = 0.5) -> List[Dict]:
    if not segments:
        return []
    segments = sorted(segments, key=lambda x: x['start'])
    merged_segments = []
    cur = segments[0].copy()
    for seg in segments[1:]:
        if seg['start'] - cur['end'] <= max_gap:
             cur['end'] = seg['end']
             cur['text'] = seg['text'] + " "+ cur['text']
        else:
            merged_segments.append(cur)
            cur = seg.copy()
        merged_segments.append(cur)
        logger.debug("Merged speech segments: %d -> %d", len(segments), len(merged_segments))
        return merged_segments
def build_combined_scene_rows(visual_scenes: List[Tuple[float,float]], speech_segments: List[Dict], max_gap: float = 0.5) -> List[Dict]:
    rows = []
    speech_merged = merge_speech_segments(speech_segments, max_gap=max_gap)
    for i, (vs, ve) in enumerate(visual_scenes, start=1):
        overlaps = [s for s in speech_merged if not (s['end'] <= vs or s['start'] >= ve)]
        speech_coverage = 0.0
        if overlaps:
            covered = sum(max(0, min(ve, s['end']) - max(vs, s['start'])) for s in overlaps)
            speech_coverage = covered / (ve - vs)
        rows.append({
            "scene_id": i,
            "start_time": vs,
            "end_time": ve,
            "duration": ve - vs,
            "scene_source": "visual",
            "speech_coverage": speech_coverage,
            "speech_segments": overlaps
        })
    for s in overlaps:
        rows.append({
        "scene_id": f"{i}_speech_{int(s['start'] * 1000)}",
        "start_time": s['start'],
        "end_time": s['end'],
        "duration": s['end'] - s['start'],
        "scene_source": "speech_based",
        "speech_coverage": 1.0,
        "speech_segments": [s]
        })
    return rows

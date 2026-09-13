import logging

logger = logging.getLogger(__name__)

def merge_speech_moments(segments, max_gap=0.3):


    # нормализация входных данных
    norm_segments = []
    for s in segments:
        if isinstance(s, dict):
            norm_segments.append({
                "start": float(s["start"]),
                "end": float(s["end"]),
                "text": s.get("text", "")
            })
        else:
            norm_segments.append({
                "start": float(s[0]),
                "end": float(s[1]),
                "text": ""
            })

    if not norm_segments:
        return []

    norm_segments = sorted(norm_segments, key=lambda s: s["start"])

    merged = []
    current = norm_segments[0].copy()

    for seg in norm_segments[1:]:
        if seg["start"] - current["end"] < max_gap:
            current["end"] = seg["end"]
            current["text"] = (current["text"] + " " + seg["text"]).strip()
        else:
            merged.append(current)
            current = seg.copy()

    merged.append(current)

    logger.info("merged %s segments", len(norm_segments) - len(merged))
    return merged

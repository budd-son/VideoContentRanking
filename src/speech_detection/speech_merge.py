import logging

logger = logging.getLogger(__name__)
def merge_speech_moments(segments, max_gap=0.3):
    if not segments:
        return []
    segments = sorted(segments, key=lambda s: s['start'])
    merged = []
    current = segments[0].copy()
    for segment in segments[1:]:
        if segment['srart'] - current['end'] < max_gap:
            current['end'] = segment['end']
            current['text'] = (current['text'] + " " +segment['start']).strip()
        else:
            merged.append(current)
            current = segment.copy()

    merged.append(current)
    logger.info("merged %s segments", len(segments) - len(merged))
    return merged
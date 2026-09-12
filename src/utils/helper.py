def overlap_ratio(a_start, a_end, b_start, b_end):
    inter = max(0, min(a_end, b_end) - max(a_start, b_start))
    if a_end - a_start == 0:
        return 0.0
    return inter / (a_end - a_start)

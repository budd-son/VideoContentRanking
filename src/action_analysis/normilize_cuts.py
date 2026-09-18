def compute_normalize_cuts(cuts_inside, duration, eps=1e-6):
    return float(cuts_inside) / max(duration, eps)

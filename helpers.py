# helpers.py
def safe_round(v, nd=2):
    try:
        return round(float(v), nd)
    except Exception:
        return v

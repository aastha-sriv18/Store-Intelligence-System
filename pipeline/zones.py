ZONES = {
    "FRAGRANCE": (0, 150, 250, 500),
    "NAIL_UNIT": (250, 150, 500, 500),
    "MAKEUP_UNIT": (500, 150, 900, 500),
    "BILLING_COUNTER": (900, 150, 1280, 500),
    "ENTRANCE": (0, 500, 250, 720)
}

def get_zone(x, y):

    for zone_name, (x1, y1, x2, y2) in ZONES.items():

        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone_name

    return "UNKNOWN"
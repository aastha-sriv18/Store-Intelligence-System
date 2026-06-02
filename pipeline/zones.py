# Store zones

ZONES = {

    "ENTRANCE": (
        0, 450,
        350, 720
    ),

    "SNACKS": (
        350, 250,
        650, 720
    ),

    "BEVERAGES": (
        650, 250,
        950, 720
    ),

    "REFRIGERATORS": (
        350, 0,
        1280, 250
    ),

    "CHECKOUT": (
        0, 0,
        350, 450
    )
}


def get_zone(x, y):

    for zone_name, (x1, y1, x2, y2) in ZONES.items():

        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone_name

    return "UNKNOWN"
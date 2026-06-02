def create_event(
    visitor_id,
    event_type,
    frame_number,
    zone=None
):

    return {
        "visitor_id": visitor_id,
        "event_type": event_type,
        "zone": zone,
        "frame_number": frame_number
    }
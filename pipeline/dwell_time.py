import json

FPS = 30


def load_events():

    with open(
        "outputs/events.json",
        "r"
    ) as f:

        return json.load(f)


def calculate_dwell_times(events):

    active_visits = {}

    dwell_results = []

    for event in events:

        visitor_id = event["visitor_id"]
        zone = event["zone"]
        frame = event["frame_number"]

        key = (
            visitor_id,
            zone
        )

        # -------------------
        # Zone Enter
        # -------------------

        if event["event_type"] == "ZONE_ENTER":

            active_visits[key] = frame

        # -------------------
        # Zone Exit
        # -------------------

        elif event["event_type"] == "ZONE_EXIT":

            if key in active_visits:

                enter_frame = active_visits[key]

                dwell_seconds = (
                    frame - enter_frame
                ) / FPS

                dwell_results.append(
                    {
                        "visitor_id": visitor_id,
                        "zone": zone,
                        "dwell_seconds": round(
                            dwell_seconds,
                            2
                        )
                    }
                )

                del active_visits[key]

    return dwell_results


if __name__ == "__main__":

    events = load_events()

    dwell_times = calculate_dwell_times(
        events
    )

    print("\n===== DWELL TIMES =====\n")

    for dwell in dwell_times[:20]:

        print(dwell)

    print(
        f"\nTotal Dwell Records: "
        f"{len(dwell_times)}"
    )

    with open(
        "outputs/dwell_times.json",
        "w"
    ) as f:

        json.dump(
            dwell_times,
            f,
            indent=4
        )

    print(
        "\nSaved to outputs/dwell_times.json"
    )
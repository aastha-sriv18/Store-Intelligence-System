# System Design

## Overview

The Store Intelligence System transforms raw CCTV footage into structured retail analytics.

Pipeline:

Video → Detection → Tracking → Event Generation → Analytics → API/Dashboard

---

## Architecture

```text
CCTV Video
    │
    ▼
YOLOv8 Detection
    │
    ▼
ByteTrack Tracking
    │
    ▼
Zone Assignment
    │
    ▼
Event Engine
    │
    ▼
events.json
    │
    ├────────► Analytics Engine
    │
    ├────────► Anomaly Detection
    │
    └────────► FastAPI + Dashboard
```

---

## Components

### Detection Layer

YOLOv8 detects people in each frame.

Output:

- Bounding Box
- Confidence Score

---

### Tracking Layer

ByteTrack assigns a persistent ID to each detected visitor.

Example:

```
Visitor #12
Visitor #13
```

---

### Event Engine

Converts detections into business events.

Supported events:

- STORE_ENTRY
- ZONE_ENTER
- ZONE_EXIT

Example:

```json
{
  "visitor_id": 12,
  "event_type": "ZONE_ENTER",
  "zone": "MAKEUP",
  "frame_number": 820
}
```

---

### Analytics Engine

Computes:

- Total Entries
- Unique Visitors
- Zone Distribution
- Dwell Time
- Customer Journeys

---

### Anomaly Detection

Detects:

- Crowded Zones
- Long Dwell Times
- Unusual Customer Behavior

---

### Dashboard

Built using Streamlit.

Displays:

- Store Metrics
- Zone Distribution
- Dwell Time
- Customer Journeys
- Heatmaps
- Anomalies

---

### API Layer

Built using FastAPI.

Provides:

- Events API
- Metrics API
- Funnel API
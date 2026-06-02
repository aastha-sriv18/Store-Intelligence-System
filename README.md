# AI-Powered Store Intelligence System

## Overview

This project is an end-to-end Store Intelligence System built for the Purplle Tech Challenge 2026.

The system processes raw CCTV footage and generates actionable retail insights using Computer Vision, Object Tracking, Event Processing, Analytics, and APIs.

The goal is to transform video streams into structured business intelligence that can help store operators understand customer movement, zone popularity, occupancy, and behavioral patterns.

---

# Features

## Computer Vision Pipeline

- Person Detection using YOLOv8
- Multi-Object Tracking using ByteTrack
- Customer Entry Detection
- Zone-Based Tracking
- Event Generation Pipeline

## Event Intelligence

The system converts raw detections into business events.

Examples:

- ENTRY
- ZONE_ENTER
- ZONE_EXIT

Example Event:

```json
{
  "visitor_id": 42,
  "event_type": "ZONE_ENTER",
  "zone": "MAKEUP",
  "timestamp": "2026-05-30T10:20:15"
}
```

---

## Analytics

Current analytics include:

- Total Entries
- Unique Visitors
- Zone Distribution

Example:

```json
{
  "total_entries": 16,
  "unique_visitors": 221,
  "zone_distribution": {
    "BILLING": 53,
    "FRAGRANCE": 62,
    "MAKEUP": 94,
    "SKINCARE": 95
  }
}
```

---

## REST API

Built using FastAPI.

Available Endpoints:

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "Store Intelligence API"
}
```

### Events

```http
GET /events
```

Returns all generated store events.

---

# Project Architecture

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
    ├────────────► Analytics Engine
    │
    └────────────► FastAPI Service
```

---

# Project Structure

```text
store-intelligence/

│
├── api/
│   └── app.py
│
├── data/
│   └── test_video.mp4
│
├── outputs/
│   └── events.json
│
├── pipeline/
│   ├── analytics.py
│   ├── entry_counter.py
│   ├── event_engine.py
│   ├── main.py
│   ├── test_coordinates.py
│   ├── test_yolo.py
│   ├── track_people.py
│   └── zones.py
│
├── README.md
│
└── requirements.txt
```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| Detection | YOLOv8 |
| Tracking | ByteTrack |
| Video Processing | OpenCV |
| Analytics | Python |
| API Layer | FastAPI |
| Server | Uvicorn |

---

# Engineering Decisions

## Why YOLOv8?

YOLOv8 provides:

- Fast inference
- Easy deployment
- Strong real-time performance
- Good balance between speed and accuracy

Trade-off:

- Lower accuracy than larger transformer-based detectors
- Significantly faster for real-time systems

---

## Why ByteTrack?

ByteTrack is a lightweight multi-object tracker that works well with YOLO detections.

Benefits:

- Real-time capable
- Easy integration
- Good ID consistency

Trade-off:

- Identity fragmentation can occur during heavy occlusion
- Same person may occasionally receive multiple IDs

---

## Why Event-Based Architecture?

Instead of storing raw detections only, the system converts detections into events.

Benefits:

- Easier analytics
- API-friendly
- Scalable architecture
- Enables future streaming systems (Kafka, Redis Streams, etc.)

Example:

```text
Detection
    ↓
Tracking
    ↓
Event Generation
    ↓
Analytics
```

---

# Current Limitations

1. Visitor count is currently based on ByteTrack IDs. Due to occlusions and re-identification limitations, the same physical visitor may receive multiple track IDs. Production systems would use person re-identification (ReID) embeddings to merge fragmented tracks.

2. Zones are manually defined.

Future versions can support dynamic store layouts through configuration files or UI-based zone creation.

3. Event timestamps currently represent processing time rather than exact video timestamps.

Future improvements will synchronize events with video frame timestamps.

---

# Future Improvements

## Dwell Time Analytics

Calculate time spent inside each store zone.

Example:

```json
{
  "visitor_id": 42,
  "zone": "SKINCARE",
  "dwell_seconds": 73
}
```

---

## Occupancy Monitoring

Real-time store occupancy tracking.

---

## Live Dashboard

Streamlit dashboard with:

- Occupancy metrics
- Zone popularity
- Visitor flow
- Event feed

---

## Anomaly Detection

Examples:

- Crowd surge detection
- Long queue detection
- Unusual dwell time
- Empty store during peak hours

---

## Event Streaming

Future versions can replace file-based event storage with:

- Apache Kafka
- Redis Streams
- RabbitMQ

for real-time event processing.

---

# Running the Project

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Pipeline

```bash
python pipeline/main.py
```

---

## Run Analytics

```bash
python pipeline/analytics.py
```

---

## Run API

```bash
uvicorn api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Challenge

Purplle Tech Challenge 2026

Theme:
AI-Powered Store Intelligence System using CCTV footage, event streaming, analytics, anomaly detection, and production-grade APIs.
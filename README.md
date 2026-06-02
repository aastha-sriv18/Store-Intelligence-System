# AI-Powered Store Intelligence System

## Overview

This project is an end-to-end **Store Intelligence System** built for the **Purplle Tech Challenge 2026**.

The system processes CCTV footage and transforms customer movements into structured retail intelligence using Computer Vision, Multi-Object Tracking, Event Processing, Analytics, and Interactive Dashboards.

The objective is to help retailers understand customer behavior, zone popularity, movement patterns, dwell time, and store utilization from CCTV footage.

---

# Features

## Computer Vision Pipeline

* Person Detection using YOLOv8
* Multi-Object Tracking using ByteTrack
* Customer Entry Detection
* Zone-Based Tracking
* Event Generation Pipeline

---

## Event Intelligence

Raw detections are converted into business events.

Supported Events:

* STORE_ENTRY
* ZONE_ENTER
* ZONE_EXIT

Example:

```json
{
  "visitor_id": 42,
  "event_type": "ZONE_ENTER",
  "zone": "REFRIGERATORS",
  "frame_number": 517
}
```

---

# Analytics

The analytics engine processes generated events and produces store-level insights.

Metrics:

* Total Entries
* Unique Visitors
* Zone Distribution

Example:

```json
{
  "total_entries": 3,
  "unique_visitors": 75,
  "zone_distribution": {
    "REFRIGERATORS": 24,
    "SNACKS": 16,
    "CHECKOUT": 52,
    "ENTRANCE": 25,
    "BEVERAGES": 7
  }
}
```

Generated File:

```text
outputs/analytics.json
```

---

# Dwell Time Analytics

Calculates the time spent by visitors inside each zone.

Example:

```json
{
  "visitor_id": 30,
  "zone": "REFRIGERATORS",
  "dwell_seconds": 4.37
}
```

Generated Files:

```text
outputs/dwell_times.json
outputs/dwell_analytics.json
```

Provides:

* Average dwell time per zone
* Visitor engagement analysis
* High-interest zone identification

---

# Customer Journey Analytics

Tracks visitor movement across store zones.

Example:

```json
{
  "30": [
    "REFRIGERATORS",
    "CHECKOUT",
    "REFRIGERATORS",
    "CHECKOUT"
  ]
}
```

Generated File:

```text
outputs/journeys.json
```

Provides:

* Customer flow analysis
* Popular navigation paths
* Zone transition patterns

---

# Heatmap Generation

Generates a heatmap using tracked visitor positions.

Output:

```text
outputs/heatmap.png
```

Provides:

* High traffic areas
* Customer concentration zones
* Store layout insights

---

# Interactive Dashboard

Built using Streamlit.

Dashboard Features:

* Store Overview
* Total Entries
* Unique Visitors
* Zone Distribution
* Average Dwell Time
* Customer Journey Samples
* Heatmap Visualization

Launch:

```bash
streamlit run dashboard.py
```

---

# REST API

Built using FastAPI.

## Health Check

```http
GET /
```

Response:

```json
{
  "message": "Store Intelligence API"
}
```

---

## Events

```http
GET /events
```

Returns all generated events.

Example:

```json
[
  {
    "visitor_id": 42,
    "event_type": "ZONE_ENTER",
    "zone": "CHECKOUT",
    "frame_number": 152
  }
]
```

---

# System Architecture

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
    ├──────────► Analytics Engine
    │
    ├──────────► Dwell Time Engine
    │
    ├──────────► Journey Analysis
    │
    ├──────────► Heatmap Generator
    │
    ├──────────► Streamlit Dashboard
    │
    └──────────► FastAPI Service
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
│   ├── analytics.json
│   ├── dwell_times.json
│   ├── dwell_analytics.json
│   ├── journeys.json
│   ├── events.json
│   ├── positions.json
│   └── heatmap.png
│
├── pipeline/
│   ├── analytics.py
│   ├── dwell_time.py
│   ├── dwell_analytics.py
│   ├── journeys.py
│   ├── heatmap.py
│   ├── event_engine.py
│   ├── main.py
│   └── zones.py
│
├── dashboard.py
│
├── README.md
│
└── requirements.txt
```

---

# Technology Stack

| Component        | Technology |
| ---------------- | ---------- |
| Language         | Python     |
| Detection        | YOLOv8     |
| Tracking         | ByteTrack  |
| Video Processing | OpenCV     |
| Analytics        | Python     |
| Dashboard        | Streamlit  |
| API Layer        | FastAPI    |
| Server           | Uvicorn    |

---

# Engineering Decisions

## Why YOLOv8?

YOLOv8 was selected because it provides:

* Fast inference speed
* Lightweight deployment
* Real-time performance
* Strong object detection accuracy

Trade-off:

* Slightly lower accuracy than larger transformer-based models
* Better suited for real-time retail analytics

---

## Why ByteTrack?

ByteTrack is a lightweight multi-object tracking algorithm that integrates easily with YOLO detections.

Benefits:

* Real-time capable
* Efficient tracking
* Low computational overhead

Trade-off:

* Identity fragmentation can occur during occlusions
* Same visitor may occasionally receive multiple IDs

---

## Why Event-Based Architecture?

Instead of storing only detections, the system converts detections into business events.

Benefits:

* Easier analytics
* API-friendly design
* Scalable architecture
* Supports future streaming systems

Pipeline:

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

## Visitor Re-Identification

Visitor counting currently relies on ByteTrack tracking IDs.

Because of:

* Occlusions
* Missed detections
* Tracker resets

the same customer may occasionally receive multiple IDs.

Future versions can integrate:

* DeepSORT
* BoT-SORT
* Person Re-Identification (ReID)

to improve identity consistency.

---

## Manual Zone Configuration

Store zones are currently defined manually inside the code.

Future improvements:

* Dynamic zone configuration
* UI-based zone creation
* Configuration-driven layouts

---

## Single Camera Support

Current implementation processes a single CCTV feed.

Future versions can support:

* Multi-camera analytics
* Cross-camera tracking
* Store-wide customer journeys

---

# Future Improvements

## Real-Time Analytics

* Live occupancy monitoring
* Live visitor counts
* Streaming event dashboard

---

## Queue Monitoring

Detect:

* Long checkout queues
* Waiting times
* Congested areas

---

## Anomaly Detection

Examples:

* Crowd surges
* Unusual dwell times
* Empty store alerts
* Suspicious movement patterns

---

## Event Streaming

Replace file-based event storage with:

* Apache Kafka
* Redis Streams
* RabbitMQ

for production-scale event processing.

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

## Run Tracking Pipeline

```bash
python -m pipeline.main
```

Generates:

```text
events.json
positions.json
```

---

## Run Analytics

```bash
python -m pipeline.analytics
```

Generates:

```text
analytics.json
```

---

## Run Dwell Time Analysis

```bash
python -m pipeline.dwell_time
```

```bash
python -m pipeline.dwell_analytics
```

Generates:

```text
dwell_times.json
dwell_analytics.json
```

---

## Run Journey Analysis

```bash
python -m pipeline.journeys
```

Generates:

```text
journeys.json
```

---

## Generate Heatmap

```bash
python -m pipeline.heatmap
```

Generates:

```text
heatmap.png
```

---

## Run Dashboard

```bash
streamlit run dashboard.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## Run API

```bash
uvicorn api.app:app --reload
```

API URL:

```text
http://127.0.0.1:8000
```

---

# Challenge

Purplle Tech Challenge 2026

Theme:

**AI-Powered Store Intelligence System using CCTV footage, computer vision, event processing, analytics, dashboards, and production-grade APIs.**

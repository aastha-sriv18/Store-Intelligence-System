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
  "zone": "MAKEUP",
  "frame_number": 517
}
```

---

## Analytics

The analytics engine processes generated events and produces store-level insights.

- Total Entries
- Unique Visitors
- Zone Distribution
- Customer Journey Analysis
- Dwell Time Analytics
- Store Heatmap Generation
- Anomaly Detection

Example:

```json
{
  "total_entries": 3,
  "unique_visitors": 75,
  "zone_distribution": {
    "ENTRANCE": 25,
    "FRAGRANCE": 18,
    "MAKEUP": 31,
    "NAIL_UNIT": 12,
    "BRAND_WALL": 21,
    "CHECKOUT": 52
  }
}
```

Generated File:

```text
outputs/analytics.json
```

---

## Dwell Time Analytics

Calculates the time spent by visitors inside each zone.

Example:

```json
{
  "visitor_id": 30,
  "zone": "SKINCARE",
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

## Customer Journey Analytics

Tracks visitor movement across store zones.

Example:

```json
{
  "30": [
    "SKINCARE",
    "CHECKOUT",
    "HAIRCARE",
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

## Heatmap Generation

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

## Sales Analytics

This module computes key business KPIs from `data/sales.csv` and combines them with visitor analytics from `outputs/analytics.json`.

### Inputs
- `data/sales.csv` → transactional sales data (`order_id`, `GMV`)
- `outputs/analytics.json` → visitor analytics (`unique_visitors`)

### Computed Metrics
- Total Orders: number of unique orders
- Total Revenue: sum of GMV
- Average Basket Value: Total Revenue / Total Orders
- Conversion Rate: (Total Orders / Unique Visitors) × 100

```bash
python -m pipeline.sales_analytics
```

### Output
Generated metrics are saved to:

```text
outputs/sales_metrics.json
```

### 🌐 API Endpoint

**GET** `/sales-metrics`

Returns the latest computed sales KPIs from `sales_metrics.json`.

This endpoint automatically runs the sales analytics computation using the latest `data/sales.csv` and `outputs/analytics.json` before returning the response.

---

### 🔁 Recompute Endpoint (Optional)

**POST** `/recompute-sales-metrics`

Triggers recomputation of sales metrics from raw data.

It regenerates `outputs/sales_metrics.json` using the latest available:
- `data/sales.csv`
- `outputs/analytics.json`

Returns the updated KPI object after recomputation.

---

## Anomaly Detection

The system automatically identifies unusual customer behavior patterns from generated events.

Supported anomalies:

### Long Dwell Time

Detects customers spending an unusually long time inside a zone.

Example:

```json
{
  "visitor_id": 42,
  "anomaly": "LONG_DWELL_TIME",
  "zone": "MAKEUP",
  "dwell_seconds": 15.4
}
```

### Excessive Zone Switching

Detects customers repeatedly moving between multiple zones.

Example:

```json
{
  "visitor_id": 18,
  "anomaly": "EXCESSIVE_ZONE_SWITCHING",
  "zones_visited": 7
}
```

### Direct Checkout

Detects visitors who move directly from the entrance to checkout.

Example:

```json
{
  "visitor_id": 31,
  "anomaly": "DIRECT_CHECKOUT"
}
```

Detected anomalies are stored in:

```text
outputs/anomalies.json
```

---

## Interactive Dashboard

Built using Streamlit.

Dashboard Features:

* Store Overview
* Total Entries
* Unique Visitors
* Zone Distribution
* Average Dwell Time
* Customer Journey Samples
* Anomaly Detection Results
* Heatmap Visualization
* Conversion Funnel

Launch:

```bash
streamlit run dashboard.py
```

---

## Deployment

- Dockerized application
- One-command deployment using Docker Compose
- FastAPI service
- Streamlit dashboard

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
    |
    ├──────────► Sales Analysis
    │
    ├──────────► Heatmap Generator
    │
    ├──────────► Anomaly Detection
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
|   ├── anomalies.json
│   ├── dwell_times.json
│   ├── dwell_analytics.json
│   ├── funnel.json
│   ├── journeys.json
│   ├── events.json
│   ├── positions.json
|   ├── heatmap.png
│   └── sales_metrics.json
│
├── pipeline/
│   ├── analytics.py
|   ├── anomaly_detection.py
│   ├── dwell_time.py
│   ├── dwell_analytics.py
│   ├── funnel.py
│   ├── journeys.py
│   ├── heatmap.py
│   ├── event_engine.py
│   ├── main.py
│   ├── sales_analytics.py
│   └── zones.py
│
├── dashboard.py
│
├── CHOICES.md
|
├── DESIGN.md
|
├── README.md
│
├── Dockerfile
|
├── docker-compose.yml
|
└── requirements.txt
```

---

# Technology Stack

| Component        | Technology     |
| ---------------- | -------------- |
| Language         | Python         |
| Detection        | YOLOv8         |
| Tracking         | ByteTrack      |
| Video Processing | OpenCV         |
| Analytics        | Python         |
| Dashboard        | Streamlit      |
| API Layer        | FastAPI        |
| Server           | Uvicorn        |
| Containerization | Docker         |
| Deployment       | Docker Compose |


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

## Store zones and entry boundaries are currently configured manually.

Current implementation uses manually defined zones that approximate the provided Purplle store layout:

- Entrance
- Fragrance Island
- Nail Unit
- Makeup Island
- Brand Wall Displays
- Checkout Counter

The challenge includes multiple store layouts and camera viewpoints. Therefore, zone coordinates are configured per video and are intended to demonstrate the analytics pipeline rather than represent a single universal layout.

---

## Anomaly detection currently uses rule-based thresholds.

Future versions can incorporate machine learning models to learn normal customer behavior patterns and automatically detect unusual activity.

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

## Event Streaming

Replace file-based event storage with:

* Apache Kafka
* Redis Streams
* RabbitMQ

for production-scale event processing.

---

## Zone Configuration

Future versions can automatically map floor-plan layouts to camera views using homography and calibration techniques.

Benefits:

- Accurate zone analytics
- Store-specific customer journeys
- Reduced manual configuration
- Better alignment with retail floor plans

---

# Docker Deployment

Build and run the complete system:

```bash
docker compose up --build
```

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

## Run Complete Analysis At Once 

```bash
python -m pipeline.run_all
```

Generates:
Analytics, anomalies, dwell times, funnel conversion, heatmap, journeys and sales_metrics at once.

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

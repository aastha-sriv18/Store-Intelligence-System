# Engineering Choices

## Why YOLOv8?

YOLOv8 provides:

- Fast inference
- Easy deployment
- Good real-time performance
- Strong community support

Tradeoff:

- Slightly lower accuracy than larger transformer-based models

---

## Why ByteTrack?

ByteTrack is lightweight and integrates well with YOLO detections.

Benefits:

- Real-time capable
- Stable tracking
- Easy implementation

Tradeoff:

- Identity fragmentation can occur during occlusions

---

## Why Event-Based Design?

Instead of storing only detections, the system converts observations into events.

Benefits:

- Easier analytics
- API friendly
- Scalable architecture

---

## Why Zone-Based Analytics?

Retail decisions are made around store sections rather than individual coordinates.

Zones allow:

- Heatmap generation
- Dwell time analysis
- Popularity tracking

---

## Zone Design Decisions

The challenge provided store layouts showing key retail areas such as:

- Fragrance
- Nail Unit
- Makeup
- Skincare
- Haircare
- Billing Counter

Instead of using generic retail zones, the system maps tracked visitors into beauty-specific business zones.

This improves business relevance because metrics such as:

- Zone popularity
- Dwell time
- Conversion funnel
- Customer journeys

can be directly linked to merchandising areas within the store.

Zones are currently manually defined using pixel coordinates derived from the store layout and camera viewpoint. This approach was chosen for simplicity and reproducibility within the challenge timeframe.

---

## Why Virtual Entry Line?

A configurable line crossing approach is simple and effective for visitor counting.

Tradeoff:

- Requires camera-specific positioning

---

## Assumptions Made

Several assumptions were required due to the limited information available from CCTV footage alone:

1. Each ByteTrack ID represents a unique visitor session.

2. The entry line was manually defined based on the visible store entrance in the provided footage.

3. Zone boundaries were approximated from camera perspective and store layout information.

4. Customer journeys are inferred from zone transitions rather than exact shopper intent.

These assumptions enabled the creation of a complete working system while maintaining explainable business metrics.

---

## Limitations

- ByteTrack may assign multiple IDs to the same person.
- Entry line must be configured for each store.
- Zones are manually defined.
- Multi-camera identity matching is not implemented.
- Billing data integration is currently limited.
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("data/test1.jpg")

for result in results:

    for box in result.boxes:

        cls = int(box.cls[0])

        conf = float(box.conf[0])

        print(
            f"Class={cls}, Confidence={conf:.2f}"
        )
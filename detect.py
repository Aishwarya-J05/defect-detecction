import cv2
import os
import json
from ultralytics import YOLO
from explain import explain_defect

# Load your trained model
model = YOLO("best.pt")

COLORS = {
    "HIGH":   (0, 0, 255),    # Red
    "MEDIUM": (0, 165, 255),  # Orange
    "LOW":    (0, 255, 0)     # Green
}

def detect_defects(image_path):
    image = cv2.imread(image_path)
    results = model(image_path)[0]
    
    detections = []

    for box in results.boxes:
        # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        location = f"x:{x1} y:{y1} w:{x2-x1} h:{y2-y1}"

        # Crop the defect region
        crop_path = f"temp_crop_{class_name}.jpg"
        crop = image[y1:y2, x1:x2]
        cv2.imwrite(crop_path, crop)

        # Get GenAI explanation
        explanation = explain_defect(crop_path, class_name, confidence, location)
        os.remove(crop_path)

        # Draw bounding box on image
        color = COLORS.get(explanation["severity"], (255, 255, 255))
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        label = f"{class_name} {confidence:.0%}"
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        detections.append({
            "defect_type": class_name,
            "confidence": confidence,
            "location": location,
            "explanation": explanation["explanation"],
            "probable_cause": explanation["probable_cause"],
            "recommended_action": explanation["recommended_action"],
            "severity": explanation["severity"]
        })

    # Save annotated image
    output_path = "output_annotated.jpg"
    cv2.imwrite(output_path, image)

    return {
        "annotated_image": output_path,
        "detections": detections
    }
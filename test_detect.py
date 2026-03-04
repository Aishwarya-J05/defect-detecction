from detect import detect_defects
import json

result = detect_defects("test.jpg")

print("Detections found:", len(result["detections"]))
print("Annotated image saved to:", result["annotated_image"])

for i, det in enumerate(result["detections"]):
    print(f"\n--- Defect {i+1} ---")
    print(f"Type:       {det['defect_type']}")
    print(f"Confidence: {det['confidence']:.1%}")
    print(f"Severity:   {det['severity']}")
    print(f"Explanation:{det['explanation']}")
    print(f"Cause:      {det['probable_cause']}")
    print(f"Action:     {det['recommended_action']}")
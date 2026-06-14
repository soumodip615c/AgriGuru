from ultralytics import YOLO
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "plant_disease" / "best.pt"

model = YOLO(str(MODEL_PATH))


def predict_disease(image_path):

    results = model.predict(
        source=image_path,
        verbose=False
    )

    result = results[0]

    probs = result.probs.data.tolist()

    class_id = probs.index(max(probs))

    disease_name = result.names[class_id]

    confidence = round(max(probs) * 100, 2)

    return {
        "disease": disease_name,
        "confidence": confidence
    }
from libreyolo import LibreYOLO
import torch

if __name__ == "__main__":
    if torch.cuda.is_available():
        model = LibreYOLO("LibreYOLO9s.pt")
        
        results = model.train(
            data="data.yaml",
            epochs=100,
            batch=16,
            imgsz=640,
            lr=0.01,
            save_period=10,
            device=0,
            plots=False
        )

        # Mark: Does not work properly, find another way to export the model to TFlite format
        path = model.export(
            format="tflite",
            path="/weights/trained.tflite"
        )

        print(f"Training complete, saved model to {path}")
    else:
        print("No cuda found. Training would take decades ;(")
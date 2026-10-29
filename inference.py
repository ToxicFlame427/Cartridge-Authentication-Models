from libreyolo import LibreYOLO

# MARK: Note, that is insanely simple :)
model = LibreYOLO("runs/train/yolo9_exp4/weights/best.pt")

result = model(
    "test_images/1_large.jpg",
    save=True
)
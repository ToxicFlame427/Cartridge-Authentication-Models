from libreyolo import LibreYOLO
import cv2
from os import listdir
import sys

# Gets all images in the directory specified (.jpg)
def getTestImages(path):
    print(f"Getting test images from {path}")

    found_images = []
    # TODO: FIx this function
    for image in listdir(path):
        if image.endswith(".jpg"):
            found_images.append(f"{path}{image}")

    print(found_images)

    return found_images

# Gets all negative tag names based on the cart type selected
def getNegTags(path):
    tags = []

    with open(f"{path}negative_tags.txt", 'r') as file:
        tags = [
            # Put in viable format
            line.strip() for line in file.readlines() if line.strip()
        ]

    return tags


results = [] # Stores annotated result
ann_type = str(sys.argv[1]) # Stores the argument model type
test_path = f"test_images/{ann_type}/" # Location of test images
save_path = "annotated/" # The base path for annotations
tags_path = f"tags/{ann_type}/" # Base path that stroes annotation tags

# For custom annotation colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)

test_images = getTestImages(test_path)
negative_tags = getNegTags(tags_path)

if test_images != []:
    print("Running inference on the test images")
    # MARK: Note, that is insanely simple :)
    model = LibreYOLO("runs/train/yolo9_exp4/weights/best.pt")

    i = 0
    # Each image in the folder will get annotated
    for image in test_images:
        results.append(
            model(image)
        )

        # Allows manual annotations to be written
        cv2_img = cv2.imread(image)

        # After the inference, change the box colors
        for box in results[i].boxes:
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)

            cls_id = int(box.cls)
            conf = float(box.conf)
            class_name = results[i].names[cls_id]

            # Check if any of the annotation are negative
            if class_name in negative_tags:
                box_color = RED
            else:
                box_color = GREEN

            # Set the labels and colors of the annotations
            label = f"{class_name} {conf:.2f}"
            cv2.rectangle(cv2_img, (x1, y1), (x2, y2), box_color, thickness=2)
            cv2.putText(cv2_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

       
        save = f"{save_path}{ann_type}_ann{i}.jpg"
        # Write the image
        cv2.imwrite(save, cv2_img)

        i = i + 1

    print(f"Inference complete! See {save_path} to see the results.")

else:
    print(f"No images have been found in {save_path}{ann_type}")
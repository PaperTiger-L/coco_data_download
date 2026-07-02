import json
from pathlib import Path

ANIMAL_CATEGORIES = {
    "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe",
}


def convert_annotation_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    old_categories = data["categories"]
    old_category_id_to_name = {}

    for category in old_categories:
        old_category_id_to_name[category["id"]] = category["name"]

    new_categories = [
        {"id": 1, "name": "person", "supercategory": "person"},
        {"id": 2, "name": "pet", "supercategory": "animal"},
    ]

    new_annotations = []
    used_image_ids = set()

    for annotation in data["annotations"]:
        old_category_name = old_category_id_to_name[annotation["category_id"]]

        if old_category_name == "person":
            new_annotation = annotation.copy()
            new_annotation["category_id"] = 1
            new_annotations.append(new_annotation)
            used_image_ids.add(new_annotation["image_id"])
        elif old_category_name in ANIMAL_CATEGORIES:
            new_annotation = annotation.copy()
            new_annotation["category_id"] = 2
            new_annotations.append(new_annotation)
            used_image_ids.add(new_annotation["image_id"])

    new_images = []

    for image in data["images"]:
        if image["id"] in used_image_ids:
            new_images.append(image)

    new_data = {
        "images": new_images,
        "annotations": new_annotations,
        "categories": new_categories,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f)

    print(f"saved: {output_path}")
    print(f"images: {len(new_images)}")
    print(f"annotations: {len(new_annotations)}")
    print(f"categories: {[c['name'] for c in new_categories]}")


def main():
    input_dir = Path("coco2017/filtered/annotations")

    convert_annotation_file(
        input_dir / "instances_train2017.json",
        input_dir / "instances_train2017_person_pet.json",
    )

    convert_annotation_file(
        input_dir / "instances_val2017.json",
        input_dir / "instances_val2017_person_pet.json",
    )


if __name__ == "__main__":
    main()

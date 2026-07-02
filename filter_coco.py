import json
import shutil
from pathlib import Path

ANIMAL_CATEGORIES = {
    "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe",
}

TARGET_CATEGORIES = {"person"} | ANIMAL_CATEGORIES


def process_split(split_name, annotation_file_name):
    annotation_path = Path("coco2017/annotations") / annotation_file_name

    with open(annotation_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\nprocessing {split_name}")
    print(f"loaded annotation file: {annotation_path}")

    categories = data["categories"]
    target_category_ids = set()
    target_categories = []

    for category in categories:
        if category["name"] in TARGET_CATEGORIES:
            target_category_ids.add(category["id"])
            target_categories.append(category)

    print(f"target category ids: {sorted(target_category_ids)}")

    annotations = data["annotations"]
    target_annotations = []
    target_image_ids = set()

    for annotation in annotations:
        if annotation["category_id"] in target_category_ids:
            target_annotations.append(annotation)
            target_image_ids.add(annotation["image_id"])

    print(f"target annotations count: {len(target_annotations)}")
    print(f"target images count: {len(target_image_ids)}")

    images = data["images"]
    target_images = []
    target_file_names = []

    for image in images:
        if image["id"] in target_image_ids:
            target_images.append(image)
            target_file_names.append(image["file_name"])

    print(f"target image records count: {len(target_images)}")
    print(f"target file count: {len(target_file_names)}")
    print(f"first 5 files: {target_file_names[:5]}")

    source_dir = Path("coco2017") / split_name
    output_dir = Path("coco2017/filtered") / split_name
    output_dir.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    total_files = len(target_file_names)

    for index, file_name in enumerate(target_file_names, start=1):
        source_path = source_dir / file_name
        target_path = output_dir / file_name

        if source_path.exists():
            shutil.copy2(source_path, target_path)
            copied_count += 1

        print(f"\rcopying {split_name}: {index}/{total_files}", end="")

    print()
    print(f"copied files: {copied_count}")

    filtered_data = {
        "images": target_images,
        "annotations": target_annotations,
        "categories": target_categories,
    }

    annotations_output_dir = Path("coco2017/filtered/annotations")
    annotations_output_dir.mkdir(parents=True, exist_ok=True)

    output_annotation_path = annotations_output_dir / annotation_file_name

    with open(output_annotation_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f)

    print(f"filtered annotation saved to: {output_annotation_path}")


def main():
    process_split("train2017", "instances_train2017.json")
    process_split("val2017", "instances_val2017.json")


if __name__ == "__main__":
    main()

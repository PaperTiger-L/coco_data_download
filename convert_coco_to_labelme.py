import json
import shutil
from pathlib import Path


def coco_bbox_to_labelme_points(bbox):
    x, y, w, h = bbox
    return [
        [x, y],
        [x + w, y + h],
    ]


def convert_coco_file_to_labelme(input_json_path, image_dir, output_dir):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = data["categories"]
    images = data["images"]
    annotations = data["annotations"]

    category_id_to_name = {}
    for category in categories:
        category_id_to_name[category["id"]] = category["name"]

    image_id_to_info = {}
    for image in images:
        image_id_to_info[image["id"]] = image

    image_id_to_shapes = {}
    for annotation in annotations:
        image_id = annotation["image_id"]
        label = category_id_to_name[annotation["category_id"]]
        points = coco_bbox_to_labelme_points(annotation["bbox"])

        shape = {
            "label": label,
            "points": points,
            "group_id": None,
            "description": "",
            "shape_type": "rectangle",
            "flags": {},
        }

        if image_id not in image_id_to_shapes:
            image_id_to_shapes[image_id] = []

        image_id_to_shapes[image_id].append(shape)

    output_dir.mkdir(parents=True, exist_ok=True)

    total_images = len(image_id_to_info)

    for index, (image_id, image_info) in enumerate(image_id_to_info.items(), start=1):
        file_name = image_info["file_name"]
        json_name = Path(file_name).stem + ".json"

        source_image_path = image_dir / file_name
        target_image_path = output_dir / file_name
        if source_image_path.exists():
            shutil.copy2(source_image_path, target_image_path)

        labelme_data = {
            "version": "5.0.1",
            "flags": {},
            "shapes": image_id_to_shapes.get(image_id, []),
            "imagePath": file_name,
            "imageData": None,
            "imageHeight": image_info["height"],
            "imageWidth": image_info["width"],
        }

        output_json_path = output_dir / json_name
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(labelme_data, f, ensure_ascii=False, indent=2)

        print(f"\rprocessing {output_dir.name}: {index}/{total_images}", end="")

    print()
    print(f"saved labelme files to: {output_dir}")


def main():
    annotation_dir = Path("coco2017/filtered/annotations")

    convert_coco_file_to_labelme(
        annotation_dir / "instances_train2017_person_animal.json",
        Path("coco2017/filtered/train2017"),
        Path("coco2017/labelme/train2017"),
    )

    convert_coco_file_to_labelme(
        annotation_dir / "instances_val2017_person_animal.json",
        Path("coco2017/filtered/val2017"),
        Path("coco2017/labelme/val2017"),
    )


if __name__ == "__main__":
    main()

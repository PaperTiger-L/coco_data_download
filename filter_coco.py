import json
from pathlib import Path
import shutil

ANIMAL_CATEGORIES = {
    "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe",
}

TARGET_CATEGORIES = {"person"} | ANIMAL_CATEGORIES

def main():
    annotation_path = Path('coco2017/annotations/instances_train2017.json')

    with open(annotation_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = data['categories']
    print(f'categories count: {len(categories)}')

    target_category_ids = set()

    for category in categories:
        if category['name'] in TARGET_CATEGORIES:
            target_category_ids.add(category['id'])

    print(f'target category ids:{sorted(target_category_ids)}')

    annotations = data['annotations']
    target_image_ids = set()

    for annotation in annotations:
        if annotation['category_id'] in target_category_ids:
            target_image_ids.add(annotation['image_id'])      
    
    print(f'target images count: {len(target_image_ids)}')

    images = data['images']
    target_file_names = []

    for image in images:
        if image['id'] in target_image_ids:
            target_file_names.append(image['file_name'])
    
    print(f'target file count:{len(target_file_names)}')
    print(f'first 5 files: {target_file_names[:5]}')

    source_dir = Path('coco2017/train2017')
    output_dir = Path('coco2017/filtered/train2017')
    output_dir.mkdir(parents=True, exist_ok=True)

    copied_count = 0

    for file_name in target_file_names:
        source_path = source_dir / file_name
        target_path = output_dir /file_name

        if source_path.exists():
            shutil.copy2(source_path, target_path)
            copied_count += 1

    print(f'copied files:{copied_count}')



if __name__ == '__main__':
    main()
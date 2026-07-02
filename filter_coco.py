import json
from pathlib import Path

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
            target_category_ids.add(annotation['image_id'])      
    
    print(f'target images count: {len(target_category_ids)}')
    

if __name__ == '__main__':
    main()
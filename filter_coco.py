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

if __name__ == '__main__':
    main()
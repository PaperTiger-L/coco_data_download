import sys
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

FILES = {
    "train2017.zip": "http://images.cocodataset.org/zips/train2017.zip",
    "val2017.zip": "http://images.cocodataset.org/zips/val2017.zip",
    "annotations_trainval2017.zip": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
}

DOWNLOAD_DIR = Path("coco2017") / "archives"

def format_size(num_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(num_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f'{size:.2f} {unit}'
        size /= 1024

def show_progress(block_num, block_size, total_size):
    downloaded = block_num * block_size

    if total_size > 0:
        downloaded = min(downloaded, total_size)
        percent = downloaded / total_size * 100
        message = f'\r{percent:6.2f}% {format_size(downloaded)} / {format_size(total_size)}'
    else:
        message = f'\r{format_size(downloaded)}'

    sys.stdout.write(message)
    sys.stdout.flush()

def download_file(filename, url):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DOWNLOAD_DIR / filename

    if output_path.exists():
        print(f'跳过，文件已存在：{output_path}')
        return

    print(f'开始下载：{filename}')
    urllib.request.urlretrieve(url, output_path, reporthook=show_progress)
    print()
    print(f'下载完成：{output_path}')




def main():
    for file_name, url in FILES.items():
        download_file(file_name, url)
        

if __name__ == '__main__':
    main()


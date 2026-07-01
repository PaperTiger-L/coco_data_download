import sys
import urllib.request
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


def get_remote_file_size(url):
    with urllib.request.urlopen(url) as response:
        return int(response.headers.get('Content-Length', 0))


def download_file(filename, url):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DOWNLOAD_DIR / filename

    remote_size = get_remote_file_size(url)
    local_size = output_path.stat().st_size if output_path.exists() else 0

    if remote_size > 0 and local_size >= remote_size:
        print(f'跳过，文件已下载完成：{output_path}')
        return

    print(f'开始下载：{filename}')
    print(f'本地已下载：{format_size(local_size)} / {format_size(remote_size)}')
    request = urllib.request.Request(url)

    if local_size > 0:
        request.add_header('Range', f'bytes={local_size}-')

    with urllib.request.urlopen(request) as response:

        if local_size > 0 and response.status != 206:
            raise RuntimeError('服务器不支持断点续传，请删除残缺文件后重新下载')

        with open(output_path, 'ab') as f:
            chunk_size = 1024 * 1024
            downloaded = local_size

            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break

                f.write(chunk)
                downloaded += len(chunk)

                if remote_size > 0:
                    percent = downloaded / remote_size * 100
                    message = f'\r{percent:6.2f}% {format_size(downloaded)} / {format_size(remote_size)}'

                else:
                    message = f'\r{format_size(downloaded)}'
                
                sys.stdout.write(message)
                sys.stdout.flush()
    final_size = output_path.stat().st_size
    if remote_size > 0 and final_size != remote_size:
        raise RuntimeError(
            f'下载不完整：{output_path}，本地大小 {final_size}，远程大小 {remote_size}'
        )
    
    print()



def main():
    for filename, url in FILES.items():
        download_file(filename, url)


if __name__ == '__main__':
    main()


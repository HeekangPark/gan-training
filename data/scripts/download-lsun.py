import os
import subprocess
from urllib.request import Request, urlopen

__author__ = 'Fisher Yu'
__email__ = 'fy@cs.princeton.edu'
__license__ = 'MIT'


def list_categories():
    url = 'http://dl.yf.io/lsun/categories.txt'
    with urlopen(Request(url)) as response:
        return response.read().decode().strip().split('\n')


def download(out_dir, category, set_name):
    url = 'http://dl.yf.io/lsun/scenes/{category}_' \
          '{set_name}_lmdb.zip'.format(**locals())
    if set_name == 'test':
        out_name = 'test_lmdb.zip'
        url = 'http://dl.yf.io/lsun/scenes/{set_name}_lmdb.zip'
    else:
        out_name = '{category}_{set_name}_lmdb.zip'.format(**locals())
    out_path = os.path.join(out_dir, out_name)
    cmd = ['curl', url, '-o', out_path]
    print('Downloading', category, set_name, 'set')
    subprocess.call(cmd)


def main(out_dir='', category=None):
    categories = list_categories()
    if category is None:
        print('Downloading', len(categories), 'categories')
        for category in categories:
            download(out_dir, category, 'train')
            download(out_dir, category, 'val')
        download(out_dir, '', 'test')
    else:
        if category == 'test':
            download(out_dir, '', 'test')
        elif category not in categories:
            print('Error:', category, "doesn't exist in", 'LSUN release')
        else:
            download(out_dir, category, 'train')
            download(out_dir, category, 'val')


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = "data/lsun"

    os.system(f"rm -rf {os.path.join(root_dir, data_dir)}")
    os.system(f"mkdir -p {os.path.join(root_dir, data_dir)}")

    zips_dir = os.path.join(root_dir, data_dir, "zips")
    os.system(f"mkdir {zips_dir}")
    
    main(out_dir=zips_dir)

    for file in [os.path.join(zips_dir, file) for file in os.listdir(zips_dir) if file.endswith(".zip")]:
        os.system(f"unzip {file} -d {os.path.join(root_dir, data_dir)}")

import os
from tempfile import TemporaryDirectory
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = "data/celeba/real"

os.system(f"rm -rf {os.path.join(root_dir, data_dir)}")
os.system(f"mkdir -p {os.path.dirname(os.path.join(root_dir, data_dir))}")
with TemporaryDirectory() as temp_dir:
    api.dataset_download_files("jessicali9530/celeba-dataset", path=temp_dir, force=True, quiet=False, unzip=True)
    os.system(f"mv {os.path.join(temp_dir, 'img_align_celeba', 'img_align_celeba')} {os.path.join(root_dir, data_dir)}")

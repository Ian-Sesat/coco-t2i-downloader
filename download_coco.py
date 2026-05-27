"""
MS-COCO Download Script
Downloads MS-COCO 2017 Train and Val images + captions from cocodataset.org.

Train2017 : 118,287 images (18GB)
Val2017   :   5,000 images (1GB)
Total     : 123,287 images × 5 captions = 616,435 queries

Gallery : all 123,287 images
Queries : all 616,435 captions
"""

import os
import json
import zipfile
import urllib.request
from tqdm import tqdm

SAVE_DIR     = '/media/isesat/e8188905-1ffc-4de1-83b6-ac2addc2a941/coco'
IMAGES_DIR   = os.path.join(SAVE_DIR, 'images')
ANNOT_DIR    = os.path.join(SAVE_DIR, 'annotations')
CAPTION_FILE = os.path.join(SAVE_DIR, 'captions.json')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(ANNOT_DIR,  exist_ok=True)

URLS = {
    'train_images' : 'http://images.cocodataset.org/zips/train2017.zip',
    'val_images'   : 'http://images.cocodataset.org/zips/val2017.zip',
    'annotations'  : 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip',
}


def download_file(url, save_path):
    print(f"Downloading: {os.path.basename(save_path)}")
    with urllib.request.urlopen(url) as response:
        total = int(response.headers.get('Content-Length', 0))
    with tqdm(total=total, unit='B', unit_scale=True) as pbar:
        urllib.request.urlretrieve(url, save_path,
            lambda b, bs, t: pbar.update(bs))


def extract_zip(zip_path, extract_to):
    print(f"Extracting: {os.path.basename(zip_path)}")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in tqdm(z.namelist(), desc="Extracting"):
            z.extract(member, extract_to)
    os.remove(zip_path)


annot_zip = os.path.join(SAVE_DIR, 'annotations.zip')
if not os.path.exists(os.path.join(ANNOT_DIR, 'captions_train2017.json')):
    download_file(URLS['annotations'], annot_zip)
    extract_zip(annot_zip, SAVE_DIR)
else:
    print("Annotations already downloaded")

train_zip = os.path.join(SAVE_DIR, 'train2017.zip')
if not os.path.exists(os.path.join(IMAGES_DIR, 'train2017')):
    download_file(URLS['train_images'], train_zip)
    extract_zip(train_zip, IMAGES_DIR)
else:
    print("Train images already downloaded")

val_zip = os.path.join(SAVE_DIR, 'val2017.zip')
if not os.path.exists(os.path.join(IMAGES_DIR, 'val2017')):
    download_file(URLS['val_images'], val_zip)
    extract_zip(val_zip, IMAGES_DIR)
else:
    print("Val images already downloaded")

images  = []
queries = []

for split, caption_file, img_subdir in [
    ('train', 'captions_train2017.json', 'train2017'),
    ('val',   'captions_val2017.json',   'val2017'),
]:
    with open(os.path.join(ANNOT_DIR, caption_file)) as f:
        data = json.load(f)

    id_to_filename = {img['id']: img['file_name'] for img in data['images']}

    id_to_captions = {}
    for ann in data['annotations']:
        id_to_captions.setdefault(ann['image_id'], []).append(ann['caption'])

    for img_id, filename in tqdm(id_to_filename.items(), desc=f"Processing {split}"):
        images.append({'img_id': str(img_id), 'filename': filename})
        for caption in id_to_captions.get(img_id, []):
            queries.append({'img_id': str(img_id), 'caption': caption})

with open(CAPTION_FILE, 'w') as f:
    json.dump({'images': images, 'queries': queries}, f, indent=2)

print(f"Images saved  : {len(images):,}")
print(f"Queries saved : {len(queries):,}")
print(f"Captions file : {CAPTION_FILE}")
# coco-t2i-downloader

Downloads MS-COCO 2017 Train and Val images and captions directly from cocodataset.org for Text-to-Image retrieval evaluation. Saves all images to disk and exports a clean JSON file containing image filenames and captions ready for embedding extraction.

## Dataset

MS-COCO 2017 contains 123,287 images (118,287 train + 5,000 val) each annotated with 5 human-written captions, giving 616,435 text queries in total. Images cover complex everyday scenes with multiple objects across 80 categories.

## Usage

```bash
python download_coco.py
```

No additional dependencies required beyond the Python standard library. Requires approximately 19GB of disk space. Zip files are automatically deleted after extraction.

## Output

```
coco/
    images/
        train2017/   ← 118,287 images
        val2017/     ←   5,000 images
    annotations/
        captions_train2017.json
        captions_val2017.json
    captions.json    ← clean combined image and caption index
```

The captions.json file has two fields:

```json
{
    "images" : [{"img_id": "57870", "filename": "000000057870.jpg"}, ...],
    "queries": [{"img_id": "57870", "caption": "A restaurant with wooden tables"}, ...]
}
```

All 123,287 images form the retrieval gallery and all 616,435 captions serve as text queries for Recall@1 and Recall@5 evaluation.

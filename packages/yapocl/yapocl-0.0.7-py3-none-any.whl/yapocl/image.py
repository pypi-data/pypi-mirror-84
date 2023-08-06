import io
import os
import shutil
import requests
from PIL import Image
from tqdm.auto import tqdm
from joblib import Parallel, delayed

def _create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def _remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)

def _remove_file(file):
    if os.path.exists(file):
        os.remove(file)

def _media_id(ad_media_id):
    for _ in range(10-len(str(ad_media_id))):
        ad_media_id = '0'+str(ad_media_id)
    return ad_media_id

def get_image_url(ad_media_id, image_host="https://img.yapo.cl"):
    ad_media_id = _media_id(ad_media_id)
    return '{}/images/{}/{}.jpg'.format(image_host, str(ad_media_id)[:2], ad_media_id)

def get_yams_url(ad_media_id, yams_host="https://images.yapo.cl/api/v1/pro/images"):
    ad_media_id = _media_id(ad_media_id)
    return '{}/{}.jpg?rule=images'.format(yams_host, ad_media_id)

def download(ad_media_id, folder=".", source="yapo"):
    _create_folder(folder)
    file_path = "{}/{}.jpg".format(folder, ad_media_id)
    if source == "yapo":
        url = get_image_url(ad_media_id)
    elif source == "yams":
        url = get_yams_url(ad_media_id)
    try:
        response = requests.get(url, stream=True, timeout=10.0, allow_redirects=True)
        with Image.open(io.BytesIO(response.content)) as im:
            with open(file_path, 'wb') as out_file:
                im.save(out_file)
        return file_path
    except Exception:
        return None

def download_images(ad_media_ids=[], folder=".", source="yapo"):
    results = []
    with Parallel(n_jobs=os.cpu_count()) as parallel:
        batch_results = parallel(
            delayed(download)(ad_media_id, folder, source) for ad_media_id in tqdm(ad_media_ids)
        )
        for result in batch_results:
            results.append(result)
    return results
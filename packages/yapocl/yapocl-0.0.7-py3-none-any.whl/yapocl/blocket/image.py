import os
import shutil
import requests
from tqdm.auto import tqdm
from joblib import Parallel, delayed

class Image(object):
    def __init__(self, image_host="https://img.yapo.cl", yams_host="https://images.yapo.cl/api/v1/pro/images"):
        self.image_host = image_host
        self.yams_host = yams_host

    def _create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def _remove_folder(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    
    def _remove_file(self, file):
        if os.path.exists(file):
            os.remove(file)

    def _media_id(self, ad_media_id):
        for _ in range(10-len(str(ad_media_id))):
            ad_media_id = '0'+str(ad_media_id)
        return ad_media_id

    def get_image_url(self, ad_media_id):
        ad_media_id = self._media_id(ad_media_id)
        return '{}/images/{}/{}.jpg'.format(self.image_host, str(ad_media_id)[:2], ad_media_id)
    
    def get_yams_url(self, ad_media_id):
        ad_media_id = self._media_id(ad_media_id)
        return '{}/{}.jpg?rule=images'.format(self.yams_host, ad_media_id)

    def download(self, ad_media_id, folder=".", source="yapo"):
        self._create_folder(folder)
        if source == "yapo":
            url = self.get_image_url(ad_media_id)
        elif source == "yams":
            url = self.get_yams_url(ad_media_id)
        try:
            response = requests.get(url, stream=True, timeout=1.0, allow_redirects=True)
            file_path = "{}/{}.jpg".format(folder, ad_media_id)
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                del response
                return file_path
        except Exception:
            return None
    
    def download_images(self, ad_media_ids=[], folder=".", workers=1, source="yapo"):
        results = []
        with Parallel(n_jobs=workers) as parallel:
            batch_results = parallel(
                delayed(self.download)(ad_media_id, folder, source) for ad_media_id in tqdm(ad_media_ids)
            )
            for result in batch_results:
                results.append(result)
        return results
import io

from PIL import Image
import requests


class ImageHelper:
    @staticmethod
    def imgurl2pillow(url) -> Image:
        return Image.open(io.BytesIO(requests.get(url).content))

    @classmethod
    def imgurl2file(cls, url, path):
        return cls.imgurl2pillow(url).save(path)

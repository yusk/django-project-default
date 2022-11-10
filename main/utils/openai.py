import os

import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIImageHelper:
    """
    https://openai.com/dall-e-2/
    https://beta.openai.com/docs/guides/images
    """
    @staticmethod
    def gen_img(prompt: str, size="1024x1024", n=1):
        res = openai.Image.create(prompt=prompt, size=size, n=n)
        urls = [d['url'] for d in res['data']]
        return urls

    @staticmethod
    def edit_img(image: bytes,
                 mask: bytes,
                 prompt: str,
                 size="1024x1024",
                 n=1):
        res = openai.Image.create_edit(image=image,
                                       mask=mask,
                                       prompt=prompt,
                                       size=size,
                                       n=n)
        urls = [d['url'] for d in res['data']]
        return urls

    @staticmethod
    def variate_img(image: bytes, size="1024x1024", n=1):
        res = openai.Image.create_variation(image=image, size=size, n=n)
        urls = [d['url'] for d in res['data']]
        return urls

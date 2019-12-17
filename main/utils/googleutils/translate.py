import requests

from google.cloud import translate as google_translate


def translate(text, source='ja', target='en', method="gas"):
    if method == "gas":
        return translate_with_gas(text=text, source=source, target=target)

    translate_client = google_translate.Client()

    translation = translate_client.translate(text, target_language=target)

    return translation['translatedText']


def translate_with_gas(text, source='ja', target='en'):
    url = "https://script.google.com/macros/s/AKfycbweJFfBqKUs5gGNnkV2xwTZtZPptI6ebEhcCU2_JvOmHwM2TCk/exec"
    res = requests.get(
        url, params={
            "text": text,
            "source": source,
            "target": target,
        })

    res.raise_for_status()
    return res.text

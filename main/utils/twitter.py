from requests_oauthlib import OAuth1Session

from django.conf import settings

twitter = OAuth1Session(
    settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)


def tweet(text, reply_to=None, data={}):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {"status": text, "in_reply_to_status_id": reply_to}
    params.update(data)

    res = twitter.post(url, params=params)
    res.raise_for_status()

    return res.json()

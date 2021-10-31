from requests_oauthlib import OAuth1Session

from main.env import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

twitter = OAuth1Session(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)


def tweet(text, reply_to=None, data={}):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {"status": text, "in_reply_to_status_id": reply_to}
    params.update(data)

    res = twitter.post(url, params=params)
    res.raise_for_status()

    return res.json()

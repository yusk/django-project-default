import slackweb

from main.env import SLACK_WEBHOOK_URL

slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)


def slack_notify(text):
    try:
        slack.notify(text=text)
    except Exception as e:
        print(e)

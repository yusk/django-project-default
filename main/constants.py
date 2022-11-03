from .env import SERVICE_NAME

DIGIT_AUTH_EXPIRED_MINUTES = 10

EMAIL_LIMIT_MINUTES = 1
EMAIL_LIMIT_MESSAGE = "メールは短時間に連続して送ることができません。お手数ですが時間を空けてからお試しください。"

LOGIN_INVALID_MINUTES = 5
LOGIN_INVALID_COUNT = 5
LOGIN_INVALID_MESSAGE = "短時間にログインの失敗が多数ありました。一時的にログインを制限しています。お手数ですが時間を空けて再度お試しください。"

CONFIRM_EMAIL_SUBJECT = "{name} メールアドレス認証コード"
CONFIRM_EMAIL_CONTENT = """{name} カスタマーサポートです。
この度は、「{name}」へのご登録、誠にありがとうございます。
確認コードは以下のとおりです。
{code}
アプリから確認コードを入力して登録を完了させてください。
"""

PASSWORD_RESET_EMAIL_SUBJECT = "{name} パスワードリセット認証コード"
PASSWORD_RESET_EMAIL_CONTENT = """{name} カスタマーサポートです。
「{name}」のパスワードリセットを受け付けました。
確認コードは以下のとおりです。
{code}
アプリから確認コードを入力して、パスワード変更を完了させてください。
"""


class ConstantProvider:
    @staticmethod
    def confirm_email_subject(name=SERVICE_NAME, **kwargs):
        return CONFIRM_EMAIL_SUBJECT.format(name=name)

    @staticmethod
    def confirm_email_content(code, name=SERVICE_NAME, **kwargs):
        return CONFIRM_EMAIL_CONTENT.format(code=code, name=name)

    @staticmethod
    def password_reset_email_subject(name=SERVICE_NAME, **kwargs):
        return PASSWORD_RESET_EMAIL_SUBJECT.format(name=name)

    @staticmethod
    def password_reset_email_content(code, name=SERVICE_NAME, **kwargs):
        return PASSWORD_RESET_EMAIL_CONTENT.format(code=code, name=name)

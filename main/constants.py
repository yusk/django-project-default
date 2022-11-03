from .env import SERVICE_NAME

DIGIT_AUTH_EXPIRED_MINUTES = 10

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

IV_IN_REVIEW_MESSAGE = "現在支払い先情報を確認中です。お手数ですが数営業日お待ちください。"
IV_VERIFIED_MESSAGE = "本人確認が完了しました。"
IV_DENIED_MESSAGE = "本人確認が完了できませんでした。もう一度正しい書類を提出してください。"
TO_DEPOSITED_MESSAGE = "出金依頼が正常に受理されました。銀行口座に指定額出金されました。"
TO_CANCELED_MESSAGE = "出金依頼が受理されませんでした。口座情報などをご確認いただくか、運営にお問合せください。"


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

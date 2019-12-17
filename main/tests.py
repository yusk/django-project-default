from django.test import TestCase

from main.utils import tokenize


class UtilsMecabTests(TestCase):
    def test_tokenize(self):
        tokens = tokenize("これはmecabのテストです。")
        answers = ['これ', 'は', 'mecab', 'の', 'テスト', 'です', '。']
        for token, answer in zip(tokens, answers):
            self.assertEqual(token, answer)

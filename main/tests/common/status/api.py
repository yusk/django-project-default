from django.test import TestCase
from django.test.client import RequestFactory

from main.views import StatusView


class StatusViewTest(TestCase):
    def test_get_news(self):
        factory = RequestFactory()
        req = factory.get("/api/status/")
        view = StatusView.as_view()
        res = view(req)

        self.assertEqual(res.status_code, 200)
        data = res.data
        self.assertEqual(data["status"], "ok")

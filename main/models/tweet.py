from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
import os

from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

from config.storage import PrivateMediaStorage

from tag.models import Tag


def storage():
    if not settings.DEBUG:
        return PrivateMediaStorage()
    return None


def validate_empty(value):
    if len(str(value)) == 0:
        raise ValidationError(
            ('空テキストは許可されていません: %(value)s'),
            params={'value': value},
        )


def tweet_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    name = timezone.now().strftime('%Y%m%d%H%M%S%f')
    return f"identity/{name}{ext}"


class Tweet(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 0, '公開'
        DRAFT = 1, '下書き'
        PRIVATE = 2, '非公開'

    user = models.ForeignKey("main.User", on_delete=models.CASCADE)
    text = models.TextField(validators=[validate_empty])
    image = models.ImageField(upload_to=tweet_file_path,
                              storage=storage(),
                              null=True,
                              blank=True)

    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)
    tags = models.ManyToManyField("tag.Tag",
                                  through="TweetTagRelation",
                                  through_fields=("tweet", "tag"),
                                  related_name="tweets",
                                  blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_from_tag(cls, tag):
        return tag.tweet_set.all()

    def status_display(self):
        return self.get_status_display()

    def get_all_tags(self):
        return self.tags.all()

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def get_tag_count(self):
        return Tag.objects.filter(
            tweettagrelation__tweet=self).distinct().count()

    def get_tag_added_at(self):
        latest_tag = Tag.objects.filter(
            tweettagrelation__tweet=self).distinct().annotate(
                tweettagrelation__created_at=Max(
                    'tweettagrelation__created_at')).order_by(
                        "-tweettagrelation__created_at").first()
        if latest_tag is None:
            return None
        return latest_tag.created_at


class TweetTagRelation(models.Model):
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    tag = models.ForeignKey("tag.Tag", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tweet", "tag"],
                                    name="uq_tweet_tag"),
        ]

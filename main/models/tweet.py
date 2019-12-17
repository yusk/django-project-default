from django.db import models
from django.db.models import Max

from .tag import Tag

TWEET_STATUS_CHOICES = ((0, '公開'), (1, '下書き'), (2, '非公開'))


class Tweet(models.Model):
    TWEET_STATUS_CHOICES = TWEET_STATUS_CHOICES

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()

    status = models.IntegerField(choices=TWEET_STATUS_CHOICES, default=0)
    tags = models.ManyToManyField(
        "Tag",
        through="TweetTagRelation",
        through_fields=("tweet", "tag"),
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
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        auto_created = True

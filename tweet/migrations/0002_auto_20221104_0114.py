# Generated by Django 3.1.6 on 2022-11-03 16:14

from django.db import migrations, models
import tweet.models.tweet


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.TextField(validators=[tweet.models.tweet.validate_empty]),
        ),
        migrations.AddConstraint(
            model_name='tweettagrelation',
            constraint=models.UniqueConstraint(fields=('tweet', 'tag'), name='uq_tweet_tag'),
        ),
    ]

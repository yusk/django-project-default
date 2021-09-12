# Generated by Django 3.1.6 on 2021-09-12 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190217_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('status', models.IntegerField(choices=[('0', '公開'), ('1', '下書き'), ('2', '非公開')], default='1')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TweetTagRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tag')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tweet')),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tweets', through='main.TweetTagRelation', to='main.Tag'),
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

from rest_framework import serializers

from tag.models import Tag
from tweet.models import Tweet

from main.utils import with_method_class


class TweetSerializer(serializers.ModelSerializer):
    tags = with_method_class(serializers.CharField)(
        required=False, help_text='e.g. "tag1,tag2"')

    class Meta:
        model = Tweet
        fields = (
            'id',
            'text',
            'status',
            'created_at',
            'tags',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].read_only = True
        self.fields['text'].required = True
        self.fields['text'].allow_blank = False
        self.fields['created_at'].read_only = True

    def create(self, validated_data):
        tags = None
        if 'tags' in validated_data:
            tag_names = validated_data.pop('tags')
            tag_names = [tag_name.strip() for tag_name in tag_names.split(",")]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
        instance = super().create(validated_data)
        if tags:
            instance.tags.add(*tags)
        return instance

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tag_names = validated_data.pop('tags')
            tag_names = [tag_name.strip() for tag_name in tag_names.split(",")]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.add(*tags)
            tags = instance.tags.exclude(name__in=tag_names)
            instance.tags.remove(*tags)
        return super().update(instance, validated_data)

    def get_tags(self, obj):
        return [d.name for d in obj.tags.all()]

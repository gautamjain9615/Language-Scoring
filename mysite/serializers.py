from rest_framework import serializers
from .models import Input

class InputSerializer(serializers.ModelSerializer):
    # link = serializers.URLField(allow_blank=True)
    # json_input = serializers.JSONField(binary=True)
    class Meta:
        model = Input
        fields = (
            # 'link',
            'json_input'
        )


    def create(self, validated_data):
        return Input.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.link = validated_data.get('link', instance.link)
        instance.json_input = validated_data.get(
                                'json_input',instance.json_input)
        instance.save()
        return instance()


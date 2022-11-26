import hashlib
import time

from rest_framework import serializers

from authentication.models import CustomUser
from backend import settings
from .models import Document


class DocumentSelfSerializer(serializers.ModelSerializer):
    shared_with = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        queryset=CustomUser.objects.all()
    )

    class CustomFileField(serializers.FileField):
        def to_representation(self, value):
            unix_timestamp_now = str(int(time.time()))
            payload = value.url + unix_timestamp_now + settings.SECRET_KEY
            suffix = f'?url={value.url}&s={unix_timestamp_now}0x{hashlib.sha256(payload.encode()).hexdigest()}'
            request = self.context.get('request', None)
            return request.build_absolute_uri(f"/documents/media/{suffix}")

    document = CustomFileField(max_length=200)

    class Meta:
        model = Document
        fields = "__all__"

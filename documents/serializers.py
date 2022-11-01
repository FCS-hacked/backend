from rest_framework import serializers

from authentication.models import CustomUser
from .models import Document


class DocumentSelfSerializer(serializers.ModelSerializer):
    shared_with = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Document
        fields = "__all__"

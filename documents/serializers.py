from rest_framework import serializers

from .models import Document


class DocumentSelfSerializer(serializers.ModelSerializer):
    shared_with = serializers.SlugRelatedField(
        many=True,
        slug_field='email'
    )

    class Meta:
        model = Document
        fields = "__all__"

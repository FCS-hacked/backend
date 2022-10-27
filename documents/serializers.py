from rest_framework import serializers

from .models import Document


class DocumentSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"



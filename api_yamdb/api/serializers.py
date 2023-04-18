from rest_framework import serializers

from reviews.models import Title


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description')

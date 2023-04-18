from rest_framework import serializers

from reviews.models import Comment, Review, Title

class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
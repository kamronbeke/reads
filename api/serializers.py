from rest_framework import serializers

from books.models import BookReview
from users.models import CustomUser


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['id', 'stars', 'comment', 'book', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class BookReviewDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()
    user = UserSerializer()

    class Meta:
        model = BookReview
        fields = ['id', 'stars', 'comment', 'book', 'user']
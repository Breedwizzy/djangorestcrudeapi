from rest_framework import serializers
from .models import Post
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # created_by = serializers.ReadOnlyField(source='created_by.username')
    author = serializers.ReadOnlyField(source='author.username')

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "content", 'image', "created_at", "likes", "comments",

        ]

    def get_likes(self, obj):
        return obj.likes.count()

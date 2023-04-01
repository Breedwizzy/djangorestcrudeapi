from rest_framework import serializers
from .models import Post
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.StringRelatedField(source='author.username')

    comments = CommentSerializer(many=True)
    # read_only=True this wis deleted here

    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "content", 'image', "created_at", "likes", "comments",

        ]

    def get_likes(self, obj):
        return obj.likes.count()

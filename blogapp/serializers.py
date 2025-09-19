from rest_framework import serializers
from .models import BlogPost,Comment
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta: 
        model = Comment 
        fields = ['id', 'post', 'author', 'content', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer): 
    comments = CommentSerializer(many=True, read_only=True) 
    author = serializers.ReadOnlyField(source='author.username')
    can_edit = serializers.SerializerMethodField()

    class Meta: 
        model = BlogPost 
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments', 'can_edit']

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.is_staff or obj.author_id == request.user.id



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
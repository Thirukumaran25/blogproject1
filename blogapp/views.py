from rest_framework import viewsets, generics, permissions
from .models import BlogPost, Comment 
from .serializers import UserSerializer, BlogPostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedAndCreate, IsAdminOrOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        print("Current user:", request.user)
        queryset = self.get_queryset()
        print("BlogPost count:", queryset.count())
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndCreate, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(BlogPost, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(BlogPost, pk=post_id)
        return Comment.objects.filter(post=post).order_by('-created_at')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

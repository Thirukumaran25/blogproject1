from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BlogPostViewSet, CommentViewSet, RegisterView


router = DefaultRouter()
router.register(r'blog_posts', BlogPostViewSet, basename='blog_posts')

# Expose router URLs directly; the project-level urls.py will include these under the desired prefix
urlpatterns = [
    path('', include(router.urls)),
    # Register endpoint is exposed at project level (/api/register/)
    # Nested comment routes: /blog_posts/<post_pk>/comments/
    path('blog_posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
]
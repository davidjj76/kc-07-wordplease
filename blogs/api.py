from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blogs.models import Post
from blogs.serializers import PostListSerializer, PostCreateSerializer


class PostList(ListCreateAPIView):

    queryset = queryset = Post.objects.select_related('blog__owner').all().order_by('-publish_date')
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        return PostCreateSerializer if self.request.method == 'POST' else self.serializer_class

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)


class PostReply(PostList):

    def perform_create(self, serializer):
        serializer.save(
            blog=self.request.user.blog,
            reply_to=Post.objects.get(pk=self.kwargs.get('pk'))
        )

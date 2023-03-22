from rest_framework import generics, permissions

# from  import permissions?
from post.permissions import IsAuthorOrAdminOrPostOwner, IsAuthorOrAdmin
from . models import Comment
from . import serializers


class CommentCreateView(generics.CreateAPIView):
    #     queryset = Comment.objects.all()

    serializer_class = serializers.CommentsSerializer
    permission_classes = (IsAuthorOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentsSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdminOrPostOwner(),
        return permissions.AllowAny(),




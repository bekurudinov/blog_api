from django.shortcuts import render
from rest_framework import generics, permissions

from like import serializers
from like.models import like
from post.permissions import IsAuthor


# Create your views here.
class likeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.likeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class likeDeleteView(generics.DestroyAPIView):
    queryset = like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)



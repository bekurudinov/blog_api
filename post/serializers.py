from rest_framework import serializers
from comment.serializers import CommentsSerializer
from category.models import Category
from .models import Post, PostImages
from like.serializers import likeSerializer


class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(
        source='owner.username'
    )
    category_name = serializers.ReadOnlyField(
        source='category.name'
    )


    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview', 'owner_username', 'category_name')
    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance, user)
        return repr


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(
        source='owner.username'
    )
    category_name = serializers.ReadOnlyField(
        source='category.name'
    )
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    @staticmethod
    def is_favorite(post, user):
        return user.favorites.filter(post=post).exists()


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comments_count'] = instance.comments.count()
        repr['comments'] = CommentsSerializer(instance=instance.comments.all(), many=True).data
        repr['likes_count'] = instance.likes.count()
        repr['liked_users'] = likeSerializer(instance=instance.likes.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance, user)
            repr['is_favorite'] = self.is_favorite(instance, user)
        return repr





class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Category.objects.all()
    )
    images = PostImagesSerializer(many=True, required=False)


    class Meta:
        model = Post
        fields = ('title', 'body', 'category',
                  'preview', 'images')

    def create(self, validated_data):
        # print(self, '!!!!!!!')
        request = self.context.get('request')
        # print(validated_data, '********************')
        # print(request.FILES.getlist('images'), '!!!!!!!!!!!')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(image=image, post=post)
        return post


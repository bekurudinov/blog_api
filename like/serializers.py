from rest_framework import serializers

from like.models import like, Favorites


class likeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if user.likes.filter(post=post).exists():
            raise serializers.ValidationError('You already liked this post!')
        return attrs

class likedUsers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = like
        fields = ('owner', 'owner_username')

class FavoritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'post')


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        if instance.post.preview:
            preview = instance.post.preview
            repr['post_preview'] = preview.url
        else:
            repr['post_preview'] = None
        return repr




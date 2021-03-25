from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'description', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'description', 'profile_image']
        extra_kwargs = {
            'username': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followings_count = serializers.IntegerField(source='count_followings')
    followers_count = serializers.IntegerField(source='count_followers')
    posts_count = serializers.IntegerField(source='count_posts')

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'description', 'followings_count', 'followers_count', 'posts_count']


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image', 'username']

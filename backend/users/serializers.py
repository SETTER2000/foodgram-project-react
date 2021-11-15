from api.serializers import RecipesMinSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Subscriptions, User


class UserSerializer(serializers.ModelSerializer):
    """Пользовательский сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipesMinSerializer(many=True, read_only=True)
    lookup_field = 'username'

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'recipes',
            'email',
            'is_subscribed',
            'password',
        )

    def get_is_subscribed(self, obj):
        pass

    def to_representation(self, obj):
        rep = super(UserSerializer, self).to_representation(obj)
        rep.pop('password', None)
        return rep

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        del self.fields['password']
        return user


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Мои подписки."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        fields = ('user', 'author')
        model = Subscriptions

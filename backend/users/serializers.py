from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Subscriptions, User
from ..app.serializers import RecipesListSerializer, RecipesMinSerializer


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

    # extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}
    def get_is_subscribed(self, obj):
        print(f'OBJ:::; {obj}')
        print(f'OBJ222:::; {serializers.CurrentUserDefault()}')

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']
        self.fields['confirmation_code'] = serializers.CharField(required=True)
        self.fields['email'] = serializers.EmailField(required=True)

    def validate(self, attrs):
        data = {}
        user = User.objects.get(email=attrs['email'])
        confirmation_code = User.objects.get(
            confirmation_code=attrs['confirmation_code']
        )
        refresh = self.get_token(user)
        if user and confirmation_code:
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            user.confirmation_code = ''
            user.save()
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

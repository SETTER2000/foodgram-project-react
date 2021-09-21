from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Пользовательский сериализатор для модели пользователя."""

    lookup_field = 'username'

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


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

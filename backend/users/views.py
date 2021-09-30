from functools import partial

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS
from .mixin import CreateListModelMixinViewSet, CreateModelMixinViewSet

from .models import User
from .permissions import PermissonForRole
from .serializers import UserSerializer


class UserModelViewSet(CreateListModelMixinViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['PATCH', 'GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False,
        url_path='me',
    )
    def user_me(self, request) -> Response:
        """Пользовательский URL-адрес для редактирования своего профиля."""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            data = serializer.data
            del data['password']
            return Response(data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def email_auth(request):
    """Проверьте электронную почту и отправьте ей код подтверждения для
     авторизации токена."""
    user = get_object_or_404(User, email=request.data['email'])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Код для генерации токена аутентификации',
        message=str(confirmation_code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(request.data['email'],),
    )
    return Response(
        data='Письмо с кодом для аутентификации',
        status=status.HTTP_201_CREATED,
    )

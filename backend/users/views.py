from functools import partial

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.crypto import get_random_string
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS
from .mixin import CreateListModelMixinViewSet, CreateModelMixinViewSet
from rest_framework.exceptions import ParseError
from .models import User
from .permissions import PermissonForRole, AllowPostAnyReadAuthenticatedUser, \
    IsAuthorOrReadOnly
from .serializers import UserSerializer


class UserModelViewSet(CreateListModelMixinViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (PermissonForRole,)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return User.objects.all()
    #     return User.objects.filter(username=user.username)
    #
    # def get_object(self):
    #     obj = get_object_or_404(User.objects.filter(id=self.kwargs["pk"]))
    #     self.check_object_permissions(self.request, obj)
    #     return obj
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = (DjangoFilterBackend,)

    # def get_queryset(self):
    #     user = self.request.user
    #     return user.accounts.all()

    def perform_create(self, serializer):
        serializer.save()

    # def get_queryset(self):
    #     return User.objects.filter(id=self.request.user.id)

    # permission_classes = (permissions.IsAuthenticated,)
    # def get_queryset(self):
    # User.query_get(pk=self.kwargs["id"])
    # user = User.objects.get(pk=self.request['pk'])
    # if user is None:
    #     raise ParseError("Неверный запрос!")

    # permission_classes = (
    #     partial(PermissonForRole, ROLES_PERMISSIONS.get('Users')),
    # )

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

        # return User.objects.filter(pk=self.kwargs["id"])


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

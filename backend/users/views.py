from functools import partial

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from backend.app.models import Recipes
from backend.app.pagination import PaginationNull
from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS

from .mixin import CreateListModelMixinViewSet, CreateModelMixinViewSet
from .models import User, Subscriptions
from .permissions import PermissonForRole
from .serializers import UserSerializer, SubscriptionsSerializer


class SubscriptionsModelViewSet(viewsets.ModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # pagination_class = PaginationNull

    # permission_classes = (
    #     (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
    #     | partial(PermissonForRole, ROLES_PERMISSIONS.get("Reviews")),
    # )

    def get_queryset(self):
        """Добавит рецепт в избранное."""
        user = get_object_or_404(User, email=self.request.user)
        if 'id' in self.kwargs:
            author = get_object_or_404(User, id=self.kwargs['id'])
            subscription = User.objects.filter(
                subscriptions__in=[user.id])
            if len(subscription) > 0 and subscription[0].email == author.email:
                raise ParseError("Вы уже подписаны на этого пользователя.")
            if self.request.user.id == author.id:
                raise ParseError("Вы не можете подписаться на себя.")
            user.is_subscribed.add(author)
            user.save()
        return self.queryset.filter(
            id__in=[x.id for x in user.is_subscribed.all()])
        #
        # authors = Subscriptions.objects.filter(
        #     user_id=self.request.user).values_list(
        #     'author_id', flat=True)
        #
        #
        # queryset = User.objects.filter(id__in=authors)
        # queryset = Subscriptions.objects.filter(user_id=self.request.user)
        #
        # return queryset
        #
        # if user is None:
        #     raise ParseError("Неверный запрос!")
        #     subscribers = user.is_subscribed.all()
        #     return self.queryset

    def delete(self, request, id=None):
        """Удалить рецепт из избранного."""
        user = User.objects.get(email=request.user)
        author = get_object_or_404(User, id=self.kwargs["id"])
        print(f'user: {user}')
        print(f'author: {author}')
        # print(f'self.request.user.id: {self.request.user.id}')
        # print(f'author.id: {author.id}')
        user.is_subscribed.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_queryset(self):
    #     """Мои подписки. На кого подписан текущий пользователь."""
    #     if 'id' in self.kwargs:
    #         print(f"PPP: {self.kwargs['id']}")
    #         pass
    #     # recipe = Recipes.objects.get(pk=self.kwargs["id"])
    #     authors = Subscriptions.objects.filter(
    #         user_id=self.request.user).values_list(
    #         'author_id', flat=True)
    #     print(f'authorsauthorsauthors:: {authors}')
    #
    #     queryset = User.objects.filter(id__in=authors)
    #     print(f'querysetfff:: {queryset}')
    #     queryset = Subscriptions.objects.filter(user_id=self.request.user)
    #     # queryset = Recipes.objects.filter(author__in=authors)
    #     return queryset
    #     # post_list = pagination_page(self.request, Recipes.objects.filter(
    #     #     author__in=email))
    #     # print(f'post_listpost_list:::: {post_list}')
    #     #
    #     # return render(self.request, 'follow.html',
    #     #               {'page': post_list, 'follow': True})
    #
    #     if user is None:
    #         raise ParseError("Неверный запрос!")
    #         subscribers = user.is_subscribed.all()
    #         return self.queryset

    # def delete(self, request, id=None):
    #     """Отписаться от автора."""
    #     serializer = get_object_or_404(Subscriptions, author_id=self.kwargs.get(
    #         "id"))
    #     serializer.delete()


# def delete(self, request, id=None):
#     """Удалить рецепт из избранного."""
#     recipe = Recipes.objects.get(pk=self.kwargs["id"])
#     user = User.objects.get(email=self.request.user)
#     recipe.is_favorited.remove(user)
#     return Response(status=status.HTTP_204_NO_CONTENT)


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

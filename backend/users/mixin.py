from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateListModelMixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pass


class CreateModelMixinViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    pass

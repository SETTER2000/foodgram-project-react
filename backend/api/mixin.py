from rest_framework import mixins, viewsets


class UpdateDeleteViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class BaseViewSetHelper:
    def nested_paginated_data(self, queryset, main_key):
        """
        This is for cases where we had to place the result array inside a key
        but still keep pagination features.
        :param queryset:
        :param main_key:
        :return:
        """
        start, count = self.get_pagination_params()
        queryset = self.filter_queryset(self.get_queryset())
        total = len(queryset)
        queryset = queryset[start: start + count]
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': total,
            main_key: serializer.data,
        }
        return data


class BaseModelViewSet(viewsets.ModelViewSet, BaseViewSetHelper):
    filterset_fields = ['id']
    filter_backends = [DjangoFilterBackend, ]
    ordering_fields = ['id', 'date_created', 'date_updated']

    def perform_create(self, serializer, **kwargs):
        return serializer.save(**kwargs)


class BaseUserModelViewSet(BaseModelViewSet):
    """
    This class is used for requests that limits its results to the request user
    """
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer, **kwargs):
        super().perform_create(serializer, user=self.request.user, **kwargs)


class BaseOneToOneViewSet(BaseModelViewSet):
    """
    This class is intended for all modelviewsets where the model has
    one to one relationship with user model
    """
    def get_object(self):
        self.kwargs['pk'] = self.request.user.id
        return super().get_object()

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user)

    def perform_create(self, serializer, **kwargs):
        super().perform_create(serializer, id=self.request.user)

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

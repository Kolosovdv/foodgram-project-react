from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from logic.paginations import CustomPageNumberPaginator
from logic.permissions import AuthorOrAdminOrRead

from .models import Subscription, User
from .serializers import (CustomUserSerializer, SubscriptionGetSerializer,
                          SubscriptionPostSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPaginator
    permission_classes = (AuthorOrAdminOrRead, )

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        """Статус подписки."""
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionGetSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        if request.method == 'DELETE':
            subscription = get_object_or_404(
                                            Subscription,
                                            user=user,
                                            author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {'author': author.id, 'user': user.id}
        serializer = SubscriptionPostSerializer(
                                        data=data,
                                        context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

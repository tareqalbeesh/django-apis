from typing import Any
from django.shortcuts import render
from . import serializers
from . import models
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import MenuItemViewPermission, ManagerViewPermission, DeliveryCrewViewPermission, SingleOrderViewPermission, IsDriver, IsManager, IsOnlyUser
from rest_framework.decorators import api_view
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from . import throttles
import datetime
# Create your views here.


class MenuItemView(ListCreateAPIView):
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
    permission_classes = [MenuItemViewPermission]


class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
    permission_classes = [MenuItemViewPermission]


class ManagerView(ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = Group.objects.get(name='Manager').user_set.all()

    def create(self, request: HttpRequest, *args, **kwargs):
        username = request.data['username']
        user = User.objects.get(username=username)
        manager_group = Group.objects.get(name='Manager')
        user.groups.add(manager_group)
        return Response(status=status.HTTP_200_OK)
    permission_classes = [ManagerViewPermission]
    throttle_classes = [throttles.TenCallsPerMinute]


class SingleManagerView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    queryset = Group.objects.get(name='Manager').user_set.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        manager_group = Group.objects.get(name='Manager')
        instance.groups.remove(manager_group)
        return Response(status=status.HTTP_200_OK)
    permission_classes = [ManagerViewPermission]
    throttle_classes = [throttles.TenCallsPerMinute]


class DeliveryCrewView(ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = Group.objects.get(name='Delivery crew').user_set.all()

    def create(self, request: HttpRequest, *args, **kwargs):
        username = request.data['username']
        user = User.objects.get(username=username)
        manager_group = Group.objects.get(name='Delivery crew')
        user.groups.add(manager_group)
        return Response(status=status.HTTP_200_OK)
    permission_classes = [DeliveryCrewViewPermission]
    throttle_classes = [throttles.TenCallsPerMinute]
    throttle_classes = [throttles.TenCallsPerMinute]


class SingleDeliveryCrewView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    queryset = Group.objects.get(name='Delivery crew').user_set.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        manager_group = Group.objects.get(name='Delivery crew')
        instance.groups.remove(manager_group)
        return Response(status=status.HTTP_200_OK)
    permission_classes = [DeliveryCrewViewPermission]
    throttle_classes = [throttles.TenCallsPerMinute]


class CartView(ListCreateAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(user__id=self.request.user.id).all()

    def delete(self, request, *args, **kwargs):
        data = models.Cart.objects.filter(user_id=request.user.id).all()
        data .delete()

        return Response({'details': 'deleted!'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttles.TenCallsPerMinute]


class OrderView(ListCreateAPIView):
    serializer_class = serializers.OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        permissions = []
        if self.request.method == 'POST':
            permissions = [IsAuthenticated, IsOnlyUser]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Manager').exists():
            return models.Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew'):
            return models.Order.objects.filter(delivery_crew__id=self.request.user.id).all()
        else:
            return models.Order.objects.filter(user__id=self.request.user.id).all()

    throttle_classes = [throttles.TenCallsPerMinute]


class SingleOrderView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Manager').exists():
            return models.Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew'):
            return models.Order.objects.filter(delivery_crew__id=self.request.user.id).all()
        else:
            return models.Order.objects.filter(user__id=self.request.user.id).all()

    def get_permissions(self):
        permissions = []
        if self.request.method == 'PUT':
            permissions = [IsAuthenticated, not IsDriver,
                           not IsManager, not IsAdminUser]
        elif self.request.method == 'PATCH':
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    permission_classes = [SingleOrderViewPermission]
    throttle_classes = [throttles.TenCallsPerMinute]

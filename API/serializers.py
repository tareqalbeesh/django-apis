from rest_framework import serializers
from . import models
from django.contrib.auth.models import User, Group
import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['slug', 'title', 'id']
        model = models.Category


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ['id', 'title', 'price',
                  'featured', 'category', 'category_id']
        model = models.MenuItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'id', 'email']
        model = User


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    # user_id = serializers.IntegerField(write_only=True)
    menuitem_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        self.user = self.context['request'].user

    class Meta:
        fields = ['menuitem', 'menuitem_id', 'user',
                  'quantity', 'unit_price',
                  'menuitem_price']
        model = models.Cart

    def create(self, validated_data):
        menuitem = models.MenuItem.objects.get(
            pk=validated_data['menuitem_id'])
        user = User.objects.get(pk=self.user.id)
        res_price = menuitem.price * \
            validated_data['quantity']

        cart = models.Cart(menuitem=menuitem,
                           user=user, quantity=validated_data['quantity'], unit_price=menuitem.price, price=res_price)
        cart.save()
        return cart


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Order

        fields = ['user', 'delivery_crew', 'status', 'total', 'date']
        # depth = 1

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        cart_items = models.Cart.objects.filter(
            user__id=user_id)

        total_cost = 0

        for item in cart_items:
            total_cost += item.price
        order = models.Order(user=models.User.objects.get(id=user_id), delivery_crew=models.User.objects.get(
            id=self.context['request'].data['delivery_crew']), status=False, total=total_cost, date=datetime.datetime.now())
        order.save()
        for item in cart_items:
            temp_order_item = models.OrderItem(
                order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)
            temp_order_item.save()
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    menuitem = MenuItemSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']

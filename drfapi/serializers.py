import datetime
import re

import phonenumbers
from phonenumbers import NumberParseException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from drfapi.models import Customer, Product, Order, OrderItem


class CustomerModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[
        UniqueValidator(queryset=Customer.objects.all(), message='Record with such customer name is already exists.')])
    contact_number = serializers.CharField(max_length=10, help_text='7296909051',
                                           validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                                       message='Record with such contact number is already exists.')])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                               message='Record with such email is already exists.')])

    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_number', 'email', 'created_at')

    def validate_email(self, email):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, email):
            raise serializers.ValidationError("Given email is not a valid email address.")
        return email

    def validate_contact_number(self, contact_number):
        if contact_number and len(contact_number) == 10:
            try:
                phone_number = phonenumbers.parse("+91" + contact_number)
                is_valid_number: bool = phonenumbers.is_valid_number(phone_number)
                if not is_valid_number:
                    raise serializers.ValidationError("Given contact number is not a valid number.")
            except NumberParseException as e:
                raise serializers.ValidationError("Given contact number is not a valid number.")
        else:
            raise serializers.ValidationError(
                "Contact number should be a 10-digit number without any spaces or special characters.")
        return contact_number


class ProductModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, validators=[
        UniqueValidator(queryset=Customer.objects.all(), message='Record with such product name is already exists.')])
    weight = serializers.DecimalField(decimal_places=2, max_digits=4, help_text='25')

    class Meta:
        model = Product
        fields = ('id', 'name', 'weight', 'created_at')

    def validate_weight(self, weight):
        if weight and weight < 0:
            raise serializers.ValidationError("Given weight cannot be negative.")
        elif weight > 25:
            raise serializers.ValidationError("Given weight cannot be more than 25 kg.")
        return weight


class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity',)

    def validate_quantity(self, quantity):
        if quantity > 10:
            raise serializers.ValidationError("Quantity cannot be more than 10.")
        return quantity


class OrderModelSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, required=True)
    order_date = serializers.DateField(input_formats=["%d/%m/%Y"], format='%d/%m/%Y', help_text='31/12/2023',
                                       default=datetime.date.today())

    class Meta:
        model = Order
        fields = ('customer', 'order_date', 'address', 'order_item',)

    def validate_order_date(self, order_date):
        if order_date and order_date < datetime.date.today():
            raise serializers.ValidationError("order date cannot be in past.")
        return order_date

    def validate(self, attrs):
        order_items = attrs.get('order_item')
        sum_of_weight = sum(x.get('product').weight for x in order_items)
        if sum_of_weight > 150:
            serializers.ValidationError("order cumulative weight cannot be more than 150kg.")
        return attrs

    def create(self, validated_data):
        copied_validated_data = validated_data.copy()
        order_items = validated_data.pop('order_item')
        order = Order(**validated_data)
        order.save()

        order_item_list = []
        for order_item in order_items:
            order_item_list.append(OrderItem(order=order, **order_item))
        OrderItem.objects.bulk_create(order_item_list)
        return copied_validated_data


class ListProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'weight', 'created_at')


class ListOrderItemSerailizer(serializers.ModelSerializer):
    product = ListProductModelSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'created_at')


class ListAllOrderModelSerializer(serializers.ModelSerializer):
    order_items = ListOrderItemSerailizer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'customer', 'order_date', 'address', 'order_items', 'created_at')

from rest_framework import serializers

from .models import Users, Items, Payment, UserItem


class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'contact_no', 'passwords', 'enrollment_no')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserItem
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

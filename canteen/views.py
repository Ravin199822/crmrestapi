# Create your views here.
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Users, Items, UserItem, Payment
from .serializers import ItemSerializer, PaymentSerializer


class SignupUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignupUserSerializer
    queryset = Users.objects.all()


class LoginwithPassword(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        contact_no = request.data.get('contact_no', None)
        password = request.data.get('passwords', None)
        if not contact_no:
            return Response({"error": "Please Enter your Contact no"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not password:
            return Response({"error": "please Enter Password"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = None
        if contact_no:
            user = Users.objects.filter(contact_no=contact_no).first()
            if user:
                if password == user.passwords:
                    user_serializer1 = serializers.LoginSerializer(user, many=False)
                    return Response({"user": user_serializer1.data},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Given credentials are not valid"},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({"error": "user does not exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ItemList(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Items.objects.all()
    serializer_class = ItemSerializer


class ItemListView(APIView):
    permission_classes = [AllowAny]
    queryset = Items.objects.all()
    serializer_class = serializers.ItemSerializer

    def get(self, request):
        category = request.data.get('option', None)
        if not category:
            return Response({"error": "please Choose option for meal"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            items = Items.objects.filter(category=category)
            item_serializer = serializers.ItemSerializer(items, many=True)
            return Response({"items": item_serializer.data}, status=status.HTTP_200_OK)

class CartView(APIView):
    permission_classes = [AllowAny]
    queryset = UserItem.objects.all()
    serializer_class = serializers.CartSerializer

    def post(self, request):
        user_id = request.data.get("user_id", None)
        item_id = request.data.get("item_id", None)
        user = Users.objects.filter(pk=user_id)
        items = []
        if item_id:
            items_id = item_id.split(",")
            for i in items_id:
                item = Items.objects.filter(pk=i)
                items.append(item)
        total_price = 0
        price = 0
        if items:
            for i in items:
                total_price = int(i[0].price) + total_price
                if not UserItem.objects.filter(user=user[0], items=i[0], toal_amount=total_price):
                    user_item = UserItem.objects.create(user=user[0], items=i[0], toal_amount=total_price)
                    serializer = serializers.CartSerializer(user_item, data=request.data)
                else:
                    user_item = UserItem.objects.filter(user=user[0], items=i[0], toal_amount=total_price)
                    price = int(user_item[0].items.price) + int(price)
                    serializer = serializers.ItemSerializer(user_item[0].items, data=request.data)
            return Response({"cart_value": serializer.initial_data, "payment": total_price}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Your cart is empty"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PaymentView(APIView):
    permission_classes = [AllowAny]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request):
        user_id = request.data.get("user_id", None)
        user = Users.objects.filter(pk=user_id)
        user_items = UserItem.objects.filter(user=user[0])
        if user_items:
            for i in user_items:
                payment = Payment.objects.create(user_items=i, payment_status=True, order_status="unserved")
                serializer = PaymentSerializer(payment, data=request.data)
            return Response({"payment": serializer.initial_data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Your cart is empty"})


class OrdersView(APIView):
    permission_classes = [AllowAny]
    queryset = UserItem.objects.all()
    serializers = serializers.UserItem

    def get(self, request):
        user_id = request.data.get("user_id", None)
        user = Users.objects.filter(pk=user_id)
        user_items = UserItem.objects.filter(user=user[0])
        item = []
        for items in user_items:
            payment = Payment.objects.filter(user_items=items)
            if payment[0].payment_status and payment[0].order_status == "unserved":
                serializer = ItemSerializer(items.items)
                item.append(serializer.data)
        return Response({"my_orders": item}, status=status.HTTP_200_OK)


class OrderHistoryView(APIView):
    permission_classes = [AllowAny]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request):
        user_id = request.data.get("user_id", None)
        print(user_id)
        user = Users.objects.filter(pk=user_id)
        user_items = UserItem.objects.filter(user=user[0])
        orders = []
        item_list = []
        for item in user_items:
            payment = Payment.objects.filter(user_items=item)
            print(payment)
            serializer = ItemSerializer(item.items)
            item_list.append(serializer.data)
            serializer = PaymentSerializer(payment[0])
            orders.append(serializer.data)
        return Response({"orders": orders, "items": item_list}, status=status.HTTP_200_OK)

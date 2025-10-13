from rest_framework import generics
from kiosco.models import Order
from kiosco.serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



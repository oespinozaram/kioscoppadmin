from rest_framework import serializers
from kiosco.models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

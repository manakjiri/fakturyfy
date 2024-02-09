from datetime import datetime
from rest_framework import serializers
from fakturyfy.app.models import Entity

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__' 


class RequestItem:
    def __init__(self, description: str, quantity: float, price: float, tax: float) -> None:
        self.description = description
        self.quantity = quantity
        self.price = price
        self.tax = tax

class ItemSerializer(serializers.Serializer):
    description = serializers.CharField()
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()

    def create(self, validated_data):
        return RequestItem(**validated_data)


class NewInvoiceRequest:
    def __init__(self, provider_id: int, client_id: int, item_list: list[RequestItem], date: datetime, paydate: datetime, currency: str, save: bool = False) -> None:
        self.provider = Entity.objects.get(pk=provider_id)
        self.client = Entity.objects.get(pk=client_id)
        self.item_list = item_list
        self.date = date
        self.paydate = paydate
        self.currency = currency
        self.save = save
        

class NewInvoiceSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    item_list = serializers.ListField(child=ItemSerializer())
    date = serializers.DateTimeField()
    paydate = serializers.DateTimeField()
    currency = serializers.CharField()
    save = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        validated_data['item_list'] = [ItemSerializer(data=item).create(item) for item in validated_data['item_list']]
        return NewInvoiceRequest(**validated_data)

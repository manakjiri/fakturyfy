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


class GetInvoicesRequest:
    def __init__(self, provider_id: int | None = None, client_id: int | None = None) -> None:
        self.provider_id = provider_id
        self.client_id = client_id

class GetInvoicesSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField(required=False, allow_null=True)
    client_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data: dict):
        assert ('provider_id' in validated_data and validated_data['provider_id'] is not None) \
            or ('client_id' in validated_data and validated_data['client_id'] is not None)
        return GetInvoicesRequest(**validated_data)
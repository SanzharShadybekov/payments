from django.db import IntegrityError
from rest_framework import serializers
from .models import Payment, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('payment', )


class PaymentSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Payment
        fields = ('id', 'user', 'amount', 'status', 'products', 'created_at', 'updated_at')
        read_only_fields = ('id', 'status', 'created_at', 'updated_at')

    def create(self, data):
        products = data.pop('products')
        try:
            payment = Payment.objects.create(**data)
        except IntegrityError:
            raise serializers.ValidationError({'payment_error': 'Invalid payment'})
        answer_objects = [Product(payment=payment, title=item['title'], imei=item['imei'])
                          for item in products]
        Product.objects.bulk_create(answer_objects)
        return payment


class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('status',)

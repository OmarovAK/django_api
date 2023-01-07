from rest_framework.serializers import ModelSerializer

from logistic.models import Product, Stock, StockProduct


class Serializer_Product(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description',
        ]


class Serializer_Stock(ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'id', 'address', 'products',
        ]

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)


class SerializerStockProduct(ModelSerializer):
    class Meta:
        model = StockProduct
        fields = [
            'stock', 'product', 'quantity', 'price'
        ]

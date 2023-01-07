from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock, StockProduct
from logistic.serialisers import Serializer_Product, Serializer_Stock, SerializerStockProduct


class ViewsetProduct(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = Serializer_Product


class ViewsetStock(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = Serializer_Stock


class ViewsetStockProduct(ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = SerializerStockProduct

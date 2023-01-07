from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter


from logistic.views import ViewsetProduct, ViewsetStock, ViewsetStockProduct

app_name = 'base_app'

r = DefaultRouter()

r.register('products', ViewsetProduct)
r.register('stock', ViewsetStock)
r.register('stock_product', ViewsetStockProduct)


urlpatterns = [

] + r.urls

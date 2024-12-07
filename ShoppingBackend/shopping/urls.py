from django.urls import path
from .views import ItemListCreateView, ItemDetailView, CartView

urlpatterns = [
    # Item endpoints
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    # Cart endpoint
    path('cart/', CartView.as_view(), name='cart'),
]

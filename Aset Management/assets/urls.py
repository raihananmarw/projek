from django.urls import path
from .views import asset_list, asset_detail, asset_create, asset_update, asset_delete

urlpatterns = [
    path('', asset_list, name='asset_list'),
    path('<int:pk>/', asset_detail, name='asset_detail'),
    path('create/', asset_create, name='asset_create'),
    path('<int:pk>/update/', asset_update, name='asset_update'),
    path('<int:pk>/delete/', asset_delete, name='asset_delete'),
]
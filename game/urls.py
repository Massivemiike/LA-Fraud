from django.urls import path

from . import views

urlpatterns = [
    path('', views.game_home, name='game_home'),
    path('inventory/', views.inventory, name='inventory'),
    path('shop/', views.shop, name='shop'),
    path('buy-item/<int:item_id>/', views.buy_item, name='buy_item'),
    path('crimes/', views.crimes, name='crimes'),
    path('missions/', views.missions, name='missions'),
    path('gym/', views.gym, name='gym'),
    path('properties/', views.properties, name='properties'),
    path('travel/', views.travel, name='travel'),
    path('gangs/', views.gangs, name='gangs'),
    path('stock-market/', views.stock_market, name='stock_market'),
    path('achievements/', views.achievements, name='achievements'),
]
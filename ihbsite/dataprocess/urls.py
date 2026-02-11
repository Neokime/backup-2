from django.urls import path, include
from . import views

app_name = 'dataprocess'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistics/', views.statistics, name='statistics'),
    path('charts/', views.charts, name='charts'),
    path('map/', views.map_view, name='map'),
    path('wordclouds/', views.wordclouds, name='wordclouds'),
]
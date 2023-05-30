from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calcInput/', views.calcInput, name='calcInput'),
    #path('calcOutput/', views.calcOutput, name='calcOutput'),
]
    
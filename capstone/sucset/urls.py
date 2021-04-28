from django.urls import path
from . import views

app_name = 'sucset'
urlpatterns =[
    path('main', views.main, name='main'),
]

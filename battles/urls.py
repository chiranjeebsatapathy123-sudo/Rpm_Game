from django.urls import path
from . import views

urlpatterns = [
    path('', views.battles_view, name='battles'),
]

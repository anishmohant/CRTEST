from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enlist', views.enlist, name='enlist'),
]
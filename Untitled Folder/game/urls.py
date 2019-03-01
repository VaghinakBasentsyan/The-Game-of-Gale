from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('(?P<factory_id>[0-9a-f-]+)', views.index, name='index'),

]
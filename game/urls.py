from django.urls import path

from . import views

urlpatterns = [
    path('start_new/', views.new_game, name='new_game'),
    path('', views.index, name='index'),

]
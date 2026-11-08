from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.index, name='bases1'),
    path('musico/nuevo/', views.crear_musico, name='crear_musico'),
    path('musico/editar/<int:pk>/', views.editar_musico, name='editar_musico'),
    path('musico/eliminar/<int:pk>/', views.eliminar_musico, name='eliminar_musico'),
    path('genero/nuevo/', views.crear_genero, name='crear_genero'),
    path('genero/editar/<int:pk>/', views.editar_genero, name='editar_genero'),
    path('genero/eliminar/<int:pk>/', views.eliminar_genero, name='eliminar_genero'),
    path('instrumento/nuevo/', views.crear_instrumento, name='crear_instrumento'),
    path('instrumento/editar/<int:pk>/', views.editar_instrumento, name='editar_instrumento'),
    path('instrumento/eliminar/<int:pk>/', views.eliminar_instrumento, name='eliminar_instrumento'),
]
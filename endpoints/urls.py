from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("peliculas/listar", views.obtenerPeliculas),
    path("categorias/listar", views.obtenerCategorias),
    path("categorias/crear", views.registrarCategoria)
]
from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("peliculas/listar", views.obtenerPeliculas),
    path("peliculas/listar_nombre", views.obtenerPeliculas),
    path("categorias/listar", views.obtenerCategorias),
    path("categorias/crear", views.registrarCategoria),
    path("categorias/modificar", views.modificarCategoria),
    path("categorias/eliminar", views.eliminarCategoria),
    path("actores/listar", views.obtenerActores),
]
from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Pelicula)
admin.site.register(models.Categoria)
admin.site.register(models.Actor)
admin.site.register(models.PeliculaXActor)

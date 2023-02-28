from django.contrib import admin
from . import models

class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

class PeliculaXActorAdmin(admin.ModelAdmin):
    list_filter = ['pelicula']
    fieldsets = [
        ("Llaves foraneas", {
            'fields' : ['actor', 'pelicula']
        }),
        ("Atributos", {
            'fields' : ['tiempo', 'sueldo']
        })
    ]
    list_display = ('pk','actor', 'pelicula', 'tiempo', 'sueldo')

# Register your models here.
admin.site.register(models.Pelicula)
admin.site.register(models.Categoria)
admin.site.register(models.Actor, ActorAdmin)
admin.site.register(models.PeliculaXActor, PeliculaXActorAdmin)

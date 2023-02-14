from django.db import models

class Categoria(models.Model):
    CATEGORIA_ESTADOS = (
        ("A", "Activo"),
        ("I", "Inactivo")
    )
    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=CATEGORIA_ESTADOS)

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    nombre = models.CharField(max_length=100)
    url = models.URLField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
class Actor(models.Model):
    ACTOR_ESTADOS = (
        ("A", "Activo"),
        ("R", "Retirado")
    )
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=1, choices=ACTOR_ESTADOS)

    def __str__(self):
        return self.nombre
    
class PeliculaXActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

    tiempo = models.IntegerField(verbose_name="Tiempo en pantalla", default=0)
    sueldo = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.actor.nombre} - {self.pelicula.nombre}"




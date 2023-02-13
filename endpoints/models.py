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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre



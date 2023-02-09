from django.db import models

class Pelicula(models.Model):
    nombre = models.CharField(max_length=100)
    url = models.URLField()
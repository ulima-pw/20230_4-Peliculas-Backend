from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import Actor, Categoria, Pelicula, PeliculaXActor

# /endpoints/login
@csrf_exempt
def login(request):
    if request.method == "POST":
        dictDataRequest = json.loads(request.body)
        usuario = dictDataRequest["usuario"]
        password = dictDataRequest["password"]

        # TODO: Consultar a base de datos
        if usuario == "pw" and password == "123":
            # Correcto
            dictOk = {
                "error": ""
            }
            return HttpResponse(json.dumps(dictOk))
        else:
            # Error login
            dictError = {
                "error": "Error en login"
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


def obtenerPeliculas(request):
    if request.method == "GET":
        idCategoria = request.GET.get("categoria")

        if idCategoria == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

        peliculasFiltradas = []

        if idCategoria == "-1" :
            peliculasQS = Pelicula.objects.all()
        else:
            peliculasQS = Pelicula.objects.filter(categoria__pk=idCategoria)
        
        for p in peliculasQS:
            peliculasFiltradas.append({
                "id" : p.pk,
                "nombre" : p.nombre,
                "url" : p.url,
                "categoria" : {
                    "id" : p.categoria.pk,
                    "nombre" : p.categoria.nombre
                }
            })

        dictResponse = {
            "error": "",
            "peliculas": peliculasFiltradas
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

# /endpoinst/peliculas/listar_nombre?nombre=werwer
def obtenerPeliculasPorNombre(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    nombreAFiltrar = request.GET.get("nombre")

    peliculasQS = Pelicula.objects.filter(nombre__contains=nombreAFiltrar)

    peliculas = []
    for p in peliculasQS:
        peliculas.append({
            "id" : p.id,
            "nombre" : p.nombre
        })

    dictOK = {
        "error" : "",
        "peliculas" : peliculas
    }
    return HttpResponse(json.dumps(dictOK))


def obtenerCategorias(request):
    if request.method == "GET":
        listaCategoriasQuerySet = Categoria.objects.filter(estado="A")
        listaCategorias = []
        for c in listaCategoriasQuerySet:
            listaCategorias.append({
                "id" : c.id,
                "nombre" : c.nombre
            })

        dictOK = {
            "error" : "",
            "categorias" : listaCategorias
        }
        return HttpResponse(json.dumps(dictOK))

    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

"""
Path: /endpoints/categorias/crear POST
Request:
{
    "nombre" : "...",
    "estado" : "A"
}
Response:
{
    "error" : ""
}
"""
@csrf_exempt
def registrarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    dictCategoria = json.loads(request.body)
    nombre = dictCategoria["nombre"]
    estado = dictCategoria["estado"]

    cat = Categoria(nombre=nombre, estado=estado)
    cat.save() # Registra en la bd la nueva categoria

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))

"""
Path: /endpoints/categorias/modificar POST
Request:
{
    "id" : 1,
    "nombre"? : "...",
    "estado"? : "A"
}
Response:
{
    "error" : ""
}
"""
@csrf_exempt
def modificarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictCategoria = json.loads(request.body)

    identificador = dictCategoria["id"]
    cat = Categoria.objects.get(pk=identificador) # Obtenemos cat de bd

    if dictCategoria.get("nombre") != None:
        cat.nombre = dictCategoria.get("nombre")

    if dictCategoria.get("estado") != None:
        cat.estado = dictCategoria.get("estado")

    cat.save() # Se modifica la bd

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))


def eliminarCategoria(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    idCategoria = request.GET.get("id")
    
    if idCategoria == None:
        dictError = {
            "error": "Debe enviar un id de categoria para eliminarla."
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    cat = Categoria.objects.get(pk=idCategoria) # Obtengo categoria de la bd
    cat.delete()  # elimino categoria de la bd

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))

# /endpoints/actores/listar?pelicula=2
def obtenerActores(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    peliculaId = request.GET.get("pelicula")

    actores = []
    if peliculaId == None:
        # Devolver todas los actores
        actoresQS = Actor.objects.all()
        for a in actoresQS:
            actores.append({
                "id" : a.pk,
                "nombre" : a.nombre
            })
    else :
        # Filtrar por id de pelicula
        peliculasxActorQS = PeliculaXActor.objects.filter(pelicula__pk=peliculaId)
        for pa in peliculasxActorQS:
            actores.append({
                "id" : pa.actor.pk,
                "nombre" : pa.actor.nombre
            })

    dictOK = {
        "error" : "",
        "actores" : actores
    }
    return HttpResponse(json.dumps(dictOK))

    
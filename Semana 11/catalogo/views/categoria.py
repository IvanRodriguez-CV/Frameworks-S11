from django.shortcuts import render

from catalogo.models import Categoria


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(
        request,
        "categoria/lista.html",
        {"categorias": categorias},
    )

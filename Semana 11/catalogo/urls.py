from django.urls import path

from .views.categoria import lista_categorias


urlpatterns = [
    path("", lista_categorias, name="inicio"),
    path("categoria/", lista_categorias, name="list_categorias"),
]

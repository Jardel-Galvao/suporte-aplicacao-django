from django.urls import path
from encaminhamentos_incorretos.views import index, adicionar_encaminhamentos, adicionar_encaminhamentos_form, listar_encaminhamentos

urlpatterns = [
    path("", index),
    path("adicionar_encaminhamentos_form/", adicionar_encaminhamentos_form, name="adicionar_encaminhamentos_form"),
    path("adicionar_encaminhamentos/", adicionar_encaminhamentos, name="adicionar_encaminhamentos"),   
    path("listar_encaminhamentos/", listar_encaminhamentos, name="listar_encaminhamentos"),
]
from django.urls import path
from encaminhamentos_incorretos.views import index, adicionar_encaminhamento, adicionar_encaminhamentos

urlpatterns = [
    path("", index),
    path("adicionar_encaminhamentos/", adicionar_encaminhamentos, name="adicionar_encaminhamentos"),
    path("adicionar_encaminhamento/", adicionar_encaminhamento, name="adicionar_encaminhamento"),    
]
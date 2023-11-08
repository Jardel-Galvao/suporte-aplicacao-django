from django.urls import path
from encaminhamentos.views import index, adicionar_encaminhamentos, listar_encaminhamentos, listar_usuarios, dias_atendidos, backup, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index),
    path("adicionar_encaminhamentos/", adicionar_encaminhamentos, name="adicionar_encaminhamentos"),   
    path("listar_encaminhamentos/", listar_encaminhamentos, name="listar_encaminhamentos"),
    path("listar_usuarios/", listar_usuarios, name="listar_usuarios"),
    path("dias_atendidos/", dias_atendidos, name="dias_atendidos"),
    path("backup/", backup, name="backup"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='encaminhamentos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
from django.contrib import admin
from django.urls import include, path
from encaminhamentos_incorretos.urls import urlpatterns as encaminhamentos_incorretos_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(encaminhamentos_incorretos_urls)),
]

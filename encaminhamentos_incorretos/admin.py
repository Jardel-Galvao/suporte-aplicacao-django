from django.contrib import admin
from encaminhamentos_incorretos.models import Encaminhamento, EncaminhamentoIncorreto, IgnorarMes

# Register your models here.
admin.site.register(Encaminhamento)
admin.site.register(EncaminhamentoIncorreto)
admin.site.register(IgnorarMes)

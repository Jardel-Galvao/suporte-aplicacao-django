from django.contrib import admin
from encaminhamentos.models import Encaminhamento, EncaminhamentoIncorreto, DiasAusencia

# Register your models here.
admin.site.register(Encaminhamento)
admin.site.register(EncaminhamentoIncorreto)
admin.site.register(DiasAusencia)

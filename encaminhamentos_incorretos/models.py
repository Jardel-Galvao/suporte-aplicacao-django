from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Encaminhamento(models.Model):
    datahora = models.DateTimeField(blank=False, default=datetime.today())
    link = models.CharField(max_length=256, blank=False)
    tramite = models.IntegerField(null=False)
    analista = models.ForeignKey(User, on_delete=models.CASCADE)
    classificacao = models.CharField(max_length=256, blank=False)
    modulo = models.CharField(max_length=256, blank=False)
    topico = models.CharField(max_length=256, blank=False)

    def __str__(self) -> str:
        return f"{self.link}"

class EncaminhamentoIncorreto(Encaminhamento):
    desc_encaminhamento = models.TextField(max_length=500, blank=False)
    validado = models.BooleanField(null=False, default=False)
    concordancia = models.BooleanField(null=False, default=False)
    analise_analista = models.TextField(max_length=500, blank=True)

    def __str__(self) -> str:
        return f"{self.link}"
    
class IgnorarMes(models.Model):
    analista = models.ForeignKey(User, on_delete=models.CASCADE)
    mes = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f"{self.mes} + {self.analista}"
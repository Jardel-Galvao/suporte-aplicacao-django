from django.shortcuts import render, redirect
from encaminhamentos_incorretos.models import EncaminhamentoIncorreto
import pandas as pd
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.
def index(request):
    pass

def adicionar_encaminhamentos(request):
    analistas = User.objects.all()
    analistas_dict = list(analistas.values())
    context_data = {'analistas': analistas_dict}
    return render (request=request, template_name="encaminhamentos_incorretos/adicionar_encaminhamentos.html", context=context_data)

def adicionar_encaminhamento(request):
    if not request.FILES.get('planilha'):
        try:
            datahora = request.POST.get('datahora')
            link = request.POST.get('link')
            tramite = request.POST.get('tramite')
            analista = User.objects.get(id=request.POST.get('analista')[0])
            classificacao = request.POST.get('classificacao')
            modulo = request.POST.get('modulo')
            topico = request.POST.get('topico')
            desc_encaminhamento = request.POST.get('descricao')
            novo_encaminhamento = EncaminhamentoIncorreto.objects.create(datahora=datahora, 
                                                                        link=link, 
                                                                        tramite=tramite, 
                                                                        analista=analista, 
                                                                        classificacao=classificacao, 
                                                                        modulo=modulo, 
                                                                        topico=topico, 
                                                                        desc_encaminhamento=desc_encaminhamento)
            novo_encaminhamento.save()
        except Exception as e:
            erro = {"erro" : e}
            return render (request=request, template_name="encaminhamentos_incorretos/erro.html", context=erro)
    else:
        try:
            planilha = request.FILES.get('planilha')
            planilha_df = pd.read_excel(planilha)

            validado = True if request.POST.get('validado') == 'on' else 0
            concordancia = True if validado == True else False
            
            instancias_encaminhamentos = []
            for i, encaminhamento in planilha_df.iterrows():
                nome_analista = encaminhamento['Técnico'].split()
                primeiro_nome_analista = nome_analista[0]
                ultimo_nome_analista = ' '.join(nome_analista[1:])
                analista = User.objects.get(first_name=primeiro_nome_analista, last_name=ultimo_nome_analista)
                novo_encaminhamento = EncaminhamentoIncorreto.objects.create(datahora=datetime.strptime(encaminhamento['Data do encaminhamento'], "%d/%m/%Y %H:%M"),
                                                                            link=encaminhamento['Link SS'], 
                                                                            tramite=encaminhamento['Trâmite'], 
                                                                            analista=analista,
                                                                            classificacao=encaminhamento['Classificação'], 
                                                                            modulo=encaminhamento['Módulo'],
                                                                            topico=encaminhamento['Tópico'], 
                                                                            desc_encaminhamento=encaminhamento['Descrição encaminhamento Incorreto'],
                                                                            validado=validado,
                                                                            concordancia=concordancia)
                instancias_encaminhamentos.append(novo_encaminhamento)
            for encaminhamento_instancia in instancias_encaminhamentos:
                encaminhamento_instancia.save()
        except Exception as e:
            erro = {"erro" : e}
            return render (request=request, template_name="encaminhamentos_incorretos/erro.html", context=erro)
    return redirect('/adicionar_encaminhamentos/')

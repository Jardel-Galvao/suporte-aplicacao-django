from django.shortcuts import render, redirect
from encaminhamentos_incorretos.models import EncaminhamentoIncorreto, Encaminhamento
import pandas as pd
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your views here.
def index(request):
    pass

def adicionar_encaminhamentos_form(request):
    analistas = User.objects.all()
    analistas_dict = list(analistas.values())
    context_data = {'analistas': analistas_dict}
    return render (request=request, template_name="encaminhamentos_incorretos/adicionar_encaminhamentos.html", context=context_data)

def adiciona_encaminhamento_incorreto(request, datahora, link, tramite, analista, classificacao, modulo, topico, desc_encaminhamento, justificativa= '', validado=True):
    try:
        novo_encaminhamento = EncaminhamentoIncorreto.objects.create(datahora=datahora, 
                                                                    link=link, 
                                                                    tramite=tramite, 
                                                                    analista=analista, 
                                                                    classificacao=classificacao, 
                                                                    modulo=modulo, 
                                                                    topico=topico, 
                                                                    desc_encaminhamento=desc_encaminhamento,
                                                                    justificativa=justificativa,
                                                                    validado=validado)
        novo_encaminhamento.save()
    except Exception as e:
        erro = {"erro" : e}
        print(e)
        return render (request=request, template_name="encaminhamentos_incorretos/erro.html", context=erro)

def adiciona_encaminhamento(request, datahora, link, tramite, analista, classificacao, modulo, topico):
    try:
        novo_encaminhamento = Encaminhamento.objects.create(datahora=datahora, 
                                                            link=link, 
                                                            tramite=tramite, 
                                                            analista=analista, 
                                                            classificacao=classificacao, 
                                                            modulo=modulo, 
                                                            topico=topico)
        novo_encaminhamento.save()
    except Exception as e:
        erro = {"erro" : e}
        return render (request=request, template_name="encaminhamentos_incorretos/erro.html", context=erro)

def adicionar_encaminhamentos(request):
    try:
        incorreto = True if request.POST.get('incorreto') == 'on' else False
        if not request.FILES.get('planilha'):
            datahora = request.POST.get('datahora')
            link = request.POST.get('link')
            tramite = request.POST.get('tramite')
            analista = User.objects.get(id=request.POST.get('analista')[0])
            classificacao = request.POST.get('classificacao')
            modulo = request.POST.get('modulo')
            topico = request.POST.get('topico')

            if incorreto == True:
                desc_encaminhamento = request.POST.get('descricao')
                justificativa = request.POST.get('justificativa')
                validado = True if request.POST.get('validado') == 'on' else False

                adiciona_encaminhamento_incorreto(request, datahora, link, tramite, analista, classificacao, modulo, topico, desc_encaminhamento, justificativa, validado)
            else:
                print("Taf")
                adiciona_encaminhamento(request, datahora, link, tramite, analista, classificacao, modulo, topico)
        else:  
            planilha = request.FILES.get('planilha')
            planilha_df = pd.read_excel(planilha)
            validado = True if request.POST.get('validado') == 'on' else False

            for i, encaminhamento in planilha_df.iterrows():
                nome_analista = encaminhamento['Técnico'].split()
                primeiro_nome_analista = nome_analista[0]
                ultimo_nome_analista = ' '.join(nome_analista[1:])
                datahora=timezone.make_aware(datetime.strptime(encaminhamento['Data do encaminhamento'], "%d/%m/%Y %H:%M"), timezone=timezone.utc)
                link=encaminhamento['Link SS']
                tramite=encaminhamento['Trâmite']
                analista=User.objects.get(first_name=primeiro_nome_analista, last_name=ultimo_nome_analista)
                classificacao=encaminhamento['Classificação']
                modulo=encaminhamento['Módulo']
                topico=encaminhamento['Tópico']
                desc_encaminhamento=encaminhamento['Descrição encaminhamento Incorreto']
                validado=validado
                justificativa = ''

                if incorreto == True:
                    print("Tafa")
                    adiciona_encaminhamento_incorreto(request, datahora, link, tramite, analista, classificacao, modulo, topico, desc_encaminhamento, justificativa, validado)
                else:
                    adiciona_encaminhamento(request, datahora, link, tramite, analista, classificacao, modulo, topico)
        
        return redirect('/adicionar_encaminhamentos_form/')
    except Exception as e:
            erro = {"erro" : e}
            return render (request=request, template_name="encaminhamentos_incorretos/erro.html", context=erro)

def listar_encaminhamentos(request):
    teste = 'teste'
    return render(request=request, template_name="encaminhamentos_incorretos/listar_encaminhamentos.html")
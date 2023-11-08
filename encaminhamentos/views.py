from django.shortcuts import render, redirect
from encaminhamentos.models import EncaminhamentoIncorreto, Encaminhamento, DiasAusencia
import pandas as pd
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import shutil, pandas as pd
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import F, Count
from django.db.models.functions import ExtractMonth

def meta_encaminhamentos_incorretos(request, ano):
    
    encaminhamentos = Encaminhamento.objects.filter(datahora__year = ano).annotate(month=ExtractMonth('datahora')).values('analista__username', 'month').annotate(total_encaminhamentos=Count('id'))
    encaminhamentos_incorretos = EncaminhamentoIncorreto.objects.filter(datahora__year = ano, validado=True).annotate(month=ExtractMonth('datahora')).values('analista__username', 'month').annotate(total_encaminhamentos_incorretos=Count('id'))

    return encaminhamentos
    

def index(request):
    query_analistas = User.objects.all()
    context_analistas = {"analistas" : list(query_analistas)}
    encaminhamentos = meta_encaminhamentos_incorretos(request, 2023)
    dados = list(encaminhamentos.values())
       
    return render (request, "encaminhamentos/index.html", {'context1' : encaminhamentos, 'context2' : encaminhamentos})

@login_required
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
        return render (request=request, template_name="encaminhamentos/erro.html", context=erro)

@login_required
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
        return render (request=request, template_name="encaminhamentos/erro.html", context=erro)
    
#AJUSTAR ESSA VIEW< DESORGANIZADA
@login_required
def adicionar_encaminhamentos(request):
        if request.method == "GET":
            analistas = User.objects.all()
            analistas_list = list(analistas.values())
            context_data = {'analistas': analistas_list}
            return render (request=request, template_name="encaminhamentos/adicionar_encaminhamentos.html", context=context_data)
        else:
            request.method == "POST"
            incorreto = True if request.POST.get('incorreto') == 'on' else False
            erros = []

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
                    
                    query_encaminhamento_incorreto = EncaminhamentoIncorreto.objects.filter(link=link, tramite=tramite)
                    
                    if query_encaminhamento_incorreto:
                        erro = f"SS: {link} - Trâmite: {tramite}"
                        erros.append(erro)
                    else:
                        adiciona_encaminhamento_incorreto(request, datahora, link, tramite, analista, classificacao, modulo, topico, desc_encaminhamento, justificativa, validado)
                else:
                    query_encaminhamento = Encaminhamento.objects.filter(link=link, tramite=tramite)
                    if query_encaminhamento:
                        erro = f"SS: {link} - Trâmite: {tramite}"
                        erros.append(erro)
                    else:
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
                    analista= User.objects.get(first_name=primeiro_nome_analista, last_name=ultimo_nome_analista)
                    classificacao=encaminhamento['Classificação']
                    modulo=encaminhamento['Módulo']
                    topico=encaminhamento['Tópico']
                    desc_encaminhamento=encaminhamento['Descrição encaminhamento Incorreto']
                    validado=validado
                    justificativa = ''

                    if incorreto == True:
                        query_encaminhamento_incorreto = EncaminhamentoIncorreto.objects.filter(link=link, tramite=tramite)
                    
                        if query_encaminhamento_incorreto:
                            erro = f"SS: {link} - Trâmite: {tramite}"
                            erros.append(erro)
                        else:
                            adiciona_encaminhamento_incorreto(request, datahora, link, tramite, analista, classificacao, modulo, topico, desc_encaminhamento, justificativa, validado)
                    else:
                        query_encaminhamento = Encaminhamento.objects.filter(link=link, tramite=tramite)
                        if query_encaminhamento:
                            erro = {f"SS: {link} - Trâmite: {tramite}"}
                            erros.append(erro)
                        else:
                            adiciona_encaminhamento(request, datahora, link, tramite, analista, classificacao, modulo, topico)
        for erro in erros:
            messages.error(request, erro)
        return redirect('/adicionar_encaminhamentos/')

@login_required
def listar_encaminhamentos(request):
    tipo_encaminhamento = request.POST.get('tipo_encaminhamento')

    if not tipo_encaminhamento or tipo_encaminhamento == 'encaminhamentos':
        query = Encaminhamento.objects.all()
        context = {'encaminhamentos' : query}
        return render(request=request, template_name="encaminhamentos/listar_encaminhamentos.html", context=context)
    
    elif tipo_encaminhamento == 'encaminhamentos-incorretos':
        query = EncaminhamentoIncorreto.objects.filter(validado=True)
        context = {'encaminhamentos' : query}
        return render(request=request, template_name="encaminhamentos/listar_encaminhamentos.html", context=context)
    
    else:
        query = EncaminhamentoIncorreto.objects.filter(validado=False)
        context = {'encaminhamentos' : query}
        return render(request=request, template_name="encaminhamentos/listar_encaminhamentos.html", context=context)

@login_required
def listar_usuarios(request):
    try:
        query = User.objects.all()
        context = {'usuarios' : query}

        if request.method == "GET":
            return render(request=request, template_name="encaminhamentos/usuarios.html", context=context)
        else:
            username = request.POST.get("username")
            nome = request.POST.get("nome")
            sobrenome = request.POST.get("sobrenome")
            password = request.POST.get("password")
            email = request.POST.get("email")
            novo_usuario = User.objects.create(username=username, first_name=nome, last_name=sobrenome, password=password, email=email)
            novo_usuario.save()

            return render(request=request, template_name="encaminhamentos/usuarios.html", context=context)
    except Exception as e:
        erro = {"erro" : e}
        return render (request=request, template_name="encaminhamentos/erro.html", context=erro)

@login_required
def dias_atendidos(request):
    try:
        query = DiasAusencia.objects.all()
        analistas = User.objects.all()
        context = {'meses' : query, "analistas" : analistas}

        if request.method == "GET":
            print("METODO GET")
            return render(request=request, template_name="encaminhamentos/dias_atendidos.html", context=context)
        
        if request.method == "POST":
            if request.POST.get('_method') == 'DELETE':
                query_mes = DiasAusencia.objects.filter(id=request.POST.get('id'))
                query_mes.delete()
                print("METODO DELETE")
                return render(request=request, template_name="encaminhamentos/dias_atendidos.html", context=context)
            else:
                analista = User.objects.filter(id=request.POST.get("analista"))[0]
                inicio = request.POST.get("inicio")
                fim = request.POST.get("fim")
                novo_mes = DiasAusencia.objects.create(analista=analista, inicio=inicio, fim=fim)
                novo_mes.save()
                print("METODO POST")
                return render(request=request, template_name="encaminhamentos/dias_atendidos.html", context=context)
    except Exception as e:
        erro = {"erro" : e}
        return render (request=request, template_name="encaminhamentos/erro.html", context=erro)

@login_required
def backup(request):
    try:
        data = datetime.today().date()
        db_path = 'db.sqlite3' 
        backup_path = f'backup/{data} - backup_db.sqlite3'
        shutil.copy(db_path, backup_path)

        return redirect('/adicionar_encaminhamentos_form/')
    except Exception as e:
        erro = {"erro" : e}
        return render (request=request, template_name="encaminhamentos/erro.html", context=erro)
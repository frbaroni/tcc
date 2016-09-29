from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from tcc.models import Sensor, Tipo, Dado, Alerta, AlertaConfig
import json
import datetime

def index(request):
    contexto = {}
    contexto['sensorId'] = 0
    contexto['titulo'] = 'Home'
    contexto['regioes'] = listarRegioes()
    return render(request, 'tcc/index.html', contexto)

def sensores(request):
    contexto = {}
    contexto['titulo'] = 'Sensores'
    contexto['regioes'] = listarRegioes()
    return render(request, 'tcc/sensores.html', contexto)

def graficos(request):
    contexto = {}
    contexto['titulo'] = 'Mapas e graficos'
    contexto['regioes'] = listarRegioes()
    return render(request, 'tcc/mapas_e_graficos.html', contexto)

def mensagens(request):
    contexto = {}
    contexto['titulo'] = 'Mesagens'
    alertas = Alerta.objects.order_by('-id')
    contexto['alertas'] = alertas[:13]
    contexto['regioes'] = listarRegioes()
    return render(request, 'tcc/mensagens.html', contexto)

@csrf_exempt
def configuracoes(request):
    contexto = {}
    contexto['titulo'] = 'Configurações'

    if request.POST:
        AlertaConfig.objects.all().delete()
        for nome in request.POST:
            valor = request.POST[nome]
            tipo, op = nome.split('_')

            alertacfg = AlertaConfig()
            alertacfg.tipo = Tipo.objects.get(nome=tipo)
            if op == 'MAX':
                alertacfg.operador = '>'
            else:
                alertacfg.operador = '<'
            alertacfg.valor = float(valor)
            alertacfg.save()

    alertas = AlertaConfig.objects.all()
    for alerta in alertas:
        tipo = alerta.tipo.nome
        op = ''
        if alerta.operador == '>':
            op = 'MAX'
        else:
            op = 'MIN'
        chave = tipo + '_' + op
        contexto[chave] = alerta.valor
    contexto['regioes'] = listarRegioes()
    return render(request, 'tcc/configuracoes.html', contexto)


def listarRegioes():
    listaRegioes = []
    regioes = Sensor.objects.all()
    for regiao in regioes:
        listaRegioes.append({'id': regiao.id, 'nome': regiao.nome})
    return listaRegioes


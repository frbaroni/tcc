from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from tcc.models import Sensor, Tipo, Dado, Alerta, AlertaConfig
import json
import datetime

# Formato usado na comunicacao de dados, tanto na hora de receber a chamada de um servico, quanto para enviar dados para o navegador.
# O formato e o formato padrao Javascript, para facilitar a comunicacao com os servicos
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
HISTORICO_DATE_FORMAT = '%Y-%m-%dT%H:00:00'

# Funcao que le uma string e retorna um datetime representando uma data/hora no tempo.
def unserializeDate(serialized):
    return datetime.datetime.strptime(serialized, DATE_FORMAT)

# Funcao transforma um datetime, representando uma data/hora no tempo, em uma string formatada no padrao Javascript..
def serializeDate(unserialized):
    return datetime.datetime.strftime(unserialized, DATE_FORMAT)

# Funcao transforma um datetime, representando uma data/hora no tempo de um historico
def serializeHistoricoDate(unserialized):
    return datetime.datetime.strftime(unserialized, HISTORICO_DATE_FORMAT)

####################################
### Definicoes gerais de servico ###
####################################
# <DATA> = YYYY-MM-DD-HH-MM-SS
# <TIPO> = TemperaturaAr|TemperaturaSolo|UmidadeAr|UmidadeSolo|Chuva

##################################
### Inserir dados a um sensor: ###
##################################
#  POST http://localhost:8081/tcc/sensor/<ID_SENSOR>/inserir
#  BODY dado=valor&dado2=valor2&dado3=valor3

# Exemplo:
#  POST http://localhost:8081/tcc/sensor/1/inserir
#  BODY Chuva=100.0&UmidadeAr=60.3&UmidadeSolo=73.5&TemperaturaAr=22.3&TemperaturaSolo=18.0

# Essa anotacao faz com que o Django desligue as protecoes anti-cross site, que sao ataques conhecidos no mundo de hackers.
# Como os servicos sao publicos, essa protecao nao pode estar ativo, pois
# Request e um objeto do sistema django que recupera as informacoes que o navegador passa
@csrf_exempt
def inserir(request, sensorId):
    # O parametro sensorId e obrigatorio

    # Achamos no banco de dados um sensor cujo ID igual ao sensorId passado ao servico
    sensor = Sensor.objects.get(id=sensorId)
    # SELECT sensor FROM Sensor WHERE id = sensorId

    # Criamos uma array para armazenar os novos Dados
    dados = []

    # Iteramos todos os valores dentro do dicionario POST, contendo os valores submetidos ao servico
    for chave in request.POST:
        # Armazenamos o valor de uma chave
        valor = request.POST[chave]

        # Procuramos no banco de dados, um tipo cujo NOME = CHAVE
        tipo = Tipo.objects.get(nome=chave)

        # Criamos um objeto do tipo Dado()
        # O horario da submissao e implicito como valor `default` da tabela como horario atual
        dado = Dado()

        # Armazenamos o sensor relacionado,
        dado.sensor = sensor

        # O tipo da informacao armazenada
        dado.tipo = tipo

        # O valor submetido ao servico (como por exemplo a temperatura, humidade...)
        dado.valor = float(valor)

        # Adicionamos esse novo objeto a um array, para aplicar as alteracoes depois
        dados.append(dado)

    # Depois de ter coletado todos os novos objetos do tipo Dado(),
    # Iteramos o array contendo todos aqueles novos dados
    for dado in dados:
        # Usamos a funcao do Django "models.save()" para inserir e atualizar valores no banco de dados
        dado.save()

    # Iteramos o array contendo todos aqueles novos dado
    # Para verificar se precisamos disparar algum alerta
    for dado in dados:
        # Procuramos os AlertaConfigs no banco de dados que possuem o mesmo tipo#
        alertaconfigs = AlertaConfig.objects.filter(tipo=dado.tipo)

        # Iteramos o resultado dessa pesquisa
        for alertaconfig in alertaconfigs:
            # Verificamos se o alerta deve ser disparado, ou seja,
            # se o valor é maior que o minimo ou maximo definidos
            # na tabela de configurações de alertas
            if (
                    (
                        (alertaconfig.operador == '>')
                        and
                        (dado.valor > alertaconfig.valor)
                    ) or (
                        (alertaconfig.operador == '<')
                        and
                        (dado.valor < alertaconfig.valor)
                    )
                ):
                # Validamos se o ultimo alerta desta alertaconfig não foi disparado
                # com esse mesmo valor, para evitar disparar alertas iguais
                try:
                    # Tentamos encontrar o ultimo alerta da tabela
                    ultimoAlerta = Alerta.objects.filter(operador=alertaconfig.operador, tipo=alertaconfig.tipo).latest('horario')
                    # Se encontrado, verificamos se o valor é igual
                    if ultimoAlerta.valor == dado.valor:
                        # Se for igual, pulamos para o proximo loop
                        # E não salvamos um alerta no banco de dados (para evitar repetidos)
                        continue
                except:
                    # Ocorre uma exceção se um ultimoAlerta não for encontrado
                    pass
                alerta = Alerta()
                alerta.dado = dado
                alerta.valor = alertaconfig.valor
                alerta.tipo = alertaconfig.tipo
                alerta.operador = alertaconfig.operador

                # Inserimos esse novo alert na tabela
                alerta.save()
    # Se tudo der certo, retornamos 'Ok' para o cliente que chamou o servico
    # Essa mensagem pode nao ser enviada, caso ocorra alguma excecao na submissao dos novos dados
    # Um exemplo de excecao seria quando o chamador do servico tenta inserir um Tipo() de dado nao cadastrado
    return HttpResponse('Ok')



def lerDados(sensorId, tipo=None, filtroData=None, filtroMaximo=None):
    # O parametro sensorId e obrigatorio
    # Os parametros tipo e filtroData sao opcionais, inicializados como None por padrao

    # Achamos no banco de dados um sensor cujo ID igual ao sensorId passado ao servico
    sensor = Sensor.objects.get(id=sensorId)

    # Criamos uma query ao banco de dados, que filtra por sensores iguais ao sensor encontrado na linha de cima
    dados = Dado.objects.filter(sensor=sensor)

    # Quando o parametro filtroData nao for None
    if filtroData is not None:
        # Transformamos a string filtroData em um objeto datetime, e atribuimos a variavel horario
        horario = unserializeDate(filtroData)
        horario = horario + datetime.timedelta(seconds=1)
        #horario = serializeDate(horario)

        # Modificamos a query para filtrar por dados cujo o horario seja maior que o objeto horario criado na linha a cima
        # Para comparar dados nas queries Django, usamos a notacao:
        # field__operacao=valor
        # No caso, o field e horario, e a operacao greater than (GT)
        # Comparamos o dado com o nosso valor horario
        dados = dados.filter(horario__gt=horario)

    # Quando o parametro tipo nao for None
    if tipo is not None:
        # Procuramos no banco de dados, um tipo cujo nome igual ao parametro tipo
        tipoo = Tipo.objects.get(nome=tipo)

        # Modificamos a query para filtrar por dados cujo o tipo seja igual ao objeto tipoo criado na linha a cima
        # Dessa vez, a anotacao de comparacao e:
        # field=valor
        # Procurando por vlaores exatos
        dados = dados.filter(tipo=tipoo)

    if filtroMaximo is not None:
        filtroMaximo = int(filtroMaximo)
        dados = dados.order_by('-id')[:filtroMaximo]


    # Criamos uma array vazia para armazenar o retorno, os dados que virao do banco de dados
    retorno = []

    # Executamos a query no banco de dados, e iteramos o resultado
    # O Django sabe quando precisa executar uma query no banco de dados,
    # Ele permite que alteremos a query como fizemos no codigo anterior
    # Sem executar nada no banco, ate o horario que realmente precisamos do resultado (como por exemplo, na repeticao for a baixo)
    for dado in dados:
        # Criamos uma tupla com os valores 'horario, tipo e valor'
        # No caso do horario, convertemos para o formato Javascript usando a funcao definia no cabecalho desse arquivo, serializeDate()
        tupla = {
            'horario': serializeDate(dado.horario),
            'tipo': dado.tipo.nome,
            'valor': dado.valor
        }
        # Adicionamos essa tupla ao array de retorno
        retorno.append(tupla)

    return retorno

def retornoJson(valor):
    # Serializamos o array contendo todas as tuplas para uma string Json, formato 'Javascript Object Notation'.
    serializado = json.dumps(valor)

    # Criamos um retorno para enviar ao chamador do servico, as tuplas resultantes, serializadas em formato Json
    response = HttpResponse()
    response.write(serializado)
    return response



#################################
### Ler os dados de um sensor ###
#################################
#  GET http://localhost:8081/tcc/sensor/<ID_SENSOR>/ler
#  GET http://localhost:8081/tcc/sensor/<ID_SENSOR>/ler/<LIMITE_ROWS>
#  GET http://localhost:8081/tcc/sensor/<ID_SENSOR>/ler/<DATA>
#  GET http://localhost:8081/tcc/sensor/<ID_SENSOR>/ler/<TIPO>
#  GET http://localhost:8081/tcc/sensor/<ID_SENSOR>/ler/<TIPO>/<DATA>

# Exemplos:
# Ler todos os dados do sensor com ID = 1.
#  GET http://localhost:8081/tcc/sensor/1/ler

# Ler apenas os dados 'Chuva' do sensor com ID = 1.
#  GET http://localhost:8081/tcc/sensor/1/ler/Chuva

# Ler apenas os dados 'Chuva' do sensor com ID = 1 que foram submetidos depois da data 2015-07-18, as 20:58:19.
#  GET http://localhost:8081/tcc/sensor/1/ler/Chuva/2015-07-18T20:58:19

# Essa anotacao faz com que o Django desligue as protecoes anti-cross site, que sao ataques conhecidos no mundo de hackers.
# Como os servicos sao publicos, essa protecao nao pode estar ativo, pois
@csrf_exempt
def ler(request, sensorId, tipo=None, filtroData=None, filtroMaximo=None):
    # Le todos os dados do banco de dados
    valores = lerDados(sensorId=sensorId, tipo=tipo, filtroData=filtroData, filtroMaximo=filtroMaximo)

    # Retorna em formato json
    return retornoJson(valores)


####################################
### Ler o historico de um sensor ###
####################################
# Usa os mesmos parametros do servico 'ler'
@csrf_exempt
def historico(request, sensorId, tipo=None, filtroData=None, filtroMaximo=None):
    # Le todos os dados do banco de dados
    dados = lerDados(sensorId=sensorId, tipo=tipo, filtroData=filtroData, filtroMaximo=filtroMaximo)

    # Cria um dicionario vazio para fazer os calculos
    historico = {}

    # Itera esses dados
    for dado in dados:
        # Pega os valores desse dado
        tipo = dado['tipo']
        valor = dado['valor']
        data = unserializeDate(dado['horario'])

        # Serializa o horario em um formato para agrupar os dados
        data = serializeHistoricoDate(data)

        # Verifica se o dicionario de historico já possui esse tipo
        if tipo not in historico:
            historico[tipo] = {}

        # Verifica se o dicionario já tem essa data nesse tipo
        if data not in historico[tipo]:

            # Quando não tem, inicia com valores padrões
            historico[tipo][data] = {
                    'periodo': data,
                    'min': valor,
                    'max': valor,
                    'sum': 0,
                    'avg': 0,
                    'items': 0,
                    }

        # E atualiza as informações, agora com a garantia de que esse tipo+data está
        # armazenado no dicionario Historico
        historico[tipo][data]['max'] = max(valor, historico[tipo][data]['max'])
        historico[tipo][data]['min'] = min(valor, historico[tipo][data]['min'])
        historico[tipo][data]['sum'] += valor
        historico[tipo][data]['items'] += 1

    # Itera os tipos e datas
    for tipo in historico:
        for data in historico[tipo]:
            # Para criar o 'avg' (average)
            items = historico[tipo][data]['items']
            soma = historico[tipo][data]['sum']
            historico[tipo][data]['avg'] = soma / items

    # Retorna o historico transforamndo em json
    return retornoJson(historico)

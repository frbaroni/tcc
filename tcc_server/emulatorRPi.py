import sys
from time import sleep
from random import randint
from urllib.request import urlopen
from urllib.parse import urlencode

if len(sys.argv) != 2:
    print('Por favor, usar: ' + sys.argv[0] + ' {idSensor}')
    print('Exemplo: ' + sys.argv[0] + ' 8')
else:
    sensorId = sys.argv[1]
    URL_SERVICO = 'http://127.0.0.1:8081/tcc/sensor/' + sensorId + '/inserir'
    VARIACAO_MAXIMA = 5
    valores = {
            'Chuva': 80.0,
            'UmidadeAr': 85.0,
            'UmidadeSolo': 80.0,
            'TemperaturaAr': 30.0,
            'TemperaturaSolo': 25.0
        }
    variacao = {}
    for k in valores:
        valores[k] = valores[k] + randint(-3, +3) / 10
        variacao[k] = 0.0

    accel = {}
    while True:
        for k in variacao:
            accel[k] = randint(-1.0, +1.0) / 10
        r = randint(10, 30)
        for i in range(r):
            data = {}
            for k in variacao:
                variacao[k] = variacao[k] + accel[k]
                variacao[k] = max(variacao[k], -VARIACAO_MAXIMA)
                variacao[k] = min(variacao[k], +VARIACAO_MAXIMA)
                data[k] = '%.2f' % (valores[k] + round(variacao[k], 2))
            data = urlencode(data)
            print(data)
            urlopen(URL_SERVICO, data.encode('ascii'))
            sleep(0.50)

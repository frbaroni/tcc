import urllib.request
import urllib.parse
from os import listdir
from os.path import isfile, join

# Coleta o ID do sensor lendo o arquivo idSensor
f = open('idSensor', 'r')
idSensor = f.read().strip()
f.close()

# Cria a URL para a postagem
url = 'http://fernando.local:8081/tcc/sensor/' + idSensor + '/inserir'
# url = 'http://192.168.1.101:8081/tcc/sensor/' + idSensor + '/inserir'

# Define o diretorio de leitura dos dados
diretorio = 'dados'

# Os valores sao adicionados a um dicionario, que sera enviado ao servico
valores = {}

# Pegar os valores dos arquivos na pasta ./dados
# O nome de cada arquivo sera usado como o tipo do dado, o conteudo sera usado como valor.
for nome in listdir(diretorio):
    # Junta o nome do arquivo com o diretorio
    arquivo = join(diretorio, nome)

    # Verifica se nome 'e um arquivo
    if isfile(arquivo):
        # Le o valor do arquivo
        f = open(arquivo, 'r')
        valor = f.read().strip()
        f.close()

        # Adiciona o novo valor para o dicionario de valores
        valores[nome] = valor

print('POST %s\n%s' % (url, str(valores)))

# Faz a postagem para o servico
data = urllib.parse.urlencode(valores).encode('utf-8')
urllib.request.urlopen(url, data)

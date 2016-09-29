from django.db import models

# Declara os modelos do nosso aplicativo, a partir de cada modelo, uma tabela no banco de dados e gerada automaticamente.
# O Django gerencia o banco de dados, ele verifica as alteracoes automaticamente e aplica-as no banco de dados.

# Para fazer o Django criar os comandos sql com o nome definidos no  model
# > python manage.py makemigrations

# Para executar o codigo sql gerado pelo makemigration
# > python manage.py migrate

# Os fields (tipos de campos)  usados sao:
# models.AutoField -> field incrementado automaticamente (no PostgreSQL - Serial);
# models.FloatField -> field que pode armazenar um valor de ponto flutuante (exemplo: 1.0, 3.14);
# models.DateTimeField -> field que armazena um ponto no tempo, com data e horario;
# models.ForeignKey -> field que armazena a relacao entre duas tabelas

# Quando definimos uma funcao "def __str__(self)", o Django usa essa fucao para mostrar os valores nas apresentacoes.

##################################
### Definicao do modelo Sensor ###
##################################
class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=32)
    desc = models.CharField(max_length=200)
    ultimaAtualizacao = models.DateTimeField()
    posicaoX = models.FloatField()
    posicaoY = models.FloatField()
    def __str__(self):
        return '{0} {1}'.format(self.id, self.nome)

################################
### Definicao do modelo Tipo ###
################################
class Tipo(models.Model):
    nome = models.CharField(primary_key=True, max_length=16)
    def __str__(self):
        return self.nome

################################
### Definicao do modelo Dado ###
################################
class Dado(models.Model):
    sensor = models.ForeignKey(Sensor)
    tipo = models.ForeignKey(Tipo)
    horario = models.DateTimeField(auto_now=True)
    valor = models.FloatField()
    def __str__(self):
        return '[{0} {1}] {2} {3}'.format(self.horario, self.sensor, self.tipo, self.valor)

##################################
### Definicao do modelo Alerta ###
##################################
class Alerta(models.Model):
    dado = models.ForeignKey(Dado)
    tipo = models.ForeignKey(Tipo)
    operador = models.CharField(max_length=1)
    valor = models.FloatField()
    horario = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{0} {1} {2} {3}'.format(str(self.tipo), self.operador, self.valor, str(self.dado))

########################################
### Definicao do modelo AlertaConfig ###
########################################
class AlertaConfig(models.Model):
    tipo = models.ForeignKey(Tipo)
    operador = models.CharField(max_length=1)
    valor = models.FloatField()
    def __str__(self):
        return '{0} {1} {2}'.format(str(self.tipo), self.operador, self.valor)



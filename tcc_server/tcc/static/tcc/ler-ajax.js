// Função usada para ler dados do servidor e retornar na função 'callback' os dados lidos
function ler(url, callback) {
    // Faz a requisição AJAX ao servidor
    $.ajax({
        type: 'GET',
        url: url,
        contentType: 'application/json',
        dataType: 'json',
        success: function (dados) {
            // Se for bem sucedido, recebe os dados na variavel 'dados'
            // Criamos um dicionario para armazenar os dados lidos
            var series = {};

            // Um para armazenar os tipos de dados lidos (como Chuva, UmidadeAr, TemperaturaSolo...)
            var tipos = [];

            // Outro para armazenar o resultado no formato Highcharts
            var resultado = [];

            // Iteramos todos os dados recebidos do serviço
            for (var i = 0; i < dados.length; i++) {
                // Criamos uma variavel para acessar o dado iterado 'dados[i]'
                var dado = dados[i];

                // Criamos uma variavel com o tipo lido, relacionado ao elemento sendo iterado
                var tipo = dado.tipo;

                // Criamos uma variavel com o horario lido, relacionado ao elemento sendo iterado
                var horario = dado.horario;

                // Criamos uma variavel com o valor lido, relacionado ao elemento sendo iterado
                var valor = dado.valor;

                // Verificamos se o tipo lido já se encontra no nosso dicionario de informações
                if(!series[tipo]) {
                    // Caso esse tipo não exista, criamos esse elemento no dicionario
                    series[tipo] = {
                        // Atribuimos a variavel 'name' para o valor do tipo. Essa variavel
                        // 'name' é usada pelo highcharts para apresentar as series.
                        name: tipo,

                        // Atribuimos a variavel 'data' um array vazio, que vai ser concatenado
                        // com os valores lidos em cada iteração
                        data: []
                    };

                    // Depois de registrar um novo tipo no dicionario, adicionamos o nome do tipo na lista de tipos
                    // pois isso facilita a transformação de dicionario para lista de listas, formato aceito pelo highcharts
                    tipos.push(tipo);
                }
                // Agora com a garantia de que esse tipo se encontra no dicionario, adicionamos uma tupla: [horario, valor]
                // com os dados lidos dessa iteração. Esse formato, [horario, valor] é o formato que o Highcharts aceita
                // quando o timespan de dados pode variar
                series[tipo].data.push([horario, valor]);
            }

            // Depois de gerar o dicioario de dados, no formato:
            // tipo[TIPO]{name: NOME, data: [[HORARIO1, DADO1], [HORARIO2, DADO2], [HORARIO3, DADO3], ...]}
            // Adicionamos esse objeto em um array simples, pois o HIGHCAHRTS não espera um dicionario de dados, mas um array de dados.
            for(var i = 0; i < tipos.length; i++) {
                resultado.push(series[tipos[i]]);
            }

            // Chamamos a função callback com o resultado adquirido
            callback(resultado);
        },
        failure: function () {
            callback([]);
        }
    });
}

// Função usada para converter Json date para UTC date
function dateFromUTCString(s) {
    s = s.split(/[\D]/ig);
    return Date.UTC(s[0], --s[1], s[2], s[3], s[4], s[5], s[6]||0);
}

// Função usada para ler historico do servidor e retornar na função 'callback' os dados lidos
function lerHistorico(sensorId, callback) {
    // Faz a requisição AJAX ao servidor
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8081/tcc/sensor/' + sensorId + '/historico',
        contentType: 'application/json',
        dataType: 'json',
        success: function (dados) {
            var resultado = [];
            for(var tipo in dados) {
                var periodos = [];
                var mins = [];
                var maxs = [];
                var avgs = [];
                var data = dados[tipo];
                for(var periodo in data) {
                    var tupla = data[periodo];
                    periodos.push(dateFromUTCString(periodo));
                    mins.push(tupla['min']);
                    maxs.push(tupla['max']);
                    avgs.push(tupla['avg']);
                }
                resultado[tipo] = {
                    'periodos': periodos,
                    'mins': mins,
                    'maxs': maxs,
                    'avgs': avgs
                };
            }
            callback(resultado);
        },
        failure: function () {
            callback([]);
        }
    });
}

// Função que faz refresh automaticamente de dados usando o servico
function lerAuto(sensorId, tipo, chartSeries) {
    function atualizar(sensorId_, series_, filtro_) {
        var sensorId = getSensorId();
        var url = 'http://localhost:8081/tcc/sensor/' + sensorId + '/ler/' + tipo + '/';
        var series = series_;
        var filtro = filtro_;

        if(sensorId_ == sensorId) {
            var tirarAntigos;
            if(filtro != null) {
                url += filtro;
                tirarAntigos = true;
            } else {
                url += 20;
                tirarAntigos = false;
            }
            ler(url, function(resultado) {
                var maiorHorario = filtro;
                for(var i = 0; i < resultado.length; i++) {
                    var serie = resultado[i];
                    var name = serie.name;
                    var data = serie.data;
                    for(var j = 0; j < data.length; j++) {
                        var ponto = data[j];
                        var horario = ponto[0];
                        var valor = ponto[1];
                        var tupla = [dateFromUTCString(horario), valor];
                        series.addPoint(tupla, true, tirarAntigos, true);
                        if(maiorHorario == null || horario > maiorHorario) {
                            maiorHorario = horario;
                        }
                    }
                }
                setTimeout(atualizar, 5000, sensorId, series, maiorHorario);
            });
        }
    }
    atualizar(sensorId, chartSeries, null); 
}


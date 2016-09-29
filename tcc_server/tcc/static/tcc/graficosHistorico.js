$(function(){
    var graficos = [
    {
        'tipo': 'TemperaturaSolo',
        'titulo': 'Temperatura do solo',
        'legenda': 'Temperatura em °C',
        'sufixo': '°C',
    }, {
        'tipo': 'TemperaturaAr',
        'titulo': 'Temperatura do ar',
        'legenda': 'Temperatura em °C',
        'sufixo': '°C',
    }, {
        'tipo': 'UmidadeSolo',
        'titulo': 'Umidade do solo',
        'legenda': 'Umidade em %',
        'sufixo': '%',
    }, {
        'tipo': 'UmidadeAr',
        'titulo': 'Umidade do ar',
        'legenda': 'Umidade em %',
        'sufixo': '%',
    }, {
        'tipo': 'Chuva',
        'titulo': 'Chuva',
        'legenda': 'Chuva em %',
        'sufixo': '%',
    },

    ];
    function criarGraficos() {
        function criarGrafico(meta) {
            meta['grafico'] = $('#container' + meta['tipo']).highcharts({
                title: {
                    text: meta['titulo'],
                    x: -20 //center
                },
                xAxis: {
                    type: 'datetime',
                    labels: {
                        formatter: function() {
                            return Highcharts.dateFormat('%a %d %b', this.value);
                        }
                    },
                },
                yAxis: {
                    title: {
                        text: meta['legenda']
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: meta['sufixo'] 
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: 'Minimo',
                }, {
                    name: 'Maximo',
                }, {
                    name: 'Media',
                }]
            });
        };
        for(var i = 0; i < graficos.length; i++) {
            criarGrafico(graficos[i]);
        }
        var sensorId = getSensorId();
        lerHistorico(sensorId, function(resultado) {    
            for(var i = 0; i < graficos.length; i++) {
                var meta = graficos[i];
                var tipo = meta['tipo'];
                var grafico = $(meta['grafico']).highcharts();
                grafico.xAxis[0].categories = resultado[tipo]['periodos'];
                grafico.series[0].setData(resultado[tipo]['mins']);
                grafico.series[1].setData(resultado[tipo]['maxs']);
                grafico.series[2].setData(resultado[tipo]['avgs']);
            }
        });
    }
    function atualizarHistorico(sensorId_) {
       var sensorId = getSensorId();
       if(sensorId != sensorId_) { 
           criarGraficos();
       }
       setTimeout(atualizarHistorico, 100, sensorId);
    };
    atualizarHistorico(null);
});


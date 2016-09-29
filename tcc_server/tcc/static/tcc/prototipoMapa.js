$(function(){
    //INICIAR GRÁFICO
    var mapaChart = $('#containerMap').highcharts('Map', {
        plotOptions: {
            series: {
                events: {
                    click: function (e) {
                        var sensorId = e.point.sensorId;
                        setSensorId(sensorId);
                        atualizaInfoMapa();
                    }
                }
            }
        },
        tooltip: {
           formatter: function() {
                return regioes[this.point.sensorId];
           }
            },
        series: [
        {
            "type": "map",
            "name": "Monitoração Ambiental do Território",
            "data": [
            {
                "name": regioes[1],
                "sensorId": 1,
                "path": "M521,-697,314,-720,70,-680,6,-546,0,-445,20,-313,39,-255,92,-210,95,-210,232,-196,451,-196,535,-232,549,-356,532,-482,532,-605z",
                color: '#ccccdd',
                states: {
                    hover: {
                        color: '#dddd88'
                    }

                }

            },
            {
                "name": regioes[2],
                "sensorId": 2,
                "path": "M521,-697,532,-610,532,-490,548,-361,536,-240,622,-221,804,-227,902,-252,969,-288,972,-459,955,-619,933,-711,754,-734,636,-722z",
                color: '#ddcccc',
                states: {
                    hover: {
                        color: '#dddd88'
                    }

                }
            },
            {
                "name": regioes[4],
                "sensorId": 4,
                "path": "M969,-288,1000,-73,944,107,913,166,697,210,566,205,499,174,501,39,490,-73,494,-214,535,-235,546,-238,610,-224,734,-224,798,-226,854,-240,902,-252z",
                color: '#ccddcc',
                states: {
                    hover: {
                        color: '#dddd88'
                    }

                }
            },
            {
                "name": regioes[3],
                "sensorId": 3,
                "path": "M95,-210,62,-50,62,51,34,185,188,230,389,227,501,175,501,59,494,-39,491,-95,492,-137,487,-211,460,-200,356,-196,249,-196,185,-201,106,-209",
                states: {
                    hover: {
                        color: '#dddd88'
                    }

                }
            }
            ]
        }
        ]

    });

    function atualizaInfoMapa() {
        var chart = $(mapaChart).highcharts();
        chart.setTitle({text: 'Carregando ' + regioes[getSensorId()] + '...'});
        if (!chart.label) {
            chart.label = chart.renderer.label(' ', 0, 100)
                .css({
                    width: '300px',
                    heigth: '50px'

                })
            .add();
        }
        chart.label.attr({text: 'Carregando...'}); 
        lerHistorico(getSensorId(), function(resultado) {
            var temperaturaSoloMax = Math.max.apply(Math, resultado['TemperaturaSolo']['maxs']);
            var temperaturaSoloMin = Math.min.apply(Math, resultado['TemperaturaSolo']['mins']);
            var umidadeSoloMax = Math.max.apply(Math, resultado['UmidadeSolo']['maxs']);
            var umidadeSoloMin = Math.min.apply(Math, resultado['UmidadeSolo']['mins']);
            var temperaturaArMax = Math.max.apply(Math, resultado['TemperaturaAr']['maxs']);
            var temperaturaArMin = Math.min.apply(Math, resultado['TemperaturaAr']['mins']);
            var umidadeArMax = Math.max.apply(Math, resultado['UmidadeAr']['maxs']);
            var umidadeArMin = Math.min.apply(Math, resultado['UmidadeAr']['mins']);
            var text = 
                '<br><b>' + regioes[getSensorId()] + '</b>' +
                '<br><h3><b>Solo</b></h3>' +
                '<br><b>Temperatura Máxima: </b>' + temperaturaSoloMax + ' ºC' +
                '<br><b>Temperatura Mínima: </b>' + temperaturaSoloMin + ' ºC' +
                '<br><b>Umidade Máxima: </b>' + umidadeSoloMax + '%' +
                '<br><b>Umidade Mínima: </b>' + umidadeSoloMin + '%' +
                '<br>' + 
                '<br><br><h3><b>Ar</b></h3>'+
                '<br><b>Temperatura Máxima: </b>' + temperaturaArMax + ' ºC' +
                '<br><b>Temperatura Mínima: </b>' + temperaturaArMin + ' ºC' +
                '<br><b>Umidade Máxima: </b>' + umidadeArMax + '%' +
                '<br><b>Umidade Mínima: </b>' + umidadeArMin + '%' +
                '<br>';
            chart.setTitle({text: regioes[getSensorId()]});
            chart.label.attr({text: text}); 
        });
    }
    atualizaInfoMapa();
});

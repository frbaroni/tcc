$(function () {
    function criarGraficosHome() {
        // GRÁFICO 1 COM MOTOR DE ATUALIZAÇÃO
        var container1 = $('#container1').highcharts({
            chart:{
                type: 'line',
                zoomType: 'xy',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 30
            },
            title: {
                text: 'Temperatura'
            },
            xAxis: {
                type: 'datetime',
                crosshair: true,
            },
            yAxis: { // Primeiro eixo yAxis no lado esquerdo do gréfico
                labels: {
                    format: '{value} ºC',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Temperatura em ºC',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, 
            tooltip: {
                formatter: function () {
                    var msgTooltip = '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%d/%m/%Y %H:%M:%S', this.x) + '<br/> Valor ' +
                        Highcharts.numberFormat(this.y, 2) + ' ºC';
                    return msgTooltip;
                }
            },
            legend: {
                enabled: true
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Temperatura do solo em ºC',
                color: '#A52A2A',
                data: []
            }, {
                name: 'Temperatura do ar em ºC',
                color: '#6A5ACD',
                data: []
            }
            ]
        });
        var chartSeries = $(container1).highcharts().series;

        // GRÁFICO 2 COM MOTOR DE ATUALIZAÇÃO
        var container2 = $('#container2').highcharts({
            chart:{
                type: 'line',
                zoomType: 'xy',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 30,
            },
            title: {
                text: 'Umidade'
            },
            xAxis: {
                type: 'datetime',
                crosshair: true,
            },
            yAxis: { // Primeiro eixo yAxis no lado esquerdo do gréfico
                labels: {
                    format: '{value} %',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Umidade em %',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, 
            tooltip: {
                formatter: function () {
                    var msgTooltip = '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y/%m/%d %H:%M:%S', this.x) + '<br/> Valor ' +
                        Highcharts.numberFormat(this.y, 2) + ' %';
                    return msgTooltip;
                }
            },

            legend: {
                enabled: true
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Umidade do solo em %',
                color: '#A52A2A',
                data: []
            }, {
                name: 'Umidade do ar em %',
                color: '#008B8B',
                data:  []
            }
            ]
        });
        var chartSeries2 = $(container2).highcharts().series;


        // GRÉFICO 3 COM MOTOR DE UPDATE
        var container3 = $('#container3').highcharts({
            chart:{
                type: 'spline',
                zoomType: 'xy',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 30
            },
            title: {
                text: 'Chuva'
            },
            xAxis: {
                type: 'datetime',
                crosshair: true,
            },
            yAxis: { // Primeiro eixo yAxis no lado esquerdo do gréfico
                labels: {
                    format: '{value} %',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Chuva/Agua %',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, 
            tooltip: {

                formatter: function () {

                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y/%m/%d %H:%M:%S', this.x) + '<br/> Valor ' +
                        Highcharts.numberFormat(this.y, 2);


                }
            },

            legend: {
                enabled: true
            },
            exporting: {
                enabled: false
            },
            series: [ 
            {
                name: 'Chuva/Agua %',
                color: '#008B8B',
                data: []
            }
            ]
        });
        var chartSeries3 = $(container3).highcharts().series;
        var sensorId = getSensorId();
        lerAuto(sensorId, 'UmidadeSolo', chartSeries2[0]);
        lerAuto(sensorId, 'UmidadeAr', chartSeries2[1]);
        lerAuto(sensorId, 'Chuva', chartSeries3[0]);
        lerAuto(sensorId, 'TemperaturaSolo', chartSeries[0]);
        lerAuto(sensorId, 'TemperaturaAr', chartSeries[1]);
    }
    function atualizarGraficosHome(sensorId_) {
       var sensorId = getSensorId();
       if(sensorId != sensorId_) { 
           criarGraficosHome();
       }
       setTimeout(atualizarGraficosHome, 100, sensorId);
    };
    atualizarGraficosHome(null);
});

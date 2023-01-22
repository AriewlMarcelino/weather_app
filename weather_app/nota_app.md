1. Utilizando uma api para pegar a Geolocation:
    - Para coletarmos a latituade e longitude em tempo real.
    - Utilizamos o modulo de JSON para imprimir nossa localização
    - E utilizamod o modulo pprint para melhor a visibilidade arquivos htmlde paginas.

2 - Utilizamos o Accuweater, onde criamos a nossa chave  para Api do tempo:
    - onde tambem usamos a bibliota datetime, para a conversão de valores numericos a valores reais de dia/hora/ano


diasSemana = ['Domingo','Segunda-Feira','Terça-feira','Quarta-feira','Quinta-Feira','Quinta-feira','Sexta-feira','Sabado']

diasSemana[int(date.fromtimestamp(1569391200).strftime('%w'))]

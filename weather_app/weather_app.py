import json
import requests
from datetime import date
import urllib.parse

# -23.543420, -46.298490

accuweatherAPIKey = 'wpX3VvyAXJNxAK33VBQFZLGHhPqvY8V4'
mapBox = "pk.eyJ1IjoicGF1bG9zaWx2YTEiLCJhIjoiY2xkN2k4MHh6MWxnbTNxcDUxZ2IyNjh4OCJ9.gDuvuAWUNoh3EvUGFwxqLg"

diasSemana = ['Domingo', 'Segunda-Feira', 'Terça-feira', 'Quarta-feira',
              'Quinta-Feira', 'Quinta-feira', 'Sexta-feira', 'Sabado']


def takeCoordenations():
    r = requests.get('http://www.geoplugin.net/json.gp?')

    if (r.status_code != 200):
        print('Não foi possivél obter a suas localização..')
        return None
    else:
        try:
            # Retorno a localização com JSON
            localizacao = json.loads(r.text)
            coodernadas = {}

            # Acessando a longitude e latitude da api de localização
            coodernadas['lat'] = localizacao['geoplugin_latitude']
            coodernadas['long'] = localizacao['geoplugin_longitude']
            return coodernadas
        except:
            return None


def takeCodeLocalizacion(lat, long):
    # Api de URL de localização na accuweater
    LocalizacionApiUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/" \
        + "search?apikey=" + accuweatherAPIKey \
        + "&q=" + lat + "%2C" + long + "&language=pt-br"

    # Fazendo uma nova requisição com accuweather
    r = requests.get(LocalizacionApiUrl)

    # Validando a URL LocalizacionApiUrl
    if (r.status_code != 200):
        print('Não foi possivél obter o clima atual.')
        return None
    else:
        try:
            LocationResponse = json.loads(r.text)

            infoLocal = {}

            # Pegando o nome do local:
            infoLocal['nomeLocal'] = LocationResponse['LocalizedName'] + ' , '\
                + LocationResponse['AdministrativeArea']['LocalizedName'] + ' . '\
                + LocationResponse['Country']['LocalizedName']
            # Pegando o código do local:
            infoLocal['codigoLocal'] = LocationResponse['Key']
            return infoLocal
        except:
            return None


def weatherNow(codigoLocal, nomeLocal):

    # Retornando o clima de uma localização:
    CurrentCondicionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" \
        + codigoLocal + "?apikey=" + accuweatherAPIKey \
        + "& language=pt-br"

    r = requests.get(CurrentCondicionsAPIUrl)
    # Validando a URL LocalizacionApiUrl
    if (r.status_code != 200):
        print('Não foi possivél obter a sua localização.')
        return None
    else:
        try:
            CurrentCondicionsResponse = json.loads(r.text)
            infoClima = {}
            infoClima['textoClima'] = CurrentCondicionsResponse[0]['WeatherText']
            infoClima['temperatura'] = CurrentCondicionsResponse[0]['Temperature']['Metric']['Value']
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None


def weatherPreviewFiveDays(codigoLocal):

    previewFiveDays = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
        + codigoLocal + "?apikey=" + accuweatherAPIKey \
        + "& language=pt-br"

    r = requests.get(previewFiveDays)

    if (r.status_code != 200):
        print('Não foi possivél retorna as previsões para os proximos 5 dias.')
        return None
    else:
        try:
            previewFiveDays = json.loads(r.text)
            for dia in previewFiveDays['DailyForencasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['maximum']['Value']
                climaDia['min'] = dia['Temperature']['minimum']['Value']
                climaDia['Clima'] = dia['Day']['IconPharse']
                diaSemana = diasSemana[int(date.fromtimestamp(
                    dia['EpochDate']).strftime('%w'))]
                climaDia['Dia semana'] = diasSemana[diaSemana]
                previewFiveDays.append(climaDia)
            return previewFiveDays
        except:

            return None

# Begin the System


def showPrevision(lat, long):
    try:
        local = takeCodeLocalizacion(lat, long)
        climaAtual = weatherNow(local['codigoLocal'], local['nomeLocal'])
        print('Clima atual em: ', climaAtual['nomeLocal'])
        print(climaAtual['textoClima'])
        print('Temperatura: ', str(climaAtual['temperatura']) + '\xb0' + 'C')
    except:
        print('Error ao obter o cilema atual')

    opcao = input(
        'Deseja ver a previsão para os proximos dias?(s/n): ').lowcase()

    if opcao == 's':

        try:
            print('\n Clima para hoje e os proximos 5 dias: \n')
            previewDays = weatherPreviewFiveDays(local['codigoLocal'])
            for dia in previewDays:
                print(dia['dia'])
                print('Minima para hoje: ', str(dia['min']), '\xb0', 'C')
                print('Maxima para hoje: ', str(dia['max ']), '\xb0', 'C')
                print('Clima no momento: ', (dia['clima']), '\xb0', 'C')
                print('-----------------------------------------')
        except:
            print('Erro ao obter a prevosão para os proximos dias.')


def searchLocation():

    _local = urllib.parse.quote(local)
    maxBoxGeoLocalizacion = "https://api.mapbox.com/geocoding/v5/mapbox.places/"\
        + _local + ".json?access_token=" + mapBox

    r = requests.get(maxBoxGeoLocalizacion)

    if (r.status_code != 200):
        print('Não foi possivel obter o clima atual.')
        return None
    else:
        try:
            MapboxResponse = json.loads(r.text)
            coodernadas = {}
            coodernadas['long'] = str(
                MapboxResponse['features'][0]['gemoetry']['coordinates'][0])
            coodernadas['lat'] = str(
                MapboxResponse['features'][0]['gemoetry']['coordinates'][1])
        except:
            print('Erro na pesquisa do local.')


try:
    coodernadas = takeCoordenations()
    showPrevision(coodernadas['lat'], coodernadas['long'])

    continuar = 's'

    while continuar == 's':
        continuar = input(
            'Deseja consultar a previsão de outro local?(s/n)').lower()
        if continuar != 's':
            break
        local = input('Digite a cidade e o estado: ')
        try:
            coodernadas = searchLocation(local)
            showPrevision(coodernadas['lat'], coodernadas['long'])
        except:
            print('Não foi possivél obter a previsão para este local.')

except:
    print('Erro ao processar a solicitação. Entre em contato com o suporte!')

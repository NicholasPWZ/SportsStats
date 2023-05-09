import requests
import json
from bs4 import BeautifulSoup as bs


header = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def informar_partida(url):

    html = requests.get(url, headers=header).text
    soup = bs(html, 'html.parser')
    nextdata = soup.find('script', id='__NEXT_DATA__').string
    json_data = json.loads(nextdata)
    num_event = json_data['props']['pageProps']['event']['id']
    season = json_data['props']['pageProps']['event']['season']['id']
    tournament = json_data['props']['pageProps']['event']['tournament']['uniqueTournament']['id']
    return num_event, season, tournament


def dados_evento(num):
    url = f'https://api.sofascore.com/api/v1/event/{num}'
    html = requests.get(url, headers=header)
    json_data = json.loads(html.text)
    event = json_data['event']
    torneio = event['tournament']['name']
    torneioslug = event['tournament']['slug']
    homeinfo = event['homeTeam']
    awayinfo = event['awayTeam']
    homename = homeinfo['name']
    awayname = awayinfo['name']
    homeslug = homeinfo['slug']
    homeid = homeinfo['id']
    awayslug = awayinfo['slug']
    awayid = awayinfo['id']
    country = event['tournament']['category']['name']
    try:
        referee_id = event['referee']['id']
        return torneio, homename, awayname, homeslug, homeid, awayslug, awayid, torneioslug, country ,referee_id
    except:
        return torneio, homename, awayname, homeslug, homeid, awayslug, awayid, torneioslug, country

def sequencias(num, home, away):
    url =f'https://api.sofascore.com/api/v1/event/{num}/team-streaks'
    html = requests.get(url,headers=header)
    json_data = json.loads(html.text)
    general = json_data['general']
    head2head = json_data['head2head']
    for i in general:
        nome_time = i['team']
        if nome_time == 'away':
            nome_time = away
        if nome_time == 'home':
            nome_time = home
        print(nome_time, i['name'],i['value'])
    print('-' * 10,'Head 2 Head', '-' * 10)
    
    for p in head2head:
        nome_time = p['team']
        if nome_time == 'away':
            nome_time = away
        if nome_time == 'home':
            nome_time = home
        print(nome_time, p['name'],p['value'])

def situacao(num):
    url = f'https://api.sofascore.com/api/v1/event/{num}/pregame-form'
    html = requests.get(url,headers=header)
    json_data = json.loads(html.text)
    try:
        home_posicao, home_pontos = json_data['homeTeam']['position'], json_data['homeTeam']['value']
        away_posicao, away_pontos = json_data['awayTeam']['position'], json_data['awayTeam']['value']
        home_last = json_data['homeTeam']['form']
        away_last = json_data['awayTeam']['form']
        print('Time mandante:','Posição:',home_posicao,'Com', home_pontos,'Pts', home_last,'\n','-'*10,'\n'
                 'Time visitante:','Posição:',away_posicao,'Com', away_pontos,'Pts', away_last)
    except:
        pass

def referee_last(id_juiz):
    
    url = f'https://api.sofascore.com/api/v1/referee/{id_juiz}/events/last/0'
    html = requests.get(url,headers=header)
    json_data = json.loads(html.text)
    keys = json_data['events']

    for i in keys:
                
        nome_torneio = i['tournament']['name']
        slug, custom_id = i['slug'], i['customId']
        time_casa = i['homeTeam']['name']
        time_away = i['awayTeam']['name']
        try:
            gols_casa = i['homeScore']['display']
            gols_away = i['awayScore']['display']
        except:
            continue
        print('-' * 15,'\n',nome_torneio,'||', time_casa, '-', gols_casa,'X',gols_away,'-', time_away, '\n')
        
        id_antigas = informar_partida(f'https://www.sofascore.com/{slug}/{custom_id}')


        url_antiga = f'https://api.sofascore.com/api/v1/event/{id_antigas[0]}/statistics'
        html = requests.get(url_antiga, headers=header)
        json_data_antiga = json.loads(html.text)
        try:
            stats = json_data_antiga['statistics']
        except:
            continue
        for x in stats[0]['groups']:
            for y in x['statisticsItems']:
                if y['name'] == 'Corner kicks' or y['name'] == 'Yellow cards'    :
                    print (y['name'],'-' ,time_casa,'-', y['home'], 'X', y['away'],'-', time_away)
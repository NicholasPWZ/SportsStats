import requests
import json
from bs4 import BeautifulSoup as bs
import event

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

def estatisticas(ide, torneio, season):
    url = f'https://api.sofascore.com/api/v1/team/{ide}/unique-tournament/{torneio}/season/{season}/statistics/overall'
    html = requests.get(url, headers=header)
    json_data = json.loads(html.text)
    try:
        statistics = json_data['statistics']
        partidas = statistics['matches']
        gols_favor = statistics['goalsScored']
        gols_contra = statistics['goalsConceded']
        fin_gol = statistics['shotsOnTarget']
        finalizacoes = statistics['shots']
        corners_favor = statistics['corners']
        amarelos = statistics['yellowCards']
        amarelos_adv = statistics['yellowCardsAgainst'] 
        corners_contra = statistics['cornersAgainst']
        impedimentos = statistics['offsides']
        impedimentos_adv = statistics['offsidesAgainst']
        print(f'{partidas} Partidas jogadas\n{gols_favor / partidas:.2f} Média de gols marcados\n{gols_contra / partidas:.2f} Média de gols cedidos\n{finalizacoes / partidas:.2f} Finalizações por jogo\n{fin_gol / partidas:.2f} Chutes a gol por jogo\n'
f'{corners_favor / partidas:.2f} Escanteios por jogo\n{corners_contra / partidas:.2f} Escanteios cedidos por jogo\n{(corners_favor / partidas) + (corners_contra / partidas):.2f} Escanteios na partida\n{amarelos / partidas:.2f} Cartões amarelos por jogo'
f'\n{amarelos_adv / partidas:.2f} Cartões amarelos do adversário por jogo\n{impedimentos / partidas:.2f} Impedimentos por jogo\n{impedimentos_adv / partidas:.2f} Impedimentos do adversário por jogo')
    except:
        pass

def player_stats(ide, torneio, season):
    url = f'https://api.sofascore.com/api/v1/team/{ide}/unique-tournament/{torneio}/season/{season}/top-players/overall'
    html = requests.get(url, headers=header)
    json_data = json.loads(html.text)
    try:
        keys = json_data['topPlayers']['yellowCards']
        for i in keys:
            print(f"{i['player']['name']} -  {i['statistics']['yellowCards']} cartões amarelos em {i['statistics']['appearances']} jogos\n"
                f"{int(i['statistics']['yellowCards']) / int(i['statistics']['appearances']):.2f} POR JOGO\n")
    except:
        pass
    try:
        print('-' * 15)
        keys = json_data['topPlayers']['goals']
        for i in keys:
            print(f"{i['player']['name']} -  {i['statistics']['goals']} gols em {i['statistics']['appearances']} jogos\n"
                f"{int(i['statistics']['goals']) / int(i['statistics']['appearances']):.2f} POR JOGO\n")
    except:
        pass
    try:
        print('-' * 15)
        keys = json_data['topPlayers']['assists']
        for i in keys:
            print(f"{i['player']['name']} -  {i['statistics']['assists']} assistências em {i['statistics']['appearances']} jogos\n"
                f"{int(i['statistics']['assists']) / int(i['statistics']['appearances']):.2f} POR JOGO\n")
    except:
        pass
    try:
        print('-' * 15)
        keys = json_data['topPlayers']['totalShots']
        for i in keys:
            print(f"{i['player']['name']} -  {i['statistics']['totalShots']} chutes em {i['statistics']['appearances']} jogos\n"
                f"{int(i['statistics']['totalShots']) / int(i['statistics']['appearances']):.2f} POR JOGO\n")
    except:
        pass
    try:
        print('-' * 15)
        keys = json_data['topPlayers']['shotsOnTarget']
        for i in keys:
            print(f"{i['player']['name']} -  {i['statistics']['shotsOnTarget']} chutes ao gol em {i['statistics']['appearances']} jogos\n"
                f"{int(i['statistics']['shotsOnTarget']) / int(i['statistics']['appearances']):.2f} POR JOGO\n")
    except:
        pass
                

def last_games(ide, name):
    url = f'https://api.sofascore.com/api/v1/team/{ide}/events/last/0'
    html = requests.get(url, headers=header)
    json_data = json.loads(html.text)
    try: 
        keys = json_data['events']
        gols_primeiro_soma, gols_soma, escanteios_soma, amarelos_soma, partidas_soma, chutes_soma, impedimentos_soma = 0, 0 ,0 ,0 ,0, 0, 0
        escanteios_menor, escanteios_maior, amarelos_menor, amarelos_maior, chutes_menor, chutes_maior, impedimentos_menor, impedimentos_maior = 100, 0, 100, 0, 100, 0, 100, 0
        partida_escanteios, partida_amarelos, partida_impedimentos, partida_chutes, vitorias, empates, derrotas, gols_feitos, gols_sofridos = 0, 0, 0 ,0, 0, 0, 0, 0, 0
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
            try:
                gols_casa_tempo = i['homeScore']['period1']
                gols_away_tempo = i['awayScore']['period1']
                gols_primeiro_soma += gols_casa_tempo + gols_away_tempo
                
            except:
                continue
            id_antigas = event.informar_partida(f'https://www.sofascore.com/{slug}/{custom_id}')
            url_antiga = f'https://api.sofascore.com/api/v1/event/{id_antigas[0]}/statistics'
            html = requests.get(url_antiga, headers=header)
            json_data_antiga = json.loads(html.text)
            try:
                stats = json_data_antiga['statistics']
            except:
                continue
            partidas_soma += 1
            #print('|' * 20)
            if time_casa == name:
                gols_feitos += gols_casa
                gols_sofridos += gols_away
                if gols_casa > gols_away:
                    vitorias += 1
                if gols_casa == gols_away:
                    empates += 1
                if gols_away > gols_casa:
                    derrotas += 1
            elif time_away == name:
                gols_feitos += gols_away
                gols_sofridos += gols_casa
                if gols_casa < gols_away:
                    vitorias += 1
                if gols_casa == gols_away:
                    empates += 1
                if gols_away < gols_casa:
                    derrotas += 1
            #print(nome_torneio,'||', time_casa, ':', gols_casa, time_away, ':', gols_away, '//','Primeiro tempo:', time_casa, gols_casa_tempo,' - ', time_away, gols_away_tempo )
            for x in stats[0]['groups']:
                for y in x['statisticsItems']:
                    if y['name'] == 'Corner kicks' or y['name'] == 'Yellow cards' or y['name'] == 'Total shots' or y['name'] == 'Offsides':
                        #print (y['name'],'-' ,time_casa,':', y['home'], time_away,':', y['away'])
                        if time_casa == name:
                            if y['name'] == 'Corner kicks':
                                partida_escanteios += 1
                                escanteios_soma += int(y['home'])
                                
                                if int(y['home']) < escanteios_menor:
                                    escanteios_menor = int(y['home'])
                                if int(y['home']) > escanteios_maior:
                                    escanteios_maior = int(y['home'])
                            
                            elif y['name'] == 'Yellow cards':
                                partida_amarelos += 1
                                amarelos_soma += int(y['home'])
                                
                                if int(y['home']) < amarelos_menor:
                                    amarelos_menor = int(y['home'])
                                if int(y['home']) > amarelos_maior:
                                    amarelos_maior = int(y['home'])

                            elif y['name'] == 'Total shots':
                                partida_chutes += 1
                                chutes_soma += int(y['home'])
                                
                                if int(y['home']) < chutes_menor:
                                    chutes_menor = int(y['home'])
                                if int(y['home']) > chutes_maior:
                                    chutes_maior = int(y['home'])

                            elif y['name'] == 'Offsides':
                                partida_impedimentos += 1
                                impedimentos_soma += int(y['home'])
                                
                                if int(y['home']) < impedimentos_menor:
                                    impedimentos_menor = int(y['home'])
                                if int(y['home']) > impedimentos_maior:
                                    impedimentos_maior = int(y['home'])

                        else:
                            if y['name'] == 'Corner kicks':
                                partida_escanteios += 1
                                escanteios_soma += int(y['away'])
                                
                                if int(y['away']) < escanteios_menor:
                                    escanteios_menor = int(y['away'])
                                if int(y['away']) > escanteios_maior:
                                    escanteios_maior = int(y['away'])
                            
                            elif y['name'] == 'Yellow cards':
                                partida_amarelos += 1
                                amarelos_soma += int(y['away'])
                                
                                if int(y['away']) < amarelos_menor:
                                    amarelos_menor = int(y['away'])
                                if int(y['away']) > amarelos_maior:
                                    amarelos_maior = int(y['away'])
                           
                            elif y['name'] == 'Total shots':
                                partida_chutes += 1
                                chutes_soma += int(y['away'])
                                
                                if int(y['away']) < chutes_menor:
                                    chutes_menor = int(y['away'])
                                if int(y['away']) > chutes_maior:
                                    chutes_maior = int(y['away'])
                            
                            elif y['name'] == 'Offsides':
                                partida_impedimentos += 1
                                impedimentos_soma += int(y['away'])
                                if int(y['away']) < impedimentos_menor:
                                    impedimentos_menor = int(y['away'])
                                if int(y['away']) > impedimentos_maior:
                                    impedimentos_maior = int(y['away'])
                    else:
                        continue
        gols_soma = gols_feitos + gols_sofridos
        print(f'{name} - Nas últimas {partidas_soma} Partidas -> escanteios: {escanteios_soma} / amarelos: {amarelos_soma} /  chutes: {chutes_soma} / impedimentos: {impedimentos_soma} '
        f'Com médias de: \n{escanteios_soma / partida_escanteios:.2f} Escanteios por jogo\n{amarelos_soma / partida_amarelos:.2f} Amarelos por jogo\n{chutes_soma / partida_chutes:.2f} Chutes por jogo\n{impedimentos_soma / partida_impedimentos:.2f} Impedimentos por jogo\n'
        f'Menores valores: Escanteios: {escanteios_menor} Amarelos: {amarelos_menor} Chutes: {chutes_menor} Impedimentos: {impedimentos_menor}\nMaiores valores: Escanteios: {escanteios_maior} Amarelos: {amarelos_maior} Chutes: {chutes_maior} Impedimentos: {impedimentos_maior}\n'
        f'{name} venceu {vitorias}, perdeu {derrotas} e empatou {empates} - Marcando {gols_feitos} gols e cedendo {gols_sofridos}\nMédia de gols na partida: {gols_soma / partidas_soma:.2f}\nMédia de gols no primeiro tempo da partida: {gols_primeiro_soma / partidas_soma:.2f}')
    except:
        pass


def ultimas_headtohead(url):
    html = requests.get(url, headers=header).text
    soup = bs(html, 'html.parser')
    nextdata = soup.find('script', id='__NEXT_DATA__').string
    json_data = json.loads(nextdata)
    hometeam = json_data['props']['pageProps']['event']['homeTeam']['name']
    awayteam = json_data['props']['pageProps']['event']['awayTeam']['name']
    identificador_custom = json_data['props']['pageProps']['event']['customId']
    url_l = f'https://api.sofascore.com/api/v1/event/{identificador_custom}/h2h/events'
    html = requests.get(url_l, headers=header)
    json_data = json.loads(html.text)
    vitorias_casa, vitorias_visitante, empates = 0, 0 ,0
    gols_totais, escanteios_totais, amarelos_totais, impedimentos_totais, chutes_totais= 0, 0, 0, 0, 0
    for i in json_data['events']:

        try:
            time_casa, gols_casa = i['homeTeam']['name'], i['homeScore']['display']
            time_fora, gols_fora = i['awayTeam']['name'], i['awayScore']['display']
            gols_totais += gols_casa + gols_fora
        except:
            continue
        if gols_casa > gols_fora:
            if time_casa == hometeam:
                vitorias_casa += 1
            else:
                vitorias_visitante += 1
        elif gols_casa < gols_fora:
            if time_fora == awayteam:
                vitorias_visitante += 1
            else:
                vitorias_casa += 1
        else:
            empates += 1

        fonte = requests.get(f"https://api.sofascore.com/api/v1/event/{i['id']}/statistics", headers=header)
        
        try:
            json_dict = json.loads(fonte.text)
            stats = json_dict['statistics']
        except:
            continue
        print(f"{time_casa}: {gols_casa} X {gols_fora}: {time_fora}")
        for x in stats[0]['groups']:
            for y in x['statisticsItems']:
                if y['name'] == 'Corner kicks'   :
                    print (f"{y['name']}---{time_casa} {y['home']} {time_fora} {y['away']}")
                    escanteios_totais += int(y['home'])
                    escanteios_totais += int(y['away'])

                if y['name'] == 'Yellow cards':
                    print (f"{y['name']}---{time_casa} {y['home']} {time_fora} {y['away']}")
                    amarelos_totais += int(y['home'])
                    amarelos_totais += int(y['away'])


                if y['name'] == 'Total shots':
                    print (f"{y['name']}---{time_casa} {y['home']} {time_fora} {y['away']}")
                    chutes_totais += int(y['home'])
                    chutes_totais += int(y['away'])


                if y['name'] == 'Offsides':
                    print (f"{y['name']}---{time_casa} {y['home']} {time_fora} {y['away']}")
                    impedimentos_totais += int(y['home'])
                    impedimentos_totais += int(y['away'])
        
        print('\n')
    print(f'{hometeam} venceu {vitorias_casa} || {awayteam} venceu {vitorias_visitante} || Empatou {empates} vezes\n'
          f'Médias no jogos de: \nEscanteios: {escanteios_totais/ (vitorias_casa + vitorias_visitante + empates):.2f}\nAmarelos: {amarelos_totais/ (vitorias_casa + vitorias_visitante + empates):.2f}\nImpedimentos: {impedimentos_totais/ (vitorias_casa + vitorias_visitante + empates):.2f}\nChutes: {chutes_totais/ (vitorias_casa + vitorias_visitante + empates):.2f}'
          f'\nGols: {gols_totais / (vitorias_casa + vitorias_visitante + empates):.2f}')
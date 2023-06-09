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
        cruzamentos = statistics['totalCrosses']
        cruzamentos_adv = statistics['crossesTotalAgainst']
        print(f'{partidas} Partidas jogadas\n{gols_favor / partidas:.2f} Média de gols marcados\n{gols_contra / partidas:.2f} Média de gols cedidos\n{finalizacoes / partidas:.2f} Finalizações por jogo\n{fin_gol / partidas:.2f} Chutes a gol por jogo\n'
f'{corners_favor / partidas:.2f} Escanteios por jogo\n{corners_contra / partidas:.2f} Escanteios cedidos por jogo\n{(corners_favor / partidas) + (corners_contra / partidas):.2f} Escanteios na partida\n{amarelos / partidas:.2f} Cartões amarelos por jogo'
f'\n{amarelos_adv / partidas:.2f} Cartões amarelos do adversário por jogo\n{impedimentos / partidas:.2f} Impedimentos por jogo\n{impedimentos_adv / partidas:.2f} Impedimentos do adversário por jogo'
f'\n{cruzamentos / partidas:.2f} Cruzamentos por jogo\n{cruzamentos_adv / partidas:.2f} Cruzamentos cedidos por jogo')
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
                

def last_games(ide, time, home):
    url = f'https://api.sofascore.com/api/v1/team/{ide}/events/last/0'
    html = requests.get(url, headers=header)
    json_data = json.loads(html.text)
    try: 
        keys = json_data['events']
        chute_block_casa, chutes_block_casa_cedidos,  chute_block_away, chute_block_away_cedidos, chutes_soma_casa, chutes_soma_casa_cedidos ,chutes_soma_away ,chutes_soma_away_cedidos = 0, 0, 0, 0, 0, 0, 0, 0
        partidas_cruz_casa, partidas_cruz_fora, partidas_casa, partidas_fora, gols_soma, escanteios_soma, amarelos_soma, partidas_soma, chutes_soma, impedimentos_soma = 0, 0 ,0 ,0 ,0, 0, 0, 0, 0, 0
        partida_cruzamentos,partida_escanteios, partida_amarelos, partida_impedimentos, partida_chutes_target, partida_chutes_block, vitorias, empates, derrotas, gols_feitos, gols_sofridos = 0, 0, 0 ,0, 0, 0, 0, 0, 0,0,0
        lista_escanteios, lista_gols, lista_amarelos,lista_escanteios_casa, lista_gols_casa, lista_escanteios_fora, lista_gols_fora,lista_gols_sofridos_casa, lista_gols_sofridos_fora  = [], [], [],[],[],[],[],[],[]
        lista_cruzamentos_favor, lista_cruzamentos_contra, lista_escanteios_casa_contra, lista_escanteios_fora_contra, lista_cruzamentos_casa_favor,lista_cruzamentos_casa_contra = [], [], [], [],[],[]
        lista_cruzamentos_fora_favor, lista_cruzamentos_fora_contra,  = [], []
        for i in keys:
            
            nome_torneio = i['tournament']['name']
            slug, custom_id = i['slug'], i['customId']
            time_casa = i['homeTeam']['name']
            time_away = i['awayTeam']['name']
            try:
                gols_casa = i['homeScore']['display']
                gols_away = i['awayScore']['display']
               
                if time_casa == time:
                    partidas_casa+=1
                    lista_gols_casa.append(int(gols_casa))
                    lista_gols_sofridos_casa.append(int(gols_away))
                    

                else:
                    partidas_fora+=1
                    lista_gols_fora.append(int(gols_away))
                    lista_gols_sofridos_fora.append(int(gols_casa))
                    
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
            if time_casa == time:
                gols_feitos += gols_casa
                gols_sofridos += gols_away
                if gols_casa > gols_away:
                    vitorias += 1
                if gols_casa == gols_away:
                    empates += 1
                if gols_away > gols_casa:
                    derrotas += 1
            elif time_away == time:
                gols_feitos += gols_away
                gols_sofridos += gols_casa
                if gols_casa < gols_away:
                    vitorias += 1
                if gols_casa == gols_away:
                    empates += 1
                if gols_away < gols_casa:
                    derrotas += 1
            lista_gols.append(int(gols_casa) + int(gols_away))
            #print('-' * 15,'\n',nome_torneio,'||', time_casa, '-', gols_casa,'X',gols_away,'-', time_away, '\n')
                    
            for x in stats[0]['groups']:
                for y in x['statisticsItems']:
                    if y['name'] == 'Corner kicks' or y['name'] == 'Yellow cards' or y['name'] == 'Shots on target' or y['name'] == 'Blocked shots' or y['name'] == 'Offsides' or y['name'] =='Crosses':
                        
                        #print (y['name'],'-' ,time_casa,'-', y['home'], 'X', y['away'],'-', time_away)
                        if y['name'] =='Crosses':
                            partida_cruzamentos += 1
                            numc = y['home'].split('/')
                            numc = numc[1].split('(')
                            numf = y['away'].split('/')
                            numf = numf[1].split('(')
                            if time_casa == time:
                                partidas_cruz_casa += 1                         
                                lista_cruzamentos_casa_favor.append(int(numc[0]))
                                lista_cruzamentos_casa_contra.append(int(numf[0]))
                                lista_cruzamentos_favor.append(int(numc[0]))
                                lista_cruzamentos_contra.append(int(numf[0]))
                            else:
                                partidas_cruz_fora += 1
                                lista_cruzamentos_fora_favor.append(int(numf[0]))
                                lista_cruzamentos_fora_contra.append(int(numc[0]))
                                lista_cruzamentos_favor.append(int(numf[0]))
                                lista_cruzamentos_contra.append(int(numc[0]))

                       
                        elif y['name'] == 'Corner kicks':
                            partida_escanteios += 1
                            if time_casa == time:
                                lista_escanteios_casa_contra.append(int(y['away']))
                                lista_escanteios_casa.append(int(y['home']))
                            else:
                                
                                lista_escanteios_fora.append(int(y['away']))
                                lista_escanteios_fora_contra.append(int(y['home']))
                            lista_escanteios.append(int(y['home']) + int(y['away']))
                                
                        elif y['name'] == 'Yellow cards':
                            partida_amarelos += 1
                            if time_casa == time:
                                amarelos_soma += int(y['home'])
                            else:
                                amarelos_soma += int(y['away'])
                            lista_amarelos.append(int(y['home']) + int(y['away']))
                                                    
                        elif y['name'] == 'Shots on target' :
                            partida_chutes_target += 1
                            if time_casa == time:
                                chutes_soma_casa += int(y['home'])
                                chutes_soma_casa_cedidos += int(y['away'])
                            else:
                                chutes_soma_away += int(y['away'])
                                chutes_soma_away_cedidos += int(y['home'])
                        elif y['name'] == 'Blocked shots':
                            partida_chutes_block += 1
                            if time_casa == time:
                                chute_block_casa += int(y['home'])
                                chutes_block_casa_cedidos += int(y['away'])
                            else:
                                chute_block_away += int(y['away'])
                                chute_block_away_cedidos += int(y['home'])
                                pass
                        elif y['name'] == 'Offsides':
                            partida_impedimentos += 1
                            if time_casa == time:
                                impedimentos_soma += int(y['home'])
                            else:
                                impedimentos_soma += int(y['away'])
                            
                        





                    else:
                        continue
    except:
        pass              
    gols_soma = gols_feitos + gols_sofridos
    print(f'\n{time} - Nas últimas {partidas_soma} Partidas \n'
    f'{time} venceu {vitorias}, perdeu {derrotas} e empatou {empates} - Marcando {gols_feitos} gols e cedendo {gols_sofridos}\nMédia de gols na partida: {gols_soma / partidas_soma:.2f}\n\nPartidas do time: {partidas_soma}\n '
    f'Lista de gols totais nas últimas partidas: {lista_gols}')
    
    try:
        soma_cruza_favor1, soma_cruza_contra1 = sum(lista_cruzamentos_favor), sum(lista_cruzamentos_contra)
        soma_esc_favor, soma_esc_contra = sum(lista_escanteios_casa) + sum(lista_escanteios_fora), sum(lista_escanteios_casa_contra) + sum(lista_escanteios_fora_contra)
        cruz_para_esc, cruz_para_esc_adv, media_esc_, media_esc_adv = soma_cruza_favor1 / soma_esc_favor , soma_cruza_contra1 / soma_esc_contra, float(soma_cruza_favor1 / partida_cruzamentos) / float(soma_cruza_favor1 / soma_esc_favor), float(soma_cruza_contra1 / partida_cruzamentos) / float(soma_cruza_contra1 / soma_esc_contra)
    except:
        pass
    
    
    
    try:
        print(f'Cruzamentos do time necessarios para um escanteio: {cruz_para_esc:.2f} ({soma_cruza_favor1 / partida_cruzamentos:.2f} Cruzamentos por jogo) -> {media_esc_:.2f}\n'
          f'Cruzamentos do ADVERSARIO necessarios para um escanteio: {cruz_para_esc_adv:.2f} ({soma_cruza_contra1 / partida_cruzamentos:.2f} Cruzamentos por jogo) -> {media_esc_adv:.2f}')
        
        
    except:
        pass
    
    
    
    x = 0.5
    for i in range(5):
        contador = lista_gols.count(x) + sum(1 for numero in lista_gols if numero > x)
        print(f'-> acima de {x} gols: {contador}')
        x += 1
 
    print('-' * 20)

    x = 6
    for i in range(9):
        contador =lista_escanteios.count(x) + sum(1 for numero in lista_escanteios if numero > x)
        print(f'-> acima de {x} escanteios: {(contador * 100) / partida_escanteios:.2f}% ({contador})')
        x += 1 
   
    print('-' * 20)

    x = 0
    for i in range(8):
        contador =lista_amarelos.count(x) + sum(1 for numero in lista_amarelos if numero > x)
        print(f'-> acima de {x} amarelos: {contador}')
        x += 1
    
    #print(f'Número de ESCANTEIOS nas ultimas partidas: {lista_escanteios}\nNúmero de GOLS nas ultimas partidas: {lista_gols}\nNúmero de CARTÕES AMARELOS nas ultimas partidas: {lista_amarelos}')
    
    
    if time == home:
        print(f'\nPartidas do time em casa: {partidas_casa}')
        #print(f'Número de ESCANTEIOS do time em casa: {lista_escanteios_casa}\nNúmero de GOLS do time em casa: {lista_gols_casa}\nNúmero de GOLS SOFRIDOS do time em casa: {lista_gols_sofridos_casa}')
        soma_cruza_favor, soma_cruza_contra = sum(lista_cruzamentos_casa_favor), sum(lista_cruzamentos_casa_contra)
        soma_esc_favor, soma_esc_contra = sum(lista_escanteios_casa) , sum(lista_escanteios_casa_contra)
        cruza_favor_media , cruza_contra_media =  soma_cruza_favor / partidas_cruz_casa, soma_cruza_contra / partidas_cruz_casa
        print(f'Escanteios a favor nos últimos home games: {lista_escanteios_casa}\nEscanteios a contra nos últimos home games: {lista_escanteios_casa_contra}\n'
        f'Gols a favor nos últimos home games: {lista_gols_casa}\nGols SOFRIDOS nos últimos home games: {lista_gols_sofridos_casa}')
        
        try:
            print(f'Cruzamentos do time necessarios para um escanteio: {soma_cruza_favor / soma_esc_favor:.2f} ({soma_cruza_favor / partidas_cruz_casa:.2f} Cruzamentos por jogo) -> {float(soma_cruza_favor / partidas_cruz_casa) / float(soma_cruza_favor / soma_esc_favor):.2f}\n'
            f'Cruzamentos do ADVERSARIO necessarios para um escanteio: {soma_cruza_contra / soma_esc_contra:.2f} ({soma_cruza_contra / partidas_cruz_casa:.2f} Cruzamentos por jogo) -> {float(soma_cruza_contra / partidas_cruz_casa) / float(soma_cruza_contra / soma_esc_contra):.2f}')
 
        except:
            pass
        print(f'Cruzamentos quando mandante: {lista_cruzamentos_casa_favor}\nCruzamentos SOFRIDOS quando mandante: {lista_cruzamentos_casa_contra}')

        
        print('\nGOLS MARCADOS:')
        x = 0.5
        for i in range(5):
            contador =lista_gols_casa.count(x) + sum(1 for numero in lista_gols_casa if numero > x)
            print(f'-> acima de {x} gols: {contador}')
            x += 1
        
        print('\nGOLS SOFRIDOS:')
        
        x = 0.5
        for i in range(5):        
            contador =lista_gols_sofridos_casa.count(x) + sum(1 for numero in lista_gols_sofridos_casa if numero > x)
            print(f'-> acima de {x} gols: {contador}')
            x+=1
        return cruza_favor_media, cruza_contra_media,( soma_cruza_favor / soma_esc_favor), (soma_cruza_contra / soma_esc_contra)
    
    else:       
        print(f'\nPartidas do time fora: {partidas_fora}')
        soma_cruza_favor, soma_cruza_contra = sum(lista_cruzamentos_fora_favor), sum(lista_cruzamentos_fora_contra)
        soma_esc_favor, soma_esc_contra = sum(lista_escanteios_fora) , sum(lista_escanteios_fora_contra)
        cruza_favor_media , cruza_contra_media =  soma_cruza_favor / partidas_cruz_casa, soma_cruza_contra / partidas_cruz_casa
        print(f'Escanteios a favor nos últimos away games: {lista_escanteios_fora}\nEscanteios a contra nos últimos home games: {lista_escanteios_fora_contra}\n'
        f'Gols a favor nos últimos away games: {lista_gols_fora}\nGols SOFRIDOS nos últimos away games: {lista_gols_sofridos_fora}')
       
        
        try:
            print(f'Cruzamentos do time necessarios para um escanteio: {soma_cruza_favor / soma_esc_favor:.2f} ({soma_cruza_favor / partidas_cruz_fora:.2f} Cruzamentos por jogo) -> {float(soma_cruza_favor / partidas_cruz_fora) / float(soma_cruza_favor / soma_esc_favor):.2f}\n'
          f'Cruzamentos do ADVERSARIO necessarios para um escanteio: {soma_cruza_contra / soma_esc_contra:.2f} ({soma_cruza_contra / partidas_cruz_fora:.2f} Cruzamentos por jogo) -> {float(soma_cruza_contra / partidas_cruz_fora) / float(soma_cruza_contra / soma_esc_contra):.2f}')  
        except:
          pass
        print(f'Cruzamentos quando away: {lista_cruzamentos_fora_favor}\nCruzamentos SOFRIDOS quando away: {lista_cruzamentos_fora_contra}')
        print('\nGOLS MARCADOS')
        
        x = 0.5
        for i in range(5):
            contador =lista_gols_fora.count(x) + sum(1 for numero in lista_gols_fora if numero > x)
            print(f'-> acima de {x} gols: {contador}')
            x+=1

        print('\nGOLS SOFRIDOS:')

        x = 0.5
        for i in range(5):
            contador =lista_gols_sofridos_fora.count(x) + sum(1 for numero in lista_gols_sofridos_fora if numero > x)
            print(f'-> acima de {x} gols: {contador}')
            x+=1
        return cruza_favor_media, cruza_contra_media, (soma_cruza_favor / soma_esc_favor), (soma_cruza_contra / soma_esc_contra)





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
    divisor_es, divisor_am, divisor_im, divisor_ch = 0, 0, 0, 0
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
        #print(f"{time_casa}: {gols_casa} X {gols_fora}: {time_fora}")
        for x in stats[0]['groups']:
            for y in x['statisticsItems']:
                if y['name'] == 'Corner kicks'   :
                    #print (f"{y['name']}---{time_casa} {y['home']} X {y['away']} {time_fora} ")
                    divisor_es += 1
                    escanteios_totais += int(y['home'])
                    escanteios_totais += int(y['away'])

                if y['name'] == 'Yellow cards':
                    #print (f"{y['name']}---{time_casa} {y['home']} X {y['away']} {time_fora} ")
                    divisor_am += 1
                    amarelos_totais += int(y['home'])
                    amarelos_totais += int(y['away'])


                if y['name'] == 'Total shots':
                    #print (f"{y['name']}---{time_casa} {y['home']} x {y['away']} {time_fora} ")
                    divisor_ch += 1
                    chutes_totais += int(y['home'])
                    chutes_totais += int(y['away'])


                if y['name'] == 'Offsides':
                    #print (f"{y['name']}---{time_casa} {y['home']} X {y['away']} {time_fora} ")
                    divisor_im +=1
                    impedimentos_totais += int(y['home'])
                    impedimentos_totais += int(y['away'])
        
        #print('\n')
    print(f'{hometeam} venceu {vitorias_casa} || {awayteam} venceu {vitorias_visitante} || Empatou {empates} vezes\n')
    
    try:
        print(      f'Médias nas partidas de: \nEscanteios: {escanteios_totais/ divisor_es:.2f}\nAmarelos: {amarelos_totais/ divisor_am:.2f}\nImpedimentos: {impedimentos_totais/ divisor_im:.2f}\nChutes: {chutes_totais/ divisor_ch:.2f}')
    except:
          pass 
    print(
        f'\nGols: {gols_totais / (vitorias_casa + vitorias_visitante + empates):.2f}')
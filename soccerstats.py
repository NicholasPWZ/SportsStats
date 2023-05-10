import requests
import re
from bs4 import BeautifulSoup as bs

def info_soccerstats(nomedotime, torneio, pais):
    url = get_url_match(nomedotime, torneio, pais)
    html = requests.get(url).text
    soup = bs(html, 'html.parser')
    list_tags = []
    tag_h2 = soup.find('h2', string='Corner statistics')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    tag_h2 = soup.find('h2', string='Goal statistics')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    tag_h2 = soup.find('h2', string='Scoring rates')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    tag_h2 = soup.find('h2', string='Goals scored / Goals conceded')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    tag_h2 = soup.find('h2', string='Match total goals')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    tag_h2 = soup.find('h2', string='Current Streaks & Sequences')
    if tag_h2 == None:
       pass
    else: 
        list_tags.append(tag_h2)
    
    

    for y in list_tags:

        empty = y.next_sibling
        tabela = empty.next_sibling
        nomes = tabela.find_all('font', {'style':'font-size:13px;font-weight:bold;'})
        homename = nomes[0].text
        awayname = nomes[1].text
        stats = {}
        stat = y.text
        stats[homename], stats[awayname] = {} , {}
        stats[homename][stat], stats[awayname][stat] = {}, {}
        empty = tabela.next_sibling
        data_table = empty.next_sibling
        keys = data_table.find_all('font', {'color' : '#fafafa' })
        dados_tags = data_table.find_all('td',{'width' : '13%'} )
        name_dados_tags = data_table.find_all('td',{'width' : '48%'})
        name_dados = []
        dados = []
        for i in name_dados_tags:
            x = i.text
            x = x.strip()
            if x == 'Stat':
                continue
            if x == 'SCORED + CONCEDED':
                continue
            if x == 'CURRENT SEQUENCES':
                continue
            if x == 'OPENING GOALS':
                continue
            if x == 'HALF-TIME LEAD':
                continue
            if x == 'MINUTES PER GAME SPENT...':
                continue
            if x == 'DEFENDING THE LEAD':
                continue
            if x == 'QUALIZING':
                continue
            if x == 'NON-CRUCIAL GOALS':
                continue
            name_dados.append(x)
        for i in dados_tags:
            x = i.text
            x = x.strip()
            dados.append(x)

        x = 0
        for i in range(4,len(dados),4):
            stats[homename][stat][name_dados[x]] = {}
            stats[awayname][stat][name_dados[x]] = {}

            stats[homename][stat][name_dados[x]][keys[0].text] = dados[i]
            stats[homename][stat][name_dados[x]][keys[1].text] = dados[i+1]
            stats[awayname][stat][name_dados[x]][keys[-1].text]=  dados[i+3]
            stats[awayname][stat][name_dados[x]][keys[-2].text] = dados[i+2]
            
            x+=1
        print('-'* 10,homename,'-'*10)
        for i in stats[homename]:
            for p in stats[homename][i].keys():
                print (f"{p} -- CASA: {stats[homename][i][p]['Home']} || TOTAL: {stats[homename][i][p]['Total']}\n")
                
        print('-'* 10,awayname,'-'*10)
        for i in stats[awayname]:
            for p in stats[awayname][i].keys():
                print (f"{p} -- FORA: {stats[awayname][i][p]['Away']} || TOTAL: {stats[awayname][i][p]['Total']}\n")

#link = input('Informe a partida SoccerStats: ')
#info_soccerstats(link)

def get_url_match(time, torneio, pais):
    
    pais = pais.lower()
    url = 'https://www.soccerstats.com/leagues.asp'
    html = requests.get(url).text
    soup = bs(html, 'html.parser')
    torneio = re.compile(pais)
    tag = soup.find('a', class_='vsmall', attrs={'href':torneio})
    href = tag['href']
    
    link_lastest = f'https://www.soccerstats.com/{href}'
    nome_time = re.compile(time)
    html = requests.get(link_lastest).text
    soup = bs(html, 'html.parser')
    tag_a_match = soup.find('a', attrs={'title':nome_time})
    slug_match = tag_a_match['href']

    url = f'https://www.soccerstats.com/{slug_match}'
    return url



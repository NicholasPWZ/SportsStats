import requests
from bs4 import BeautifulSoup as bs
import re
import json

def get_slug(slugtorneio, nometime):
    
    html = requests.get(f'https://www.thepunterspage.com/kickform/{slugtorneio}-matchday-tips/').text
    sp = bs(html, 'html.parser')
    pattern = re.compile(nometime)
    href = sp.find('a', attrs={'title':pattern}) 
    slug = href['href']
    return slug

def get_probs(slug):
    html = requests.get(f'https://www.thepunterspage.com{slug}').text
    soup = bs(html,'html.parser')

    insides = soup.find_all('div', class_='inside')
    insides = insides[:4]
    insides1 = insides[0], insides[-1]
    insides2 = insides[1], insides[2]

    for i in insides1 :
        valores = i.find_all(string = True)
        lista_valor = [p.strip() for p in valores]
        lista_valor1 = list(filter(bool, lista_valor))
        print('\n', lista_valor1[0])
        lista_valor1 = lista_valor1[1:]
        
        for p in range(0,len(lista_valor1),3):
            print(lista_valor1[p], lista_valor1[p+1], lista_valor1[p+2])
    for i in insides2:
        valores = i.find_all(string = True)
        lista_valor = [p.strip() for p in valores]        
        lista_valor1 = list(filter(bool, lista_valor))
        print('\n',lista_valor1[0])
        lista_valor1 = lista_valor1[1:]
        if len(lista_valor1)< 10:
            for p in range(0,len(lista_valor1),2):
                print(lista_valor1[p], lista_valor1[p+1])
        else:
            for p in range(0,len(lista_valor1),6):
                print(lista_valor1[p+4],':' ,lista_valor1[p], lista_valor1[p+1])
                print(lista_valor1[p+5],':', lista_valor1[p+2], lista_valor1[p+3])

def get_ocorrencies(slug):
    header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cache-control': 'max-age=1800',
    'cookie': ' _gid=GA1.2.1435488029.1683552214; _ga=GA1.2.1745249219.1683552214; _ga_D19B1RLLVS=GS1.1.1683571553.3.0.1683571557.56.0.0; _gat_UA-13171516-22=1',
    'referer': 'https://www.thepunterspage.com/kickform/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

    html = requests.get(f'https://www.thepunterspage.com{slug}').text
    soup = bs(html,'html.parser')
    link_tables_tags = soup.find_all('div', class_='col-lg-4 col-md-6')
    names_tag = soup.find_all('div', class_='col-lg-12')
    names = []
    for i in names_tag:
        names.append(i.find('span').string)
    link_tables =[]

    for i in link_tables_tags:
        iframe = i.find('iframe')
        link = iframe['src']
        link = link.split('?')
        link[0] = link[0].replace('https://www.adamchoi.co.uk/widget.html#/thepunterspage/', '')
        link1 = link[1].split('&')
        link1[1] = link1[1].replace('leagueid', 'leagueId')
        final_link = f'https://www.adamchoi.co.uk/scripts/data/json/scripts/getStatsTablesSecure.php?clflc=abc&stat={link[0]}&numMatches=All&minPercent=-1&getFixtures=false&{link1[0]}&matchesType=All&minPlayed=0&{link1[1]}'
        link_tables.append(final_link)




    p = 0
    for i in link_tables:
        y=1
        html = requests.get(i, headers=header).text
        soup = bs(html, 'html.parser').string
        try:
            soup = json.loads(soup)
        except:
            continue
        print('\n','*'*4,'-'*5,names[p],'-'*5,'*'*4)
        print('Jogos em que ocorreu / Jogos disputados','- -','Porcentagem dos jogos que aconteceu\n')
        teams = soup['Teams'][0]['teams']
        for x in teams:
            print(y,'-',x['teamName'],' - '*2,x['numMatches'],' - '*2,x['percent'],'%')
            y+=1


        
        p+=1

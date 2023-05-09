import event
import team
import punterspage
import soccerstats

link = input('Informe a partida Sofascore: ')
try:
    ids = event.informar_partida(link)
except:
    print('Insira url correta do confronto no site do sofascore: ')
id_partida, id_season, id_torneio = ids[0], ids[1], ids[2]

dados = event.dados_evento(id_partida)

torneio, hometeam, awayteam, homeslug, homeid, awayslug, awayid, torneioslug, country = dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8]
try:
    id_juiz = dados[9]
except:
    pass
if torneioslug == 'laliga':
    torneioslug = 'la-liga'
elif torneioslug == 'premierleague':
    torneioslug = 'premier-league'
try:
    slug_punterspage =  punterspage.get_slug(torneioslug, hometeam)
except:
    timecasa = hometeam[2:]
    try:
        slug_punterspage = punterspage.get_slug(torneioslug, timecasa)
    except:
        print('Partida não possui probabilidade no PuntersPage')
try:
    punterspage.get_probs(slug_punterspage)
    print('\n')
    punterspage.get_ocorrencies(slug_punterspage)
except:
    pass

print('\n')

try:
    soccerstats.info_soccerstats(hometeam, torneio, country)
except:
    timecasa = hometeam[2:]
    try:
        soccerstats.info_soccerstats(timecasa, torneio, country)
    except:
        if torneio == 'LaLiga':
            torneio = 'La Liga'
        try:
            soccerstats.info_soccerstats(hometeam, torneio, country)
        except:
            print('Partida não possui informações no site SoccerStats')

print('\n')

event.sequencias(id_partida, hometeam, awayteam)

print('\n')

print('-' * 10,hometeam,'-' * 10)

team.estatisticas(homeid,id_torneio,id_season)

print('\n')

print('-' * 10,awayteam,'-' * 10)

team.estatisticas(awayid,id_torneio,id_season)

print('-' * 5,'ÚLTIMOS CONFRONTOS' ,'-' * 5,'Jogos mais recentes primeiro')

team.ultimas_headtohead(link)

print('\n')

print('-' * 20,'ULTIMOS JOGOS','-' * 20)

print(hometeam, 'Jogos mais recentes por último')

team.last_games(homeid, hometeam)

print('-' * 20)

print(awayteam, 'Jogos mais recentes por último')

team.last_games(awayid, awayteam)

print('\n')

event.situacao(id_partida)

print('\n')
try:
    print('-'*7, 'Árbitro da partida', '-'*7)
    event.referee_last(id_juiz)
except:
    print('Sem informações sobre o árbitro')

decisao = input('Se deseja ver a estatística dos jogadores, digite "s":\n')
if decisao == 's' or decisao == 'S':
    print('-' * 20)

    team.player_stats(homeid,id_torneio,id_season)

    print('-' * 15, awayteam,'-' * 15)

    team.player_stats(awayid,id_torneio,id_season)

input('Digite enter para sair')
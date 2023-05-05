import event
import team
import punterspage


link = input('Informe a partida Sofascore: ')
try:
    ids = event.informar_partida(link)
except:
    print('Insira url correta do confronto no site do sofascore: ')
id_partida, id_season, id_torneio = ids[0], ids[1], ids[2]

dados = event.dados_evento(id_partida)

torneio, hometeam, awayteam, homeslug, homeid, awayslug, awayid, torneioslug = dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7]
if torneioslug == 'laliga':
    torneioslug = 'la-liga'
elif torneioslug == 'premierleague':
    torneioslug = 'premier-league'
try:
    punterspage.get_probs(punterspage.get_slug(torneioslug, hometeam))
except:
    timecasa = hometeam[2:]
    try:
        punterspage.get_probs(punterspage.get_slug(torneioslug, timecasa))
    except:
        print('Partida não possui probabilidade no PuntersPage')

print('\n')

event.sequencias(id_partida, hometeam, awayteam)

print('\n')

print('-' * 10,hometeam,'-' * 10)

team.estatisticas(homeid,id_torneio,id_season)

print('\n')

print('-' * 10,awayteam,'-' * 10)

team.estatisticas(awayid,id_torneio,id_season)

print('-' * 5,'ÚLTIMOS CONFRONTOS' ,'-' * 5)

team.ultimas_headtohead(link)

print('-' * 20)

team.player_stats(homeid,id_torneio,id_season)

print('-' * 15, awayteam,'-' * 15)

team.player_stats(awayid,id_torneio,id_season)

print('\n')

print('-' * 20,'ULTIMOS JOGOS','-' * 20)

print(hometeam)

team.last_games(homeid, hometeam)

print('-' * 20)

print(awayteam)

team.last_games(awayid, awayteam)

print('\n')

event.situacao(id_partida)

input('Digite enter para sair')
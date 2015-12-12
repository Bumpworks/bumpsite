from bump.models import Player, Game
import math
def isRanked(ranked_dict, player):
    return ranked_dict[player][0] >= 7 and ranked_dict[player][0] + ranked_dict[player][1] >= 15
def kFactor(elo):
    if elo < 1010:
        return 32
    if elo > 1100:
        return 16
    else:
        return 24
def record(ranked_dict_entry):
    return "("+str(ranked_dict_entry[0])+"-"+str(ranked_dict_entry[1])+")"
def saveRecords(ranked_dict):
    for player in ranked_dict.keys():
        player.wins = ranked_dict[player][0]
        player.losses = ranked_dict[player][1]
        player.save()
def saveElo(elo_dict):
    for player in elo_dict.keys():
        player.elo = int(elo_dict[player])
        player.save()
games = Game.objects.order_by('date').select_related('winner','loser')
players = Player.objects.all()
elo_dict = {}
ranked_dict = {}
for player in players:
    elo_dict[player] = 1000
    ranked_dict[player] = [0,0]
for game in games:
    ranked_dict[game.winner][0] += 1
    ranked_dict[game.loser][1] += 1
saveRecords(ranked_dict)
for game in games:
    if not isRanked(ranked_dict, game.winner) or not isRanked(ranked_dict, game.loser):
        continue
    winner_elo = elo_dict[game.winner]
    loser_elo = elo_dict[game.loser]
    expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
    delta = (1-expected_win_for_winner)
    elo_dict[game.winner] += delta * kFactor(winner_elo)
    elo_dict[game.loser] -= delta * kFactor(loser_elo)
saveElo(elo_dict)
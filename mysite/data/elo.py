from bump.models import Player, Game
import math
games = Game.objects.all()
players = Player.objects.all()
elo_dict = {}
ranked_dict = {}
for player in players:    elo_dict[player] = 1000
    ranked_dict = False
for game in games:    winner_elo = elo_dict[game.winner]    loser_elo = elo_dict[game.loser]    expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))    expected_win_for_loser = 1 - expected_win_for_winner
    k = 16    elo_dict[game.winner] += delta * expected_win_for_loser    elo_dict[game.loser] -= delta * expected_win_for_loser
print elo_dict
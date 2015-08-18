from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Player, Game
import math
from .forms import GameSubmissionForm


def index(request):
    feed_games = Game.objects.order_by('-date')[:20]
    return render(request,'bump/feed.html',{'games_feed':feed_games})

def submit_game(request):
    if request.method=='POST':
        form = GameSubmissionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            game_text = cd.get('game_text')
            games_details = game_text.split('\n')
            for detail in games_details:
                game = detail.split()
                winner = get_object_or_404(Player,name=game[0])
                loser = get_object_or_404(Player,name=game[1])
                game = Game(winner=winner,loser=loser)
                game.save()
            form = GameSubmissionForm()
    else:
        form = GameSubmissionForm()
    return render(request,'bump/game_submit.html',{'form':form})

    
def rankings(request):
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
        return "     ("+str(ranked_dict_entry[0])+"-"+str(ranked_dict_entry[1])+")"
    games = Game.objects.all()
    players = Player.objects.all()
    elo_dict = {}
    ranked_dict = {}
    for player in players:
        elo_dict[player] = 1000
        ranked_dict[player] = [0,0]
    for game in games:
        ranked_dict[game.winner][0] += 1
        ranked_dict[game.loser][1] += 1
    
    for game in games:
        if not isRanked(ranked_dict, game.winner) or not isRanked(ranked_dict, game.loser):
            continue
        winner_elo = elo_dict[game.winner]
        loser_elo = elo_dict[game.loser]
        expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
        delta = (1-expected_win_for_winner)
        elo_dict[game.winner] += delta * kFactor(winner_elo)
        elo_dict[game.loser] -= delta * kFactor(loser_elo)
    pruned_elo = [(key,value,record(ranked_dict[key])) for key,value in elo_dict.items() if value != 1000]
    sorted_elo = sorted(pruned_elo, key=lambda x: -x[1])
    return render(request, 'bump/rankings.html', {'elo_dict': sorted_elo})


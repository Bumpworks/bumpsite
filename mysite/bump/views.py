from django.shortcuts import render, get_object_or_404
from .models import Player, Game
import math
from .forms import GameSubmissionForm, UserForm, PlayerForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    feed_games = Game.objects.order_by('-date')[:20]
    return render(request,'bump/feed.html',{'games_feed':feed_games})

@login_required
def submit_game(request):
    if request.method=='POST':
        form = GameSubmissionForm(request.POST)
        if form.is_valid():
            game_recorder = None
            if request.user.is_authenticated():
                game_recorder = request.user
            cd = form.cleaned_data
            game_text = cd.get('game_text')
            date = cd.get('date')
            table = cd.get('table')
            games_details = game_text.split('\n')
            for detail in games_details:
                if len(detail)==0:
                    continue
                game = detail.split()
                winner = get_object_or_404(Player,identifier__iexact=game[0])
                current_index = 1
                try:
                    num_games = int(game[current_index])
                    current_index += 1
                except ValueError:
                    num_games = 1
                loser = get_object_or_404(Player,identifier__iexact=game[current_index])
                tags = game[current_index+1:]
                advantage = ''
                finisher = ''
                for i in range(len(tags)):
                    if tags[i] in Game.advantage_choices:
                        advantage = tags[i]
                    if tags[i] in Game.finisher_choices:
                        finisher = tags[i]
                for i in range(num_games):    
                    game = Game(winner=winner,loser=loser,advantage=advantage,finisher=finisher,table=table,date=date,recorder=game_recorder)
                    game.save()
            form = GameSubmissionForm()
    else:
        form = GameSubmissionForm()
    feed_games = Game.objects.order_by('-pk')[:20]
    return render(request,'bump/game_submit.html',{'form':form, 'feed':feed_games, 'players':Player.objects.all()})

    
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
        return "("+str(ranked_dict_entry[0])+"-"+str(ranked_dict_entry[1])+")"
    games = Game.objects.select_related('winner','loser')
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
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            player = cd.get('player')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            player.user = user
            player.save()
            
            
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request,
            'bump/register.html',
            {'user_form': user_form, 'registered': registered} )
def create_player(request):
    created = False
    if request.method == 'POST':
        player_form = PlayerForm(data=request.POST)
        if player_form.is_valid():
            cd = player_form.cleaned_data
            player = player_form.save()
            created = True
        else:
            print user_form.errors
    else:
        player_form = PlayerForm()
    return render(request,
            'bump/create_player.html',
            {'player_form': player_form, 'created': created} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bump/')
            else:
                return HttpResponse("Your Le Bump account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'bump/login.html', {})
from django.contrib.auth import logout

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/bump/')
    
def player_profile(request, player_name):
    player = get_object_or_404(Player, identifier=player_name)
    return render(request, 'bump/profile.html', {'player' : player})
    
def player_info(request):
    return render(request, 'bump/players.html', {'players' : Player.objects.order_by('first_name')})

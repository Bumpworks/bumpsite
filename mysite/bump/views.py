from django.shortcuts import render, get_object_or_404
from .models import Player, Game
import math
from .forms import GameSubmissionForm, UserForm, PlayerForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta



def index(request):
    ordered_games = Game.objects.order_by('-date')
    feed_games = ordered_games[:20]
    now = datetime.now()
    month_games = ordered_games.filter(date__lte = (now - timedelta(days = 7)))
    week_games = month_games.filter(date__lte = (now - timedelta(days = 30)))
    day_games = week_games.filter(date__lte = (now - timedelta(days=1)))
    hour_games = day_games.filter(date__lte = (now - timedelta(hours=1)))
    context = {
        'month_count' : month_games.count(),
        'week_count' : week_games.count(),
        'day_count' : day_games.count(),
        'hour_count' : hour_games.count(),
        'games_feed' : feed_games
    }
    return render(request,'bump/feed.html',context)

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
            return HttpResponseRedirect('')
    else:
        form = GameSubmissionForm()
    feed_games = Game.objects.order_by('-pk')[:15]
    return render(request,'bump/game_submit.html',{'form':form, 'feed':feed_games, 'players':Player.objects.all()})

    
def rankings(request):
    players = Player.objects.all().order_by('-elo')
    players = [x for x in players if x.ranked()]
    return render(request, 'bump/rankings.html', {'players': players})
    
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
            print player_form.errors
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
                return HttpResponseRedirect('/submit-game')
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
    return HttpResponseRedirect('/')
    
def player_profile(request, player_identifier):
    player = Player.objects.get(identifier=player_identifier)
    user = player.user
    return render(request, 'bump/profile.html', {'player_user':user,'player' : player})
  
def player_info(request):
    return render(request, 'bump/players.html', {'players' : Player.objects.order_by('first_name')})

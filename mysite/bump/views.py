from django.shortcuts import render, get_object_or_404
from .models import Player, Game
import math
from .forms import GameSubmissionForm, UserForm, PlayerForm, GameEditForm, RankingsSimulationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import logout
from .elo import eloRecords

def api_games(request):
    data = serializers.serialize("json", Game.objects.all())
    return HttpResponse(data, content_type='application/json')
def api_games_by(request, player):
    data = serializers.serialize("json", Game.objects.filter(Q(winner__identifier=player) | Q(loser__identifier=player)))
    return HttpResponse(data, content_type='application/json')
def api_games_between(request, player1, player2):
    players = [player1, player2]
    data = serializers.serialize("json", Game.objects.filter(winner__identifier__in=players, loser__identifier__in=players))
    return HttpResponse(data, content_type='application/json')
def api_players(request):
    data = serializers.serialize("json", Player.objects.all())
    return HttpResponse(data, content_type='application/json')
def index(request):
    ordered_games = Game.objects.order_by('-date','-pk')
    feed_games = ordered_games[:20]
    now = timezone.now()
    month_games = ordered_games.filter(date__gte = (now - timedelta(days = 30)))
    week_games = month_games.filter(date__gte = (now - timedelta(days = 7)))
    day_games = week_games.filter(date__gte = (now - timedelta(days=1)))
    hour_games = day_games.filter(date__gte = (now - timedelta(hours=1)))

    start_date = timezone.localtime(timezone.now()).date()
    end_date = start_date + timedelta( days=1 ) 
    games_today = Game.objects.filter(date__range=(start_date, end_date))
    def tupleify(playerA, playerB):
        if playerA < playerB:
            return (playerA,playerB),True
        else:
            return (playerB,playerA),False
    series_dict = {}
    for game in games_today:
        tuple,first_player_won = tupleify(game.winner.identifier,game.loser.identifier)
        if tuple not in series_dict.keys():
            series_dict[tuple] = [0,0]
        if first_player_won:
            series_dict[tuple][0]+=1
        else:
            series_dict[tuple][1]+=1
    series_tuples = sorted(series_dict.items(), key=lambda e: -e[1][0]-e[1][1])
    series_tuples = [x for x in series_tuples if x[1][0]+x[1][1] >= 2]
    context = {
        'month_count' : month_games.count(),
        'week_count' : week_games.count(),
        'day_count' : day_games.count(),
        'hour_count' : hour_games.count(),
        'player_count' : Player.objects.all().count(),
        'player_week' : Player.objects.filter(start_date__gte = (now - timedelta(days=7))).count(),
        'games_feed' : feed_games,
        'series_tuples' : series_tuples
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

@login_required
def recent_submitted_games(request):
    if request.user.is_authenticated():
        user = request.user
        recent_submitted_games = Game.objects.filter(date__gte= (timezone.now() - timedelta(minutes=20)),recorder=user).order_by('-date')
    return render(request,'bump/recent_submitted.html',{'recent_submitted_games' : recent_submitted_games})
def edit_game(request,game_pk):
    game = get_object_or_404(Game,pk=game_pk)
    if request.user.is_authenticated():
        user = request.user
        if game.recorder != user:
            return HttpResponse('You can not edit this game as you did not submit it.')
        if game.date < (timezone.now()-timedelta(minutes=20)):
            return HttpResponse('You submitted this game, but it is past 20 minutes since you submitted it, and as such cannot be editted. Contact an admin.')
        if request.method == 'POST':
            form = GameEditForm(data=request.POST, instance=game)
            if form.is_valid():
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/recent-submitted/')

                else:
                    print form.errors
        else:
            form = GameEditForm(instance=game)
    return render(request,'bump/edit_game.html',{'form':form, 'game':game})

def rankings(request):
    on_the_bump = Player.objects.filter(wins__lte = 15).order_by('-wins')
    on_the_bump = [x for x in on_the_bump if not x.ranked()]
    on_the_bump = on_the_bump[:10]
    players = Player.objects.all().order_by('-elo')
    players = [x for x in players if x.ranked()]
    
    return render(request, 'bump/rankings.html', {'players': players, 'on_the_bump' : on_the_bump})
def rankings_sim(request):
    player_elo_tuples = None
    if request.method == 'POST':
        form = RankingsSimulationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start = cd.get('start_date')
            end = cd.get('end_date')
            if start == None:
                start = '2000-01-01'
            if end == None:
                end = '2199-01-01'
            day = timezone.localtime(timezone.now())
            last_friday = day - timedelta(days=day.weekday()) + timedelta(days=4, weeks=-1)
            last_friday_at_five = last_friday.replace(hour=17, minute=0)
            if end > last_friday_at_five:
                end = last_friday_at_five
            table_booleans = [cd.get('brunswick_table'),cd.get('will_table'),cd.get('kaighn_table'),cd.get('adil_table'),cd.get('loop_table'),cd.get('rectangle_table')]
            active_players_only = cd.get('active_players_only')
            chosen_tables = [x for i,(x,y) in enumerate(Game.table_choices_tuples) if table_booleans[i]]
            all_games = Game.objects.all().select_related('winner','loser')
            games = all_games.filter(table__in=chosen_tables,date__lte=end,date__gte=start).order_by('date','pk')
            elo_dict,ranked_dict = eloRecords(games,games)
            def player_ranked(player):
                wins = ranked_dict[player][0]
                losses = ranked_dict[player][1]
                return wins >= 7 and wins+losses>=15
            ranked_players = [player for player in Player.objects.all() if player_ranked(player)]
            player_elo_tuples = [(player,elo_dict[player]) for player in ranked_players]
            player_elo_tuples = sorted(player_elo_tuples, key=lambda e: -e[1])
            player_elo_tuples = [(player,elo,ranked_dict[player][0],ranked_dict[player][1]) for player,elo in player_elo_tuples]
            if active_players_only:
                final_tuples = []
                for tuple in player_elo_tuples:
                    player,_,_,_ = tuple
                    date1 = Game.objects.filter(winner=player).order_by('-date')[0].date
                    date2 = Game.objects.filter(loser=player).order_by('-date')[0].date
                    last_game_date = date1 if date1 > date2 else date2
                    if (timezone.now() - last_game_date).days <= 30:
                        final_tuples.append(tuple) 
                player_elo_tuples = final_tuples
        else:
            print form.errors
    else:
        form = RankingsSimulationForm()
    return render(request, 'bump/rankings_sim.html', {'form': form, 'player_elo_tuples':player_elo_tuples})
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
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Le Bump account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'bump/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    
def player_profile(request, player_identifier):
    player = Player.objects.get(identifier__iexact=player_identifier)
    recent_games = Game.objects.filter(Q(winner__identifier__iexact = player_identifier) | Q(loser__identifier__iexact=player_identifier)).order_by('-date')[:20]
    user = player.user
    ranked_players = [p for p in Player.objects.all() if p.ranked()]
    def div(a,b):
        a = float(a)
        if b==0:
            return 'NaN'
        else:
            return a/b
    def get_finisher_stat(finisher,player,ranked_opponents=False,lose=False):
        if lose:
            if ranked_opponents:
                return Game.objects.filter(finisher=finisher,loser=player,winner__in=ranked_players).count()
            else:
                return Game.objects.filter(finisher=finisher,loser=player).count()
        else:
            if ranked_opponents:
                return Game.objects.filter(finisher=finisher,winner=player,loser__in=ranked_players).count()
            else:
                return Game.objects.filter(finisher=finisher,winner=player).count()
    def get_stats(games,player):
        whr = games.filter(advantage='hr',winner__in=player).count()
        wbr = games.filter(advantage='br',winner__in=player).count()
        whw = games.filter(advantage='hw',winner__in=player).count()
        wbw = games.filter(advantage='bw',winner__in=player).count()
        lhr = games.filter(advantage='hr',loser__in=player).count()
        lbr = games.filter(advantage='br',loser__in=player).count()
        lhw = games.filter(advantage='hw',loser__in=player).count()
        lbw = games.filter(advantage='bw',loser__in=player).count()
        win_totals = [whr,wbr,whw,wbw]
        lose_totals = [lhr,lbr,lhw,lbw]
        total_wins = whr+wbr+whw+wbw
        total_losses = lhr+lbr+lhw+lbw
        total_games = total_wins + total_losses
        win_percentages = [div(n,total_wins)*100 if total_wins!=0 else 'NaN' for n in win_totals]
        lose_percentages = [div(n,total_losses)*100 if total_losses!=0 else 'NaN' for n in lose_totals]
        player_stats = [div(whr+whw+lbr+lbw,total_games),div(whr+lbw,(whr+wbr+lhw+lbw)),div(whw+lbr,(whw+lbr+wbw+lhr)),div(whr,(whr+lbw)),div(whw,(whw+lbr)),div(wbr,(wbr+lhw)),div(wbw,(wbw+lhr))]
        player_stats = [n*100 if n!='NaN' else n for n in player_stats]
        return win_totals,lose_totals,win_percentages,lose_percentages,player_stats
    player_games = Game.objects.filter(Q(winner__identifier__iexact = player_identifier) | Q(loser__identifier__iexact=player_identifier)).exclude(advantage='')
    wt,lt,wp,lp,ps = get_stats(player_games,[player])
    rwt,rlt,rwp,rlp,rps = get_stats(player_games.filter(winner__in=ranked_players,loser__in=ranked_players),[player])
    _,_,_,_,average_stats = get_stats(Game.objects.exclude(advantage=''),Player.objects.all())
    finisher_stats = [(finisher_title,get_finisher_stat(finisher,player)) for finisher,finisher_title in Game.finisher_choices_tuples if finisher!='']
    rfinisher_stats = [(finisher_title,get_finisher_stat(finisher,player,ranked_opponents=True)) for finisher,finisher_title in Game.finisher_choices_tuples if finisher!='']
    lose_finisher_stats = [(finisher_title,get_finisher_stat(finisher,player,lose=True)) for finisher,finisher_title in Game.finisher_choices_tuples if finisher!='']
    rlose_finisher_stats = [(finisher_title,get_finisher_stat(finisher,player,lose=True,ranked_opponents=True)) for finisher,finisher_title in Game.finisher_choices_tuples if finisher!='']
    games_after_site_start = Game.objects.filter(date__gte=datetime(month=1,day=1,year=2016))
    print games_after_site_start.count()
    player_won_games_after_site_start = games_after_site_start.filter(winner=player)
    finisher_percentages = [div(count,player_won_games_after_site_start.count())*100 for _,count in finisher_stats]
    rfinisher_percentages = [div(count,player_won_games_after_site_start.count())*100 for _,count in rfinisher_stats]
    total_league_finisher = [games_after_site_start.filter(finisher=fin).count() for fin in Game.finisher_choices if fin!='']
    percentage_league_finisher = [div(n,games_after_site_start.count())*100 for n in total_league_finisher]
    context = {'player_user':user,'player' : player,'recent_games':recent_games,
    'win_totals':wt,'lose_totals':lt,'win_percentages':wp,'lose_percentages':lp,'player_stats':ps,
    'rwin_totals':rwt,'rlose_totals':rlt,'rwin_percentages':rwp,'rlose_percentages':rlp,'rplayer_stats':rps,
    'average_stats':average_stats, 'finisher_stats':finisher_stats,'rfinisher_stats':rfinisher_stats,
    'lose_finisher_stats':lose_finisher_stats,'rlose_finisher_stats':rlose_finisher_stats,
    'finisher_percentages':finisher_percentages,'rfinisher_percentages':rfinisher_percentages,
    'total_league_finisher':total_league_finisher,'percentage_league_finisher':percentage_league_finisher}
    return render(request, 'bump/profile.html', context)
  
def player_info(request):
    return render(request, 'bump/players.html', {'players' : Player.objects.order_by('first_name')})

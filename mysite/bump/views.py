from django.shortcuts import render
from django.http import HttpResponse
from .models import Player, Game

def index(request):
	return HttpResponse("Hello World, you're at the Le Bump Index Page")

def player_detail(request, name):
	response = "This is the page of %s with record %s"
	name = Player.objects.get(Player_text = name)
	record = str(name.get_record())
	return HttpResponse(response % (str(name), record))

def game_detail(request, game_num):
	game = Game.objects.get(pk = int(game_num))
	winner = game.winner
	loser = game.loser
	response = "Game %d, %s won the game, %s lost the game."
	return HttpResponse(response % (int(game_num), str(winner), str(loser)))


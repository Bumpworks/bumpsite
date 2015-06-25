from django.db import models

class Player(models.Model):
	Player_text = models.CharField(max_length = 60)
	date_joined = models.DateTimeField('Date Joined LeBump')
	competitors = models.ManyToManyField('self', blank = True)
	email = models.CharField(max_length = 60, default = '')
	phone = models.CharField(max_length = 60, default = '')

	def get_record(self):
		games_won = self.game_winner.all()
		games_lost = self.game_loser.all()
		return (len(games_won), len(games_lost))

	def __str__(self):
		return self.Player_text

class Game(models.Model):
	date = models.DateTimeField('Date Joined LeBump')
	winner = models.ForeignKey(Player, related_name = 'game_winner', default = 1)
	loser = models.ForeignKey(Player, related_name = 'game_loser', default = 2)
	comments = models.CharField(max_length = 500, default = '')
	bumpForGlory = models.BooleanField(default = False)
	sweep = models.BooleanField(default = False)

	def __str__(self):
		return str(self.winner) + ' over ' + str(self.loser)


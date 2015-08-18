from django.db import models
from django.utils import timezone

class Player(models.Model):
    name = models.CharField(default="",max_length = 30)
    
    def __unicode__(self):
        return self.name

class Game(models.Model):
	date = models.DateTimeField(default=timezone.now)
	winner = models.ForeignKey(Player, related_name = 'game_winner', default = 1)
	loser = models.ForeignKey(Player, related_name = 'game_loser', default = 2)

	def __unicode__(self):
		return str(self.winner) +' '+ str(self.loser)


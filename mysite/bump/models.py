from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length = 30)  
    user = models.OneToOneField(User, null=True)
    class_year = models.IntegerField(default=2016)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    duke = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name

class Game(models.Model):
    date = models.DateTimeField(default=timezone.now)
    winner = models.ForeignKey(Player, related_name = 'game_winner', default = 1)
    loser = models.ForeignKey(Player, related_name = 'game_loser', default = 2)
    advantage_choices_tuples = (
        ('', 'Not Specified'),
        ('bw', 'Break White'),
        ('br', 'Break Red'),
        ('hw', 'Hold White'),
        ('hr', 'Hold Red'),
        )
    advantage = models.CharField(choices=advantage_choices_tuples, max_length=2, default='')
    table_choices_tuples = (
        ('ty', 'Brunswick'),
        ('wi', 'Gray Table'),
        ('ka', 'Kaighn Table'),
        ('me', 'Mehul/Adil/Bryan Table'),
        ('lo', 'Loop Table'),
    )
    table = models.CharField(choices=table_choices_tuples, max_length=2,default='ty')
    finisher_choices_tuples = (
        ('', 'Normal'),
        ('bfg', 'Bump for Glory'),
        ('jfg', 'Jump for Glory'),
        ('nfg', 'New Age for Glory'),
        ('swe', 'Sweep'),
        )
    finisher = models.CharField(choices=finisher_choices_tuples, max_length=3,default='')
    advantage_choices = [choice[0] for choice in advantage_choices_tuples]
    finisher_choices = [choice[0] for choice in finisher_choices_tuples]

    def __unicode__(self):
        return str(self.winner) +' '+ str(self.loser)


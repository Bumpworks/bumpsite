from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Player(models.Model):
    identifier = models.CharField(max_length = 30)  
    user = models.OneToOneField(User, null=True, blank = True)
    class_year = models.IntegerField()
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    duke = models.BooleanField(default=True)
    netid = models.CharField(max_length = 7, null = True, blank = True)
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)
    elo = models.IntegerField(default=1000, blank=True)
    
    def ranked(self):
        return self.wins >= 7 and self.wins + self.losses >= 15
    def __unicode__(self):
        return self.identifier

class Game(models.Model):
    date = models.DateTimeField(default=timezone.now)
    winner = models.ForeignKey(Player, related_name = 'game_winner', default = 1)
    loser = models.ForeignKey(Player, related_name = 'game_loser', default = 2)
    recorder = models.ForeignKey(User)
    advantage_choices_tuples = (
        ('', 'Not Specified'),
        ('bw', 'Break White'),
        ('br', 'Break Red'),
        ('hw', 'Hold White'),
        ('hr', 'Hold Red'),
        )
    advantage = models.CharField(choices=advantage_choices_tuples, max_length=2, default='', blank=True)
    table_choices_tuples = (
        ('ty', 'Brunswick'),
        ('wi', 'Gray Table'),
        ('ka', 'Kaighn Table'),
        ('me', 'Mehul/Adil/Bryan Table'),
        ('lo', 'Loop Table'),
        ('re', 'Rectangle Table'),
    )
    table = models.CharField(choices=table_choices_tuples, max_length=2,default='ty')
    finisher_choices_tuples = (
        ('', 'Normal'),
        ('bfg', 'Bump for Glory'),
        ('jfg', 'Jump for Glory'),
        ('nfg', 'New Age for Glory'),
        ('sweep', 'Sweep'),
        )
    finisher = models.CharField(choices=finisher_choices_tuples, max_length=5,default='',blank=True)
    advantage_choices = [choice[0] for choice in advantage_choices_tuples]
    finisher_choices = [choice[0] for choice in finisher_choices_tuples]
    

    def __unicode__(self):
        finisher_string = ''
        if self.finisher != '':
            finisher_string = self.finisher
        table_string = ''
        if self.table != 'ty':
            table = [y for x,y in self.table_choices_tuples if x == self.table]
            table_string = '('+table[0]+')'
        return str(self.winner) +' '+ str(self.loser)+' '+self.advantage+' '+finisher_string+' '+table_string


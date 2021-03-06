from django import forms
from .models import Player, Game
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('identifier', 'first_name','last_name','duke','class_year','netid')
    def clean(self):
        cd = self.cleaned_data
        id = cd.get('identifier')
        if Player.objects.filter(identifier__iexact=id).exists():
            raise ValidationError('You tried to create a player with identifier '+id+', but that player already exists (case insensitive). Dingus!')
        return cd
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    player = forms.ModelChoiceField(queryset=Player.objects.order_by("identifier").filter(user=None))

    class Meta:
        model = User
        fields = ('username','email', 'password')

class GameEditForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('table','advantage','finisher')
    def clean(self):
        cd = self.cleaned_data
        ad = cd.get('advantage')
        fi = cd.get('finisher')
        if len(ad) > 0:
            if ad[0] == 'b':
                if fi == 'sweep':
                    raise ValidationError('You cannot sweep and break, dingus!')
        return cd
        
class RankingsSimulationForm(forms.Form):
    start_date = forms.SplitDateTimeField(input_time_formats=['%I:%M%p'], input_date_formats=['%m/%d/%y'],required=False,widget=forms.SplitDateTimeWidget(date_format='%m/%d/%y',time_format='%I:%M%p'),initial=datetime(2014, 8, 24, 0, 0))
    end_date = forms.SplitDateTimeField(input_time_formats=['%I:%M%p'], input_date_formats=['%m/%d/%y'],required=False,widget=forms.SplitDateTimeWidget(date_format='%m/%d/%y',time_format='%I:%M%p'),initial=datetime(2016, 12, 31, 17, 0))
    brunswick_table = forms.BooleanField(initial=True,required=False)
    will_table = forms.BooleanField(initial=True,required=False)
    kaighn_table = forms.BooleanField(initial=True,required=False)
    adil_table = forms.BooleanField(initial=True,required=False)
    loop_table = forms.BooleanField(initial=True,required=False)
    rectangle_table = forms.BooleanField(required=False)
    active_players_only = forms.BooleanField(required=False)
class GameSubmissionForm(forms.Form):
    date = forms.DateTimeField(widget=forms.SplitDateTimeWidget, required=False)
    table = forms.ChoiceField(choices=Game.table_choices_tuples)
    game_text = forms.CharField(widget=forms.Textarea)
    
    def clean(self):
        cd = self.cleaned_data
        text = cd.get('game_text')
        date = cd.get('date')
        if date is None:
            cd['date'] = timezone.now()
        if text is None:
            raise ValidationError('You\'ve entered nothing. Dingus!')
        games = [s.strip() for s in text.splitlines()]
        for game in games:
            gt = game.split()
            if len(gt) < 2:
                raise ValidationError("You need to specify a winner and loser.")
            winner = gt[0]
            if not Player.objects.filter(identifier__iexact=winner).exists():
                raise ValidationError(winner + " is not a registered player.")
            try:
                num_games = int(gt[1])
                if num_games < 1:
                    raise ValidationError("Please enter a positive number of games. Not "+str(num_games))
                if num_games > 5:
                    raise ValidationError("You can only enter 5 games, dingus. Not "+str(num_games))
                loser = gt[2]
                cut_index = 3
            except ValueError:
                loser = gt[1]
                cut_index = 2
            if not Player.objects.filter(identifier__iexact=loser).exists():
                raise ValidationError(loser+" is not a registered player.")
            if winner == loser:
                raise ValidationError(winner + " cannot beat themself, silly.")
            tags = gt[cut_index:]
            finisher_selected = False
            advantage_selected = False
            bbreak = False
            sweep = False
            for tag in tags:
                if tag in Game.advantage_choices:
                    if tag[0] == 'b':
                        bbreak = True
                    if advantage_selected:
                        raise ValidationError(tag + " is the second advantage codeword in a line. You can only have one.")
                    advantage_selected = True
                elif tag in Game.finisher_choices:
                    if tag == 'sweep':
                        sweep = True
                    if finisher_selected:
                        raise ValidationError(tag + " is the second finisher codeword in a line. You can only have one.")
                    finisher_selected = True
                else:
                    raise ValidationError(tag+" is not a valid word.")
            if bbreak and sweep:
                raise ValidationError('It\'s impossible to break AND sweep, ya dingus.')
                
            
        return cd
        
        
        

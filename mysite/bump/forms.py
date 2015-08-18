from django import forms
from .models import Player, Game
from django.core.exceptions import ValidationError



class GameSubmissionForm(forms.Form):
    game_text = forms.CharField(widget=forms.Textarea)
    
    def clean(self):
        cd = self.cleaned_data
        if len(cd) == 0:
            raise ValidationError('You\'ve entered nothing. Dingus!')
        text = cd['game_text']
        games = [s.strip() for s in text.splitlines()]
        for game in games:
            gt = game.split()
            if len(gt) < 2:
                raise ValidationError("You need to specify a winner and loser.")
            winner = gt[0]
            loser = gt[1]
            if not Player.objects.filter(name=winner).exists():
                raise ValidationError("The winner is not a registered player.")
            if not Player.objects.filter(name=loser).exists():
                raise ValidationError("The loser is not a registered player.")
            if winner == loser:
                raise ValidationError("You can't beat yourself, silly.")
        return cd
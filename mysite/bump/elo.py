from bump.models import Player, Game
import math
import operator

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
def saveRecords(ranked_dict):
    for player in ranked_dict.keys():
        player.wins = ranked_dict[player][0]
        player.losses = ranked_dict[player][1]
        player.save()
def saveElo(elo_dict):
    for player in elo_dict.keys():
        player.elo = int(elo_dict[player])
        player.save()
def getGames():
    games = Game.objects.order_by('date','pk').select_related('winner','loser')
    return games
def getDicts():
    players = Player.objects.all()
    elo_dict = {}
    ranked_dict = {}
    for player in players:
        elo_dict[player] = 1000
        ranked_dict[player] = [0,0]
    return ranked_dict, elo_dict
def recordAgainst(player1,player2):
    return len(Game.objects.filter(winner=player1,loser=player2)),len(Game.objects.filter(winner=player2,loser=player1))
def rankedDict(ranked_dict, games):    
    for game in games:
        ranked_dict[game.winner][0] += 1
        ranked_dict[game.loser][1] += 1
def eloDict(elo_dict, ranked_dict, games):
    for game in games:
        if not isRanked(ranked_dict, game.winner) or not isRanked(ranked_dict, game.loser):
            continue
        winner_elo = elo_dict[game.winner]
        loser_elo = elo_dict[game.loser]
        expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
        delta = (1-expected_win_for_winner)
        elo_dict[game.winner] += delta * kFactor(winner_elo)
        elo_dict[game.loser] -= delta * kFactor(loser_elo)
class SgoatCalculator(object):
    def __init__(self,current_date,future_date):
        self.ranked_dict, self.elo_dict = getDicts()
        rankedDict(self.ranked_dict,getGames())
        self.current_date = current_date
        self.future_date = future_date
        self.place_history = {}
        self.first = True
    def eloDict(self):
        if self.first:
            self.first = False
            games = Game.objects.filter(date__lte=self.future_date).order_by('date','pk').select_related('winner','loser')
        else:
            games = Game.objects.filter(date__lte=self.future_date).filter(date__gte=self.current_date).order_by('date','pk').select_related('winner','loser')
        for game in games:
            if not isRanked(self.ranked_dict, game.winner) or not isRanked(self.ranked_dict, game.loser):
                continue
            winner_elo = self.elo_dict[game.winner]
            loser_elo = self.elo_dict[game.loser]
            expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
            delta = (1-expected_win_for_winner)
            self.elo_dict[game.winner] += delta * kFactor(winner_elo)
            self.elo_dict[game.loser] -= delta * kFactor(loser_elo)
    def recordPlace(self,place_number):
        player,elo = sorted(self.elo_dict.items(), key=operator.itemgetter(1), reverse=True)[place_number-1]
        if player not in self.place_history.keys():
            self.place_history[player] = 1
        else:
            self.place_history[player] += 1
    def updateDate(self,tdelta):
        self.current_date += tdelta
        self.future_date += tdelta
def eloRecords(elo_games,record_games):
    ranked_dict, elo_dict = getDicts()
    rankedDict(ranked_dict, record_games)
    eloDict(elo_dict,ranked_dict,elo_games)
    return elo_dict, ranked_dict
if __name__ == '__main__':
    games = getGames()
    elo_dict, ranked_dict = eloRecords(games,games)
    saveRecords(ranked_dict)
    saveElo(elo_dict)

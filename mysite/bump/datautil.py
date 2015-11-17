from .models import Player, Game
import math

class DataManager(object):    
    def getPlayerRecords(self):
        if self.player_records != None:
            return self.player_records
        players = Player.objects.all()
        games = Game.objects.select_related('winner','loser')
        record_dict = {}
        for player in players:
            record_dict[player] = [0,0]
        for game in games:
            record_dict[game.winner][0] += 1
            record_dict[game.loser][1] += 1
        self.player_records = record_dict
        return record_dict
    def getPlayerElos(self):
        if self.player_elos != None:
            return self.player_elos
        elo_dict = {p : 1000 for p in Player.objects.all()}
        records = self.getPlayerRecords()
        games = Game.objects.select_related('winner','loser')
        for game in games:
            print game
            if not isRanked(records[game.winner]) or not isRanked(records[game.loser]):
                continue
            winner_elo = elo_dict[game.winner]
            loser_elo = elo_dict[game.loser]
            expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
            delta = (1-expected_win_for_winner)
            elo_dict[game.winner] += delta * kFactor(winner_elo)
            elo_dict[game.loser] -= delta * kFactor(loser_elo)
        self.player_elos = elo_dict
        return elo_dict
        
    
    




def playerRecords():
    players = Player.objects.all()
    games = Game.objects.select_related('winner','loser')
    record_dict = {}
    for player in players:
        record_dict[player] = [0,0]
    for game in games:
        record_dict[game.winner][0] += 1
        record_dict[game.loser][1] += 1
    return record_dict
def isRanked(player_record):
    return player_record[0] >= 7 and player_record[0] + player_record[1] >= 15
def playerElos():
    elo_dict = {p : 1000 for p in Player.objects.all()}
    records = playerRecords()
    games = Game.objects.select_related('winner','loser')
    for game in games:
        print game
        if not isRanked(records[game.winner]) or not isRanked(records[game.loser]):
            continue
        winner_elo = elo_dict[game.winner]
        loser_elo = elo_dict[game.loser]
        expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
        delta = (1-expected_win_for_winner)
        elo_dict[game.winner] += delta * kFactor(winner_elo)
        elo_dict[game.loser] -= delta * kFactor(loser_elo)
    return elo_dict
def kFactor(elo):
    if elo < 1010:
        return 32
    if elo > 1100:
        return 16
    else:
        return 24
def recordString(player_record):
    return "("+str(player_record[0])+"-"+str(player_record[1])+")"
def pruneSortElo(elo_dict, record_dict):
    pruned_elo = [(key,value,recordString(ranked_dict[key])) for key,value in elo_dict.items() if value != 1000]
    sorted_elo = sorted(pruned_elo, key=lambda x: -x[1])
    return sorted_elo

def rankings(request):



    games = Game.objects.select_related('winner','loser')
    players = Player.objects.all()
    elo_dict = {}
    ranked_dict = {}
    print '1'
    for player in players:
        elo_dict[player] = 1000
        ranked_dict[player] = [0,0]
    print '2'
    a = 0
    for game in games:
        ranked_dict[game.winner][0] += 1
        ranked_dict[game.loser][1] += 1
    print '3'
    for game in games:
        if not isRanked(ranked_dict[game.winner) or not isRanked(ranked_dict, game.loser):
            continue
        winner_elo = elo_dict[game.winner]
        loser_elo = elo_dict[game.loser]
        expected_win_for_winner = 1/(1+math.pow(10,(loser_elo-winner_elo)/400))
        delta = (1-expected_win_for_winner)
        elo_dict[game.winner] += delta * kFactor(winner_elo)
        elo_dict[game.loser] -= delta * kFactor(loser_elo)
    print '4'
    pruned_elo = [(key,value,record(ranked_dict[key])) for key,value in elo_dict.items() if value != 1000]
    sorted_elo = sorted(pruned_elo, key=lambda x: -x[1])
    print '5'
    return render(request, 'bump/rankings.html', {'elo_dict': sorted_elo})
'''

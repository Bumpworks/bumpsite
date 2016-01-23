class SingleGame(object):
    def __init__(self,game,start_date=None,end_date=None,fin_list=None,ad_list=None,winner_list=None,loser_list=None,table_list=None):
        self.game = game
        self.start_date = start_date
        self.end_date = end_date
        self.fin_list = fin_list
        self.ad_list = ad_list
        self.winner_list = winner_list
        self.loser_list = loser_list
        self.table_list = table_list
    def att_in_list(self,att,list):
        return not list or att in list
    def eval(self):
        if self.start_date and self.game.date < self.start_date:
            return False
        if self.end_date and self.game.date > self.end_date:
            return False
        if not self.att_in_list(self.game.finisher,self.fin_list) or not self.att_in_list(self.game.advantage,self.ad_list) or not self.att_in_list(self.game.winner,self.winner_list) or not self.att_in_list(self.game.loser,self.loser_list) or not self.att_in_list(self.game.table,self.table_list):
            return False
        return True
class MultiGame(object):
    def __init__(self,games,ordered=False,consecutive=False,*achievements):
        self.games = games
        self.ordered = ordered
        self.achievements = achievements
    def eval(self):
        if len(achievements)==0:
            return True
        if ordered:
            index = 0
            for game in self.games:
                if achievements[index].eval(game):
                    index+=1
                    if index == len(achievements):
                        return True
            return False
        else:
            achievements_completed = {ach : False for ach in achievements}
            for game in self.games:
                for achievement in achievements:
                    if not achievements_completed[achievement] and achievement.eval():
                        achievements_completed[achievement] = True
            return all([bool for ach,bool in achievements_completed])
            
        
    

class TestAchievement(object):
    name = "Test1"
    category="sg"
    description = "Sweep an opponent"
    points = 30
    def evaluate(self,player,game):
        return SingleGame(game,winner_list=[player],fin_list=['sweep']).eval()
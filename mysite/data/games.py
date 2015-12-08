from django.utils import timezone
from bump.models import Player, Game
from django.contrib.auth.models import User

def parse(file,table_name):
    mFile=open(file,'r')
    currentDate="replace"
    for line in mFile:
        data=line.split(',');
        if (len(data[2])>1 and data[2]!=currentDate):
            currentDate=data[2] # Update current date
        name=data[0].strip()
        if len(name) == 0:
            continue
        if (len(name.split(" "))>1):
            repeat=int(name.split(" ")[1])
            for i in range(repeat):
                addData(data[0].split(" ")[0],currentDate, data[1], table_name)
        else:
            addData(data[0].split(" ")[0],currentDate, data[1], table_name)
    mFile.close()
		
def addData(namey, date,opponent, table_name):
    date = date.strip()
    array = date.split('/')
    datey = array[2]+'-'+array[0]+'-'+array[1]
    g = Game(winner=Player.objects.get(identifier=namey), loser=Player.objects.get(identifier=opponent), date=datey, table = table_name, recorder=User.objects.all()[0])
    g.save()
    
parse('data/bp-site-brunswick.csv','ty')
parse('data/bp-site-gray.csv','wi')
parse('data/bp-site-mehul.csv','me')
parse('data/bp-site-rectangle.csv','re')
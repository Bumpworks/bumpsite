from django.utils import timezone
from .models import Player, Game
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
                addData(data[0].split(" ")[0],currentDate, data[1])
        else:
            addData(data[0].split(" ")[0],currentDate, data[1])
    mFile.close()
		
def addData(namey, date,opponent):
    date = date.strip()
    array = date.split('/')
    datey = array[2]+'-'+array[0]+'-'+array[1]
    g = Game(winner=Player.objects.get(name=namey), loser=Player.objects.get(name=opponent), date=datey)
    g.save()
    
parse('bp-site-brunswick.csv','ty')
parse('bp-site-gray.csv','wi')
parse('bp-site-mehul.csv','me')
parse('bp-site-rectangle.csv','re')
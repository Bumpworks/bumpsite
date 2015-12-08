from django.utils import timezone
from bump.models import Player
def parse(file):
    mFile=open(file,'r')
    for row in mFile:
        if len(row)==5:
            continue
        line = row.split(',')
        d = True
        if len(line[4])>1:
            d = False
        cy = int("20"+line[3])

        p = Player(identifier=line[0],class_year=cy,first_name=line[1],last_name=line[2],duke=d)
        p.save()
    mFile.close()
    
parse('data/bp-site-playerinfo.csv')
from django.conf import settings
import importlib
from django.db.models.aggregates import Sum
from .models import Achievement, AchievementRecord
import achievements
import inspect

def make_achievements():
    clses = [cls for name, cls in inspect.getmembers(achievements) if inspect.isclass(cls) and name.endswith('Achievement')]
    for cl in clses:
        register_achievement(cl)
        '''
            errors = check_achievement_class(cl)
            if errors:
                message = "Achievement class '%s' in '%s' has missing attributes : %s" % (cl.__name__, module.__name__, ",".join(errors))
                    raise ImproperlyConfigured(message)
                else:
                    engine.register_achievement(cl)
            
            except ImproperlyConfigured:
                raise
            except Exception, exc:
                logger.error("Exception catched while trying to register achievements class %s " % exc)
                raise ImproperlyConfigured("ACHIEVEMENT_CLASSES attribute must be set properly for them to be loaded into the engine : %s" % exc)
        '''
        
def register_achievement(cls,update=False):
    (obj, created) = Achievement.objects.get_or_create(name=cls.name,  defaults={
        'description': cls.description,
        'category': cls.category,
        'points': cls.points,
        'callback': construct_callback(cls)})
    if created:
        print cls,' achievement created!'
    if not created and update:
        obj.name = cls.name
        obj.description = cls.description
        obj.category = cls.category
        obj.bonus = cls.bonus
        obj.callback = construct_callback(cls)
        obj.save()
        print cls,' achievement updated!'

def construct_callback(cls):
    return "%s.%s" % (cls.__module__, cls.__name__)
    
def check_achievements(game):
    for ach in Achievement.objects.all():
        for player in [game.winner,game.loser]:
            if evaluate_achievement_callback(player, game,ach):
                (ach_record, created) = AchievementRecord.objects.get_or_create(achievement=ach, player=player)
def evaluate_achievement_callback(player, game,obj):
    achievement = get_callback_object(obj.callback)
    return achievement().evaluate(player,game)   
def get_callback_object(ref):
    module = ".".join(ref.split(".")[:-1])
    class_name = ref.split(".")[-1]
    m = importlib.import_module(module)    
    return eval('m.%s' % class_name)         
'''
def get_user_score(user):
    """ Compute the score of a given user taking into account their Achievement's bonuses"""
    return AchievementRecord.objects.filter(user=user).aggregate(score=Sum('achievement__bonus'))['score']

'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit-game/$', views.submit_game, name='game_submit'),
    url(r'^rankings/$', views.rankings, name = 'game_detail'),
]

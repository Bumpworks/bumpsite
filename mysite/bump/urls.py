from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^game/([0-9]+)/$', views.game_detail, name = 'game_detail'),
	url(r'^player/(\w+)/$', views.player_detail, name = 'player_detail'),
]

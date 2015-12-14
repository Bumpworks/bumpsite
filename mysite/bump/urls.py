from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit-game/$', views.submit_game, name='game_submit'),
    url(r'^rankings/$', views.rankings, name = 'rankings'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profiles/(?P<player_identifier>[\w]+)/$', views.player_profile, name='profile'),
    url(r'^players/$', views.player_info, name='player_info'),
    url(r'^create-player/$', views.create_player, name='create_player'),
    url(r'^api/games$', views.api_games, name='api_games'),
    url(r'^api/games/(?P<player1>[\w]+)/(?P<player2>[\w]+)$', views.api_games_between, name='api_games_between'),
    url(r'^api/games/(?P<player>[\w]+)$', views.api_games_by, name='api_games_by'),
    url(r'^api/players$', views.api_players, name='api_players'),



    
]

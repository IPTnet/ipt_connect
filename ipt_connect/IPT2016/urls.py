# coding: utf8
from django.conf.urls import url
from views import *
from forms import member_for_team

app_name = 'IPT2016'

urlpatterns = [
    url(r'^$', tournament_overview),
	url(r'^tournament$', tournament_overview, name='tournament_overview'),
    url(r'^participants$', participants_overview, name='participants_overview'),
    url(r'^participants/(?P<pk>[0-9]+)/$', participant_detail, name='participant_detail'),
    url(r'^jurys$', jurys_overview, name='jurys_overview'),
    url(r'^member_for_team$', member_for_team),
    url(r'^jurys/(?P<pk>[0-9]+)/$', jury_detail, name='jury_detail'),
	url(r'^problems$', problems_overview, name="problems_overview"),
	url(r'^problems/(?P<pk>[0-9]+)/$', problem_detail, name="problem_detail"),
	url(r'^rounds$', rounds, name="rounds"),
	url(r'^rounds/(?P<pk>[0-9]+)/$', round_detail, name="round_detail"),
	url(r'^finalrounds/(?P<pk>[0-9]+)/$', finalround_detail, name="finalround_detail"),
	url(r'^teams$', teams_overview, name="teams"),
	url(r'^teams/(?P<team_name>[A-Za-z0-9\- ]+)/$', team_detail, name='team_detail'),
	url(r'^physics_fights$', physics_fights, name='physics_fights'),
	url(r'^physics_fights/(?P<pfid>[0-9]+)/$', physics_fight_detail, name='physics_fight_detail'),
    url(r'^ranking$', ranking, name='ranking'),
    url(r'^listing_participants$', listing_participants),
]

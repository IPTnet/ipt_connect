from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^participants$', all_participants),
	url(r'^test$', test),
	url(r'^tournament$', tournament_overview),
	url(r'^teams$', teams_overview, name="teams"),
	url(r'^teams/(?P<team_name>[A-Za-z]+)/$', team_detail, name='team_detail')


)

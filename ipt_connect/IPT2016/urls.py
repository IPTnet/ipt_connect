from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^participants$', all_participants),
)

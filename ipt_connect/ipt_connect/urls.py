from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from ipt_connect.views import home
from IPT2018.views import tournament_overview

urlpatterns = [
    # Examples:
    # url(r'^$', 'ipt_connect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    #url(r'^$', home, name='home'), #TemplateView.as_view(template_name='index.html')),#'ipt_connect.views.home'),
	url(r'^$', tournament_overview),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('loginas.urls')),
    url(r'^IPT2016/', include('IPT2016.urls', namespace='IPT2016')),
    url(r'^FPT2017/', include('FPT2017.urls', namespace='FPT2017')),
	url(r'^IPT2017/', include('IPT2017.urls', namespace='IPT2017')),
	url(r'^IPT2018/', include('IPT2018.urls', namespace='IPT2018')),
]



admin.site.site_header = 'IPT administration'

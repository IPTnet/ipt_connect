from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from ipt_connect.views import home
from IPTdev.views import tournament_overview

urlpatterns = [
    # Examples:
    # url(r'^$', 'ipt_connect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    #url(r'^$', home, name='home'), #TemplateView.as_view(template_name='index.html')),#'ipt_connect.views.home'),
    url(r'^$', tournament_overview),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('loginas.urls')),
    url(r'^IPTdev/', include('IPTdev.urls', namespace='IPTdev'))
]


admin.site.site_header = 'IPT administration'

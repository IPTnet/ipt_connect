from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'ipt_connect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^$', TemplateView.as_view(template_name='index.html')),#'ipt_connect.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^IPT2016/', include('IPT2016.urls', namespace='IPT2016')),
    url(r'^FPT2017/', include('FPT2017.urls', namespace='FPT2017')),
]


admin.site.site_header = 'IPT administration'
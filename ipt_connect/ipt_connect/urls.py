from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'ipt_connect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^$','ipt_connect.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^IPT2016/', include('IPT2016.urls')),
]


admin.site.site_header = 'IPT administration'
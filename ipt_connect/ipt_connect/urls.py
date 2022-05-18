import importlib

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

tournament_overview = importlib.import_module(
    settings.INSTALLED_TOURNAMENTS[0] + ".views"
).tournament_overview

urlpatterns = [
    # Examples:
    # url(r'^$', 'ipt_connect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^grappelli/", include("grappelli.urls")),  # grappelli URLS
    # url(r'^$', home, name='home'), #TemplateView.as_view(template_name='index.html')),#'ipt_connect.views.home'),
    url(r"^$", tournament_overview),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^admin/", include("loginas.urls")),
]

for tournament in settings.INSTALLED_TOURNAMENTS:
    urlpatterns.append(
        url(
            r"^" + tournament + "/", include(tournament + ".urls", namespace=tournament)
        )
    )

admin.site.site_header = "IPT administration"

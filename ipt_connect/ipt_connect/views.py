from django.http import HttpResponse


def home(request):
    text = """<h1>IPT Connect</h1>

              <a href="http://connect.iptnet.info/IPTdev">Results of IPT dev</a>"""
    return HttpResponse(text)

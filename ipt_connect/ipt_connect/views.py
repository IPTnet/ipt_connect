from django.http import HttpResponse

def home(request):

    text = """<h1>IPT Connect</h1>

              <a href="http://connect.iptnet.info/IPT2016">Results of IPT 2016</a>"""
    return HttpResponse(text)
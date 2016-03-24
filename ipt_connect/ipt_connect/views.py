from django.http import HttpResponse

def home(request):

    text = """<h1>IPT Connect</h1>

              <p>Soon!</p>"""

    return HttpResponse(text)
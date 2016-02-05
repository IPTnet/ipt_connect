from django.http import HttpResponse
from django.shortcuts import render
from models import Participant

def home(request):

    text = """<h1>IPT 2016</h1>

              <p>It's coming...</p>"""

    return HttpResponse(text)


def all_participants(request):
    participants_objects = Participant.objects.all()

    return render(request,'all_participants.html',{'participants' : participants_objects})

def test(request,name=None):
	if name:
		return HttpResponse("Hello %s!" % name)
	else:
		return HttpResponse("Hello world!")
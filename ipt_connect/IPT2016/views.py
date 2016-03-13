from django.http import HttpResponse
from django.shortcuts import render
from models import *

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

def tournament_overview(request):
	pfs = PhysicsFight.objects.all()
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'tournament_overview.html', {'teams': teams, 'pfs': pfs})

def teams_overview(request):
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'teams_overview.html', {'teams': teams})


def team_detail(request, team_name):
	team = Team.objects.filter(name=team_name)
	participants = Participant.objects.filter(team__name=team_name)
	return render(request, 'team_detail.html', {'team': team, 'participants': participants})



def ranking(request):
	# NOT DEFINED YET !!!
	pass
	"""
	teams = Team.objects.all()
	ranking = teams[0].ranking(verbose=False)
	rankteams = []

	for team in ranking[0]:
		rankteams.append(team)

	return render(request, 'ranking.html', {'rankteams': rankteams})
	"""
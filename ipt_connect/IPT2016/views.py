from django.http import HttpResponse
from django.shortcuts import render
from models import *

def home(request):

	text = """<h1>IPT 2016</h1>

			  <p>It's coming...</p>"""

	return HttpResponse(text)


def participants_overview(request):
	participants = Participant.objects.all()
	participants = sorted(participants, key=lambda participant: participant.name)
	return render(request,'participants_overview.html', {'participants' : participants})

def participant_detail(request, pk):
	participant = Participant.objects.filter(pk=pk)
	return render(request, 'participant_detail.html', {'participant': participant})


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


def physics_fights(request):
	pfs = PhysicsFight.objects.all()
	return render(request, 'physics_fights.html', {'pfs': pfs})

def physics_fight_detail(request, pk):
	pf = PhysicsFight.objects.filter(pk=pk)
	jurygrades = JuryGrade.objects.filter(physics_fight=pf)
	meangrades = []
	# participants mean grades

	meangrades.append(pf[0].reporter.compute_average_grades(physicsfights=[pf[0]], verbose=False)[0]["value"])
	meangrades.append(pf[0].opponent.compute_average_grades(physicsfights=[pf[0]], verbose=False)[0]["value"])
	meangrades.append(pf[0].reviewer.compute_average_grades(physicsfights=[pf[0]], verbose=False)[0]["value"])
	return render(request, 'physics_fight_detail.html', {'pf': pf, 'jurygrades': jurygrades, 'meangrades': meangrades})

def blah(request):
	return render(request, 'blah.html')


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
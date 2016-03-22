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
	return render(request, 'participants_overview.html', {'participants' : participants})

def participant_detail(request, pk):
	participant = Participant.objects.filter(pk=pk)
	return render(request, 'participant_detail.html', {'participant': participant})


def jurys_overview(request):
	jurys = Jury.objects.all()
	jurys = sorted(jurys, key=lambda participant: participant.name)
	return render(request, 'jurys_overview.html', {'jurys': jurys})

def jury_detail(request, pk):
	jury = Jury.objects.filter(pk=pk)
	return render(request, 'jury_detail.html', {'jury': jury})


def tournament_overview(request):
	pfs = PhysicsFight.objects.all()
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	rounds = [1, 2, 3, 4]
	rooms = Room.objects.all()
	rooms = sorted(rooms, key=lambda room: room.name)
	roomnumbers = [ind +1 for ind, room in enumerate(rooms)]
	orderedpfsperroom=[]
	for room in rooms:
		thisroom = []
		for round in rounds:
			thisround = []
			mypfs = PhysicsFight.objects.filter(round_number=round).filter(room=room)
			mypfs = sorted(mypfs, key=lambda pf: pf.fight_number)
			print len(mypfs)
			for ind2, pf in enumerate(mypfs):
				thisround.append(pf)
			thisroom.append(thisround)
		orderedpfsperroom.append(thisroom)
	return render(request, 'tournament_overview.html', {'teams': teams, 'pfs': pfs, 'rounds': rounds, 'roomnumbers':roomnumbers, 'orderedpfsperroom': orderedpfsperroom})

def teams_overview(request):
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'teams_overview.html', {'teams': teams})


def team_detail(request, team_name):
	team = Team.objects.filter(name=team_name)
	participants = Participant.objects.filter(team__name=team_name)
	return render(request, 'team_detail.html', {'team': team, 'participants': participants})

def problems_overview(request):
	problems = Problem.objects.all()
	problems = sorted(problems, key=lambda problem: problem.name)
	return render(request, 'problems_overview.html', {'problems': problems})

def problem_detail(request, pk):
	problem = Problem.objects.filter(pk=pk)
	(meangrades, teamresults) = problem[0].status(verbose=False)

	return render(request, 'problem_detail.html', {'problem': problem, "meangrades": meangrades, "teamresults": teamresults})


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

	tacticalrejections = TacticalRejection.objects.filter(physics_fight=pf)
	eternalrejection = EternalRejection.objects.filter(physics_fight=pf)

	return render(request, 'physics_fight_detail.html', {'pf': pf, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection})

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
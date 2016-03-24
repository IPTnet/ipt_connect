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
	rounds = Round.objects.all()
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	pfs = [1, 2, 3, 4]
	rooms = Room.objects.all()
	rooms = sorted(rooms, key=lambda room: room.name)
	roomnumbers = [ind +1 for ind, room in enumerate(rooms)]
	orderedroundsperroom=[]
	for room in rooms:
		thisroom = []
		for pf in pfs:
			thispf = []
			myrounds = Round.objects.filter(pf_number=pf).filter(room=room)
			myrounds = sorted(myrounds, key=lambda round: round.round_number)
			print len(myrounds)
			for ind2, round in enumerate(myrounds):
				thispf.append(round)
			thisroom.append(thispf)
		orderedroundsperroom.append(thisroom)
	return render(request, 'tournament_overview.html', {'teams': teams, 'rounds': rounds, 'pfs': pfs, 'roomnumbers':roomnumbers, 'orderedroundsperroom': orderedroundsperroom})

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


def rounds(request):
	rounds = Round.objects.all()
	return render(request, 'rounds.html', {'rounds': rounds})

def round_detail(request, pk):
	round = Round.objects.filter(pk=pk)
	jurygrades = JuryGrade.objects.filter(round=round)
	meangrades = []
	# participants mean grades
	meangrades.append(round[0].reporter.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
	meangrades.append(round[0].opponent.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
	meangrades.append(round[0].reviewer.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])

	tacticalrejections = TacticalRejection.objects.filter(round=round)
	eternalrejection = EternalRejection.objects.filter(round=round)

	return render(request, 'round_detail.html', {'round': round, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection})

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
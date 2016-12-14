# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from models import *
from django.contrib.auth.decorators import user_passes_test

def home(request):

	text = """<h1>FPT 2017</h1>

			  <p>It's coming...</p>"""

	return HttpResponse(text)

cache_duration_short = 0 # 60 * 1
cache_duration = 0 #60 * 60 * 60


@cache_page(cache_duration)
def participants_overview(request):
	participants = Participant.objects.filter(role='TM') | Participant.objects.filter(role='TC')
	for participant in participants:
		participant.allpoints = participant.points()
		try:
			participant.avggrade = participant.allpoints / len(Round.objects.filter(reporter=participant) | Round.objects.filter(opponent=participant) | Round.objects.filter(reviewer=participant))
		except:
			participant.avggrade = 0.0

	#rankedparticipants = participants[0].ranking(verbose=False)[0]
	participants = sorted(participants, key=lambda participant: participant.avggrade)[::-1]

	return render(request, 'FPT2017/participants_overview.html', {'participants': participants})

@cache_page(cache_duration)
def participant_detail(request, pk):
	participant = Participant.objects.get(pk=pk)
	average_grades=participant.compute_average_grades(verbose=False)
	return render(request, 'FPT2017/participant_detail.html', {'participant': participant, "average_grades": average_grades})

@cache_page(cache_duration)
def jurys_overview(request):
	jurys = Jury.objects.all()
	jurys = sorted(jurys, key=lambda participant: participant.name)
	for jury in jurys:
		mygrades = JuryGrade.objects.filter(jury=jury)
		if mygrades:
			jury.meanrepgrade = mean([grade.grade_reporter for grade in mygrades])
		else:
			jury.meanrepgrade = 0.0
		if mygrades:
			jury.meanoppgrade = mean([grade.grade_opponent for grade in mygrades])
		else:
			jury.meanoppgrade = 0.0
		if mygrades:
			jury.meanrevgrade = mean([grade.grade_reviewer for grade in mygrades])
		else:
			jury.meanrevgrade = 0.0
	return render(request, 'FPT2017/jurys_overview.html', {'jurys': jurys})


@cache_page(cache_duration)
def jury_detail(request, pk):
	jury = Jury.objects.get(pk=pk)
	mygrades = JuryGrade.objects.filter(jury=jury)
	return render(request, 'FPT2017/jury_detail.html', {'jury': jury, "grades": mygrades})

@cache_page(cache_duration)
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
			for ind2, round in enumerate(myrounds):
				thispf.append(round)
			thisroom.append(thispf)
		orderedroundsperroom.append(thisroom)
	return render(request, 'FPT2017/tournament_overview.html', {'teams': teams, 'rounds': rounds, 'pfs': pfs, 'roomnumbers':roomnumbers, 'orderedroundsperroom': orderedroundsperroom})

@cache_page(cache_duration)
def teams_overview(request):
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'FPT2017/teams_overview.html', {'teams': teams})

@cache_page(cache_duration)
def team_detail(request, team_name):
	team = Team.objects.filter(name=team_name)
	participants = Participant.objects.filter(team=team).filter(role='TM') | Participant.objects.filter(team=team).filter(role='TC')
	rankedparticipants = participants[0].ranking(pool="team", verbose=False)[0]
	teamleaders = Jury.objects.filter(team=team)
	myreprounds = Round.objects.filter(reporter_team=team)
	myopprounds = Round.objects.filter(opponent_team=team)
	myrevrounds = Round.objects.filter(reviewer_team=team)
	allrounds = []
	for rounds in [myreprounds, myopprounds, myrevrounds]:
		for round in rounds:
			if len(JuryGrade.objects.filter(round=round)) > 0:
				if round.reporter_team == team[0]:
					round.myrole = "reporter"
					round.mygrade = round.reporter.compute_average_grades(rounds=[round], verbose=False)[0]["value"]
				if round.opponent_team == team[0]:
					round.myrole = "opponent"
					round.mygrade = round.opponent.compute_average_grades(rounds=[round], verbose=False)[0]["value"]
				if round.reviewer_team == team[0]:
					round.myrole = 'reviewer'
					round.mygrade = round.reviewer.compute_average_grades(rounds=[round], verbose=False)[0]["value"]

				allrounds.append(round)

	penalties=[]
	for ind, p in enumerate([penalty for penalty in team[0].presentation_coefficients(verbose=False)]):
		if p != 3.0:
			penalties.append([ind+1, p])
	return render(request, 'FPT2017/team_detail.html', {'team': team[0], 'participants': rankedparticipants, 'teamleaders': teamleaders, 'allrounds': allrounds, 'penalties': penalties})

@cache_page(cache_duration)
def problems_overview(request):
	problems = Problem.objects.all()
	problems = sorted(problems, key=lambda problem: int(problem.name.split('-')[0]))
	rounds = Round.objects.all()
	for problem in problems:
		problem.npres = len(rounds.filter(problem_presented=problem))
		meangrades = problem.status(verbose=False, meangradesonly=True)
		problem.meangradrep = meangrades["report"]
		problem.meangradopp = meangrades["opposition"]
		problem.meangradrev = meangrades["review"]

	return render(request, 'FPT2017/problems_overview.html', {'problems': problems})

@cache_page(cache_duration)
def problem_detail(request, pk):
	problem = Problem.objects.get(pk=pk)
	(meangrades, teamresults) = problem.status(verbose=False)

	return render(request, 'FPT2017/problem_detail.html', {'problem': problem, "meangrades": meangrades, "teamresults": teamresults})

@cache_page(cache_duration_short)
def rounds(request):
	rounds = Round.objects.all()
	pfs = [1, 2, 3, 4]
	rooms = Room.objects.all()
	rooms = sorted(rooms, key=lambda room: room.name)
	orderedroundsperroom=[]
	for room in rooms:
		thisroom = []
		for pf in pfs:
			thispf = []
			myrounds = Round.objects.filter(pf_number=pf).filter(room=room)
			myrounds = sorted(myrounds, key=lambda round: round.round_number)
			for ind2, round in enumerate(myrounds):
				thispf.append(round)
			thisroom.append(thispf)
		orderedroundsperroom.append(thisroom)


	myrounds = Round.objects.filter(pf_number=5)
	finalrounds = sorted(myrounds, key=lambda round: round.round_number)
	try:
		finalteams = [finalrounds[0].reporter_team, finalrounds[0].opponent_team, finalrounds[0].reviewer_team]
		finalpoints = [team.points(pfnumber=5, bonuspoints=False) for team in finalteams]
		#finalpoints = [23.58, 8.86, 6.57]
	except:
		finalteams = ["---", "---", "---"]
		finalpoints = [0, 0, 0]

	finalranking = []
	for team, point in zip(finalteams, finalpoints):
		finalranking.append([team, point])

	return render(request, 'FPT2017/rounds.html', {'orderedroundsperroom': orderedroundsperroom, 'finalrounds': finalrounds, "finalranking": finalranking})

@cache_page(cache_duration_short)
def round_detail(request, pk):
	round = Round.objects.filter(pk=pk)
	thisround = round[0]
	jurygrades = JuryGrade.objects.filter(round=round)
	jurygrades = sorted(jurygrades, key=lambda jurygrade: jurygrade.jury.name)
	meangrades = []

	# has the round started ? If so, then reporter_team, opponent_team and reviewer_team must be defined
	if None in [thisround.reporter_team, thisround.opponent_team, thisround.reviewer_team]:
		started = False
	else:
		started = True

	# participants mean grades. If the fight is finished, then at least some jurygrades must exists
	if len(jurygrades) != 0:
		meangrades.append(round[0].reporter.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		meangrades.append(round[0].opponent.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		meangrades.append(round[0].reviewer.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		finished = True
	else:
		finished = False

	tacticalrejections = TacticalRejection.objects.filter(round=round)
	eternalrejection = EternalRejection.objects.filter(round=round)

	return render(request, 'FPT2017/round_detail.html', {'round': round, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection, "started": started, "finished": finished})

@cache_page(cache_duration_short)
def finalround_detail(request, pk):
	round = Round.objects.filter(pk=pk)
	thisround = round[0]
	jurygrades = JuryGrade.objects.filter(round=round)
	jurygrades = sorted(jurygrades, key=lambda jurygrade: jurygrade.jury.name)
	meangrades = []

	# has the round started ? If so, then reporter_team, opponent_team and reviewer_team must be defined
	if None in [thisround.reporter_team, thisround.opponent_team, thisround.reviewer_team]:
		started = False
	else:
		started = True

	# participants mean grades. If the fight is finished, then at least some jurygrades must exists
	if len(jurygrades) != 0:
		meangrades.append(round[0].reporter.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		meangrades.append(round[0].opponent.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		meangrades.append(round[0].reviewer.compute_average_grades(rounds=[round[0]], verbose=False)[0]["value"])
		finished = True
	else:
		finished = False

	tacticalrejections = TacticalRejection.objects.filter(round=round)
	eternalrejection = EternalRejection.objects.filter(round=round)

	return render(request, 'FPT2017/finalround_detail.html', {'round': round, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection, "started": started, "finished": finished})



@cache_page(cache_duration)
def physics_fights(request):
	rounds = Round.objects.all()
	pf1 = rounds.filter(pf_number=1)
	pf2 = rounds.filter(pf_number=2)
	pf3 = rounds.filter(pf_number=3)
	pf4 = rounds.filter(pf_number=4)
	return render(request, 'FPT2017/physics_fights.html', {'pf1': pf1, 'pf2': pf2, 'pf3': pf3, 'pf4': pf4})

@cache_page(cache_duration)
def physics_fight_detail(request, pfid):
	rounds = Round.objects.filter(pf_number=pfid)
	rooms = list(set([round.room for round in rounds]))
	rooms = sorted(rooms, key=lambda room: room.name)
	roomgrades = []

	for room in rooms:
		roomrounds = rounds.filter(room=room)
		roomrounds = sorted(roomrounds, key=lambda round: round.pf_number)
		finished=False
		# all the jury members of this fight-room, sorted by name
		jurynames = JuryGrade.objects.filter(round=roomrounds[0])
		jurynames = sorted([jurygrade.jury.name for jurygrade in jurynames])
		juryallgrades = []
		for juryname in jurynames:
			juryallgrade = {"name": juryname}
			juryroundsgrades = []
			for round in roomrounds:
				try:
					# if one round has no jurygrade, it means it is not finished.
					juryroundsgrade=JuryGrade.objects.filter(round=round).filter(jury__name=juryname)[0]
					finished=True
					juryroundsgrades.append(juryroundsgrade)
				except:
					pass

			juryallgrade["juryroundsgrades"] = juryroundsgrades

			juryallgrades.append(juryallgrade)

		# meangrades
		meanroundsgrades = []
		for round in roomrounds:
			meangrades=[]
			try:
				meangrades.append(round.reporter.compute_average_grades(rounds=[round], verbose=False)[0]["value"])
				meangrades.append(round.opponent.compute_average_grades(rounds=[round], verbose=False)[0]["value"])
				meangrades.append(round.reviewer.compute_average_grades(rounds=[round], verbose=False)[0]["value"])
			except:
				pass
			meanroundsgrades.append(meangrades)

		infos = {"pf": pfid, "room": room.name, "finished": finished}
		roundsgrades = [juryallgrades, meanroundsgrades, infos]
		roomgrades.append(roundsgrades)

	return render(request, 'FPT2017/physics_fight_detail.html', {"roomgrades": roomgrades})

@cache_page(cache_duration)
def ranking(request):

	teams = Team.objects.all()
	rankteams = []

	if len(teams) > 0 :
		ranking = teams[0].ranking(verbose=False)

		for ind, team in enumerate(ranking[0]):
			myreprounds = Round.objects.filter(reporter_team=team)
			myopprounds = Round.objects.filter(opponent_team=team)
			myrevrounds = Round.objects.filter(reviewer_team=team)
			pfsplayed = min(len(myreprounds), len(myopprounds), len(myrevrounds))
			team.pfsplayed = pfsplayed
			team.ongoingpf = False
			if max(len(myreprounds), len(myopprounds), len(myrevrounds)) > pfsplayed:
				team.ongoingpf = True
				team.currentpf = pfsplayed+1
			team.rank = ind+1
			if team.rank < 4:
				team.emphase=True
			rankteams.append(team)

	return render(request, 'FPT2017/ranking.html', {'rankteams': rankteams})

@user_passes_test(lambda u: u.is_superuser)
def listing_participants(request):
	participants_objects = Participant.objects.all()

	return render(request, 'FPT2017/listing_participants.html',{'participants' : participants_objects})

# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

def home(request):

	text = """<h1>IPT 2018</h1>

			  <p>Starting soon !</p>"""

	return HttpResponse(text)

cache_duration_short = 1 * 1
cache_duration = 20 * 1

ninja_mode = False

def ninja_test(user):
	return user.is_staff or not ninja_mode

@cache_page(cache_duration_short)
def soon(request):
	return render(request, 'IPT2018/bebacksoon.html')

#####################################################
################# SUPER USERS VIEWS #################
@user_passes_test(lambda u: u.is_superuser or u.username == 'fava' or u.username == 'vanovsky')
def participants_trombinoscope(request):
	participants = Participant.objects.all().order_by('team','surname')

	return render(request, 'IPT2018/participants_trombinoscope.html', {'participants': participants})

@user_passes_test(lambda u: u.is_superuser or u.username == 'fava' or u.username == 'vanovsky')
def participants_export(request):
	participants = Participant.objects.all().order_by('team','role','name')

	return render(request, 'IPT2018/participants_export.html', {'participants': participants})

@user_passes_test(lambda u: u.is_superuser or u.username == 'fava' or u.username == 'vanovsky')
def participants_export_web(request):
	participants = Participant.objects.exclude(role='ACC').order_by('team','role','surname')

	return render(request, 'IPT2018/listing_participants_web.html', {'participants': participants})

@user_passes_test(lambda u: u.is_superuser or u.username == 'fava' or u.username == 'vanovsky')
def jury_export(request):
	jurys = Jury.objects.all().order_by('surname')

	return render(request, 'IPT2018/listing_jurys.html', {'jurys': jurys})

@user_passes_test(lambda u: u.is_superuser or u.username == 'fava' or u.username == 'vanovsky')
def jury_export_web(request):
	jurys = Jury.objects.filter(team=None).order_by('surname')

	return render(request, 'IPT2018/listing_jurys_web.html', {'jurys': jurys})

@user_passes_test(lambda u: u.is_superuser)
def update_all(request):
	list_receivers = update_signal.send(sender=Round)

	assert len(list_receivers) == 1, "len(list_receivers) is not 1 in view update_all"

	return HttpResponse(list_receivers[0][1])



@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def participants_overview(request):
	participants = Participant.objects.filter(role='TM') | Participant.objects.filter(role='TC')
	for participant in participants:
		participant.allpoints = participant.tot_score_as_reporter + participant.tot_score_as_opponent + participant.tot_score_as_reviewer
		try:
			participant.avggrade = participant.allpoints / len(Round.objects.filter(reporter=participant) | Round.objects.filter(opponent=participant) | Round.objects.filter(reviewer=participant))
		except:
			participant.avggrade = 0.0
			print "PLOP"

	participants = sorted(participants, key=lambda participant: participant.avggrade, reverse=True)

	return render(request, 'IPT2018/participants_overview.html', {'participants': participants})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def participants_all(request):
	participants = Participant.objects.all().order_by('team','surname')

	return render(request, 'IPT2018/participants_all.html', {'participants': participants})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def participant_detail(request, pk):
	participant = Participant.objects.get(pk=pk)

	rounds = (Round.objects.filter(reporter=participant) | Round.objects.filter(opponent=participant) | Round.objects.filter(reviewer=participant)).order_by('pf_number', 'round_number')

	average_grades = []
	for round in rounds:
		if round.reporter == participant :
			average_grades.append({"value": round.score_reporter, "round":round, "role":"reporter"})
		elif round.opponent == participant :
			average_grades.append({"value": round.score_opponent, "round":round, "role":"opponent"})
		else :
			average_grades.append({"value": round.score_reviewer, "round":round, "role":"reviewer"})

	return render(request, 'IPT2018/participant_detail.html', {'participant': participant, "average_grades": average_grades})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def jurys_overview(request):
	jurys = Jury.objects.all().order_by('name')

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
	return render(request, 'IPT2018/jurys_overview.html', {'jurys': jurys})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def jury_detail(request, pk):
	jury = Jury.objects.get(pk=pk)
	mygrades = JuryGrade.objects.filter(jury=jury)
	return render(request, 'IPT2018/jury_detail.html', {'jury': jury, "grades": mygrades})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def tournament_overview(request):
	rounds = Round.objects.all()

	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)

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

			for round in myrounds:
				thispf.append(round)

			thisroom.append(thispf)

		orderedroundsperroom.append(thisroom)

	return render(request, 'IPT2018/tournament_overview.html', {'teams': teams, 'rounds': rounds, 'pfs': pfs, 'roomnumbers':roomnumbers, 'orderedroundsperroom': orderedroundsperroom})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def teams_overview(request):
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'IPT2018/teams_overview.html', {'teams': teams})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def team_detail(request, team_name):
	team = Team.objects.get(name=team_name)
	ranking = Team.objects.order_by('-total_points')
	for i,t in enumerate(ranking):
		if t == team:
			team.rank = i+1
	# team.rank = ranking.index(team) + 1
	participants = Participant.objects.filter(team=team).filter(role='TM') | Participant.objects.filter(team=team).filter(role='TC')

	rankedparticipants = participants.order_by('total_points')

	teamleaders = Jury.objects.filter(team=team)

	myreprounds = Round.objects.filter(reporter_team=team)
	myopprounds = Round.objects.filter(opponent_team=team)
	myrevrounds = Round.objects.filter(reviewer_team=team)

	allrounds = []

	for round in myreprounds:
		# if len(JuryGrade.objects.filter(round=round)) > 0:
		if round.score_reporter > 0.:
			round.myrole = "reporter"
			round.mygrade = round.score_reporter
			allrounds.append(round)
	for round in myopprounds:
		# if len(JuryGrade.objects.filter(round=round)) > 0:
		if round.score_opponent > 0.:
			round.myrole = "opponent"
			round.mygrade = round.score_opponent
			allrounds.append(round)
	for round in myrevrounds:
		# if len(JuryGrade.objects.filter(round=round)) > 0:
		if round.score_reviewer > 0.:
			round.myrole = "reviewer"
			round.mygrade = round.score_reviewer
			allrounds.append(round)

	penalties=[]
	prescoeffs = team.presentation_coefficients(verbose=False)

	for ind, p in enumerate(prescoeffs):
		if p != 3.0:
			penalties.append([ind+1, p])

	return render(request, 'IPT2018/team_detail.html', {'team': team, 'participants': rankedparticipants, 'teamleaders': teamleaders, 'allrounds': allrounds, 'penalties': penalties})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def problems_overview(request):
	problems = Problem.objects.all().order_by('name')
	rounds = Round.objects.all()
	for problem in problems:
		problem.npres = len(rounds.filter(problem_presented=problem))
		problem.meangradrep = problem.mean_score_of_reporters
		problem.meangradopp = problem.mean_score_of_opponents
		problem.meangradrev = problem.mean_score_of_reviewers

	return render(request, 'IPT2018/problems_overview.html', {'problems': problems})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def problem_detail(request, pk):
	problem = Problem.objects.get(pk=pk)
	(meangrades, teamresults) = problem.status(verbose=False)

	return render(request, 'IPT2018/problem_detail.html', {'problem': problem, "meangrades": meangrades, "teamresults": teamresults})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def rounds(request):
	rounds = Round.objects.all()
	rooms = Room.objects.order_by('name')

	orderedroundsperroom=[]
	for room in rooms:
		thisroom = []
		for pf in pfs:
			thisroom.append(Round.objects.filter(pf_number=pf).filter(room=room).order_by('round_number'))
		orderedroundsperroom.append(thisroom)

	if with_final_pf :
		myrounds = Round.objects.filter(pf_number=npf+1)
		finalrounds = sorted(myrounds, key=lambda round: round.round_number)
		try:
			finalteams = [finalrounds[0].reporter_team, finalrounds[0].opponent_team, finalrounds[0].reviewer_team]
			finalpoints = [team.points(pfnumber=5, bonuspoints=False) for team in finalteams]
		except:
			finalteams = ["---", "---", "---"]
			finalpoints = [0, 0, 0]

			finalranking = []
		for team, point in zip(finalteams, finalpoints):
			finalranking.append([team, point])

		return render(request, 'IPT2018/rounds.html', {'orderedroundsperroom': orderedroundsperroom, 'finalrounds': finalrounds, "finalranking": finalranking})

	else :
		return render(request, 'IPT2018/rounds.html', {'orderedroundsperroom': orderedroundsperroom})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def round_detail(request, pk):
	round = Round.objects.get(pk=pk)

	jurygrades = JuryGrade.objects.filter(round=round).order_by('jury__name')
	meangrades = []

	# has the round started ? If so, then reporter_team, opponent_team and reviewer_team must be defined
	if None in [round.reporter_team, round.opponent_team, round.reviewer_team]:
		started = False
	else:
		started = True

	# participants mean grades. If the fight is finished, then at least some jurygrades must exists
	if len(jurygrades) != 0:
		meangrades.append(round.score_reporter)
		meangrades.append(round.score_opponent)
		meangrades.append(round.score_reviewer)
		finished = True
	else:
		finished = False

	tacticalrejections = TacticalRejection.objects.filter(round=round)
	eternalrejection = EternalRejection.objects.filter(round=round)

	return render(request, 'IPT2018/round_detail.html', {'round': round, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection, "started": started, "finished": finished})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def finalround_detail(request, pk):
	round = Round.objects.get(pk=pk)
	jurygrades = JuryGrade.objects.filter(round=round).order_by('jury__name')
	meangrades = []

	# has the round started ? If so, then reporter_team, opponent_team and reviewer_team must be defined
	if None in [round.reporter_team, round.opponent_team, round.reviewer_team]:
		started = False
	else:
		started = True

	# participants mean grades. If the fight is finished, then at least some jurygrades must exists
	if len(jurygrades) != 0:
		meangrades.append(round.score_reporter)
		meangrades.append(round.score_opponent)
		meangrades.append(round.score_reviewer)
		finished = True
	else:
		finished = False

	tacticalrejections = TacticalRejection.objects.filter(round=round)
	eternalrejection = EternalRejection.objects.filter(round=round)

	return render(request, 'IPT2018/finalround_detail.html', {'round': round, 'jurygrades': jurygrades, 'meangrades': meangrades, "tacticalrejections": tacticalrejections, "eternalrejection": eternalrejection, "started": started, "finished": finished})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def physics_fights(request):
	rounds = Round.objects.all()
	pf1 = rounds.filter(pf_number=1)
	pf2 = rounds.filter(pf_number=2)
	pf3 = rounds.filter(pf_number=3)
	return render(request, 'IPT2018/physics_fights.html', {'pf1': pf1, 'pf2': pf2, 'pf3': pf3})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def physics_fight_detail(request, pfid):
	rounds = Round.objects.filter(pf_number=pfid)
	rooms = Room.objects.all().order_by('name')

	roomgrades = []
	for room in rooms:
		roomrounds = rounds.filter(room=room)
		finished = False
		grades = JuryGrade.objects.filter(round__room=room, round__pf_number=pfid).order_by('round__round_number', 'jury__surname')
		gradesdico = {}
		for grade in grades:
			gradesdico[grade.jury] = []
		for grade in grades:
			gradesdico[grade.jury].append(grade)

		juryallgrades = [{'juryroundsgrades': gradesdico[jury], 'name': jury.name+" "+jury.surname} for jury in gradesdico.keys()]
		print juryallgrades

		# meangrades
		meanroundsgrades = []
		for round in roomrounds:
			meangrades=[]
			try:
				meangrades.append(round.score_reporter)
				meangrades.append(round.score_opponent)
				meangrades.append(round.score_reviewer)

			except:
				pass
			meanroundsgrades.append(meangrades)

		infos = {"pf": pfid, "room": room.name, "finished": finished}
		roundsgrades = [juryallgrades, meanroundsgrades, infos]
		roomgrades.append(roundsgrades)

	return render(request, 'IPT2018/physics_fight_detail.html', {"roomgrades": roomgrades})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def ranking(request):
	rankteams = []
	ranking = Team.objects.order_by('-total_points')

	# if len(teams) > 0 :
	if len(ranking) > 0:

		for ind, team in enumerate(ranking):
			nrounds_as_rep = team.nrounds_as_rep # Round.objects.filter(reporter_team=team)
			nrounds_as_opp = team.nrounds_as_opp # Round.objects.filter(opponent_team=team)
			nrounds_as_rev = team.nrounds_as_rev # Round.objects.filter(reviewer_team=team)
			pfsplayed = min(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev)
			team.pfsplayed = pfsplayed
			team.ongoingpf = False
			#if max(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev) > pfsplayed:
				#team.ongoingpf = True
				#team.currentpf = pfsplayed+1
			team.rank = ind+1
			if team.rank == 1:
				team.emphase=True
			rankteams.append(team)

	return render(request, 'IPT2018/ranking.html', {'rankteams': rankteams})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT2018/soon')
@cache_page(cache_duration)
def poolranking(request):
	# Pool A
	rankteamsA = []
	ranking = Team.objects.filter(pool="A").order_by('-total_points')

	# if len(teams) > 0 :
	if len(ranking) > 0:

		for ind, team in enumerate(ranking):
			nrounds_as_rep = team.nrounds_as_rep # Round.objects.filter(reporter_team=team)
			nrounds_as_opp = team.nrounds_as_opp # Round.objects.filter(opponent_team=team)
			nrounds_as_rev = team.nrounds_as_rev # Round.objects.filter(reviewer_team=team)
			pfsplayed = min(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev)
			team.pfsplayed = pfsplayed
			team.ongoingpf = False
			if max(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev) > pfsplayed:
				team.ongoingpf = True
				team.currentpf = pfsplayed+1
			team.rank = ind+1
			if team.rank == 1:
				team.emphase=True
			rankteamsA.append(team)

	# Pool B
	rankteamsB = []
	ranking = Team.objects.filter(pool="B").order_by('-total_points')

	# if len(teams) > 0 :
	if len(ranking) > 0:

		for ind, team in enumerate(ranking):
			nrounds_as_rep = team.nrounds_as_rep # Round.objects.filter(reporter_team=team)
			nrounds_as_opp = team.nrounds_as_opp # Round.objects.filter(opponent_team=team)
			nrounds_as_rev = team.nrounds_as_rev # Round.objects.filter(reviewer_team=team)
			pfsplayed = min(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev)
			team.pfsplayed = pfsplayed
			team.ongoingpf = False
			if max(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev) > pfsplayed:
				team.ongoingpf = True
				team.currentpf = pfsplayed+1
			team.rank = ind+1
			if team.rank == 1:
				team.emphase=True
			rankteamsB.append(team)

	return render(request, 'IPT2018/poolranking.html', {'rankteamsA': rankteamsA, 'rankteamsB': rankteamsB})
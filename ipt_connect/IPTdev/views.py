# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import get_language
from forms import UploadForm
import csv
import parameters as params


def home(request):

	text = """<h1>IPT</h1>

			  <p>Starting soon !</p>"""

	return HttpResponse(text)

cache_duration_short = 1 * 1
cache_duration = 20 * 1

ninja_mode = False

def ninja_test(user):
	return user.is_staff or not ninja_mode

@cache_page(cache_duration_short)
def soon(request):
	return render(request, 'IPT%s/bebacksoon.html' % params.app_version, {'params': params})

#####################################################
################# SUPER USERS VIEWS #################
@user_passes_test(lambda u: u.is_superuser)
def participants_trombinoscope(request):
	participants = Participant.objects.all().order_by('team','surname')

	return render(request, 'IPT%s/participants_trombinoscope.html' % params.app_version, {'participants': participants})

@user_passes_test(lambda u: u.is_superuser or u.username == 'magnusson')
def participants_export(request):
	participants = Participant.objects.all().order_by('team','role','name')

	return render(request, 'IPT%s/participants_export.html' % params.app_version, {'participants': participants, 'params': params})

@user_passes_test(lambda u: u.is_superuser)
def participants_export_web(request):
	participants = Participant.objects.exclude(role='ACC').order_by('team','role','surname')

	return render(request, 'IPT%s/listing_participants_web.html' % params.app_version, {'participants': participants, 'params': params})

@user_passes_test(lambda u: u.is_superuser)
def jury_export(request):
	jurys = Jury.objects.all().order_by('surname')

	return render(request, 'IPT%s/listing_jurys.html' % params.app_version, {'jurys': jurys})

@user_passes_test(lambda u: u.is_superuser)
def jury_export_web(request):
	jurys = Jury.objects.filter(team=None).order_by('surname')

	return render(request, 'IPT%s/listing_jurys_web.html' % params.app_version, {'jurys': jurys})

@user_passes_test(lambda u: u.is_superuser)
def update_all(request):
	list_receivers = update_signal.send(sender=Round)

	assert len(list_receivers) == 1, "len(list_receivers) is not 1 in view update_all"

	return HttpResponse(list_receivers[0][1])



@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def participants_overview(request):
	participants = Participant.objects.filter(role='TM') | Participant.objects.filter(role='TC')
	pr = params.personal_ranking
	for participant in participants:
		participant.allpoints = participant.tot_score_as_reporter + participant.tot_score_as_opponent + participant.tot_score_as_reviewer
		try:
			participant.avggrade = participant.allpoints / len(Round.objects.filter(reporter=participant) | Round.objects.filter(opponent=participant) | Round.objects.filter(reviewer=participant))
		except:
			participant.avggrade = 0.0
			print "PLOP"
		if pr['active']:
			participant.set_personal_score()

	participants = sorted(participants, key=lambda participant: participant.avggrade, reverse=True)

	return render(request, 'IPT%s/participants_overview.html' % params.app_version, {'participants': participants, 'params': params, 'personal_ranking': pr['active']})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def participants_all(request):
	participants = Participant.objects.all().order_by('team','surname')

	return render(request, 'IPT%s/participants_all.html' % params.app_version, {'participants': participants})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def participant_detail(request, pk):
	participant = Participant.objects.get(pk=pk)

	rounds = (Round.objects.filter(reporter=participant) | Round.objects.filter(reporter_2=participant) | Round.objects.filter(opponent=participant) | Round.objects.filter(reviewer=participant)).order_by('pf_number', 'round_number')

	# TODO: refactor to use each filter separately
	average_grades = []
	for round in rounds:
		if   round.reporter   == participant :
			average_grades.append({"value": round.score_reporter, "round":round, "role":"reporter"})

		elif round.opponent   == participant :
			average_grades.append({"value": round.score_opponent, "round":round, "role":"opponent"})

		elif round.reporter_2 == participant :
			if params.display_coreporters :
				average_grades.append({"value": round.score_reporter, "round":round, "role":"coreporter"})

		else :
			average_grades.append({"value": round.score_reviewer, "round":round, "role":"reviewer"})

	return render(request, 'IPT%s/participant_detail.html' % params.app_version, {'participant': participant, "average_grades": average_grades, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
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
	return render(request, 'IPT%s/jurys_overview.html' % params.app_version, {'jurys': jurys, 'params': params})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def jury_detail(request, pk):
	jury = Jury.objects.get(pk=pk)
	mygrades = JuryGrade.objects.filter(jury=jury)
	return render(request, 'IPT%s/jury_detail.html' % params.app_version, {'jury': jury, "grades": mygrades, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def tournament_overview(request):
	return render(request, 'IPT%s/tournament_overview.html' % params.app_version, {'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def teams_overview(request):
	teams = Team.objects.all()
	teams = sorted(teams, key=lambda team: team.name)
	return render(request, 'IPT%s/teams_overview.html' % params.app_version, {'teams': teams, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
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

	bonus_points_displayed = 0.0

	if params.manual_bonus_points:
		bonus_points_displayed += team.bonus_points

	for round in myreprounds:
		# if len(JuryGrade.objects.filter(round=round)) > 0:
		if round.score_reporter > 0.:
			round.myrole = "reporter"
			round.mygrade = round.score_reporter
			allrounds.append(round)
			bonus_points_displayed += round.bonus_points_reporter
			print team_name, round.pf_number, round.bonus_points_reporter
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

	return render(request, 'IPT%s/team_detail.html' % params.app_version, {'team': team, 'participants': rankedparticipants, 'teamleaders': teamleaders, 'allrounds': allrounds, 'penalties': penalties, 'bonus_points_displayed': bonus_points_displayed, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def problems_overview(request):
	problems = Problem.objects.all()
	rounds = Round.objects.all()
	for problem in problems:
		problem.npres = len(rounds.filter(problem_presented=problem))
		problem.meangradrep = problem.mean_score_of_reporters
		problem.meangradopp = problem.mean_score_of_opponents
		problem.meangradrev = problem.mean_score_of_reviewers

	return render(request, 'IPT%s/problems_overview.html' % params.app_version, {'problems': problems, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def problem_detail(request, pk):
	problem = Problem.objects.get(pk=pk)
	(meangrades, teamresults) = problem.status(verbose=False)

	return render(request, 'IPT%s/problem_detail.html' % params.app_version, {'problem': problem, "meangrades": meangrades, "teamresults": teamresults, 'params': params})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def rounds(request):
	rounds = Round.objects.all()
	rooms = Room.objects.order_by('name')

	orderedroundsperroom=[]
	for room in rooms:
		thisroom = []
		for pf in selective_fights:
			thisroom.append(Round.objects.filter(pf_number=pf).filter(room=room).order_by('round_number'))
		orderedroundsperroom.append(thisroom)

	render_data = {
		'params': params,
		'orderedroundsperroom': orderedroundsperroom,
		'selective_fight_names': zip(selective_fights,params.fights['names'][:params.npf]),
	}

	if params.with_final_pf :
		myrounds = Round.objects.filter(pf_number=final_fight_number)
		finalrounds = sorted(myrounds, key=lambda round: round.round_number)
		try:
			finalteams = [finalrounds[0].reporter_team, finalrounds[0].opponent_team, finalrounds[0].reviewer_team]
			finalpoints = [team.points(pfnumber=final_fight_number, bonuspoints=False) for team in finalteams]
		except:
			finalteams = ["---", "---", "---"]
			finalpoints = [0, 0, 0]

			finalranking = []
		for team, point in zip(finalteams, finalpoints):
			finalranking.append([team, point])

		render_data.update({
			'final_fight_number': final_fight_number,
			'finalrounds': finalrounds,
			'finalranking': finalranking,
		})

	if params.semifinals_quantity > 0:
		semifinal_rounds = []
		for pf in semifinals:
			semifinal_rounds.append(Round.objects.filter(pf_number=pf).order_by('round_number'))
		render_data.update({
			'semifinal_data': zip(
				params.fights['names'][params.npf:params.npf+params.semifinals_quantity],
				semifinal_rounds
			)
		})

	return render(request, 'IPT%s/rounds.html' % params.app_version, render_data)


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
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

	return render(
		request,
		'IPT%s/round_detail.html' % params.app_version,
		{
			'params': params,
			'round': round,
			'jurygrades': jurygrades,
			'meangrades': meangrades,
			'tacticalrejections': tacticalrejections,
			'eternalrejection': eternalrejection,
			'started': started,
			'finished': finished,
			'display_room_name': round.pf_number <= params.npf,
			'display_rejections': params.fights['challenge_procedure'][round.pf_number - 1],
			'display_problems_forbidden': params.fights['problems_forbidden'][round.pf_number - 1],
			'physics_fight_name': params.fights['names'][round.pf_number - 1],
		})


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def physics_fight_detail(request, pfid):
	rounds = Round.objects.filter(pf_number=pfid)
	rooms = Room.objects.all().order_by('name')

	roomgrades = []
	for room in rooms:
		roomrounds = rounds.filter(room=room).order_by('round_number')

		grades = JuryGrade.objects.filter(round__room=room, round__pf_number=pfid).order_by('round__round_number', 'jury__surname')
		gradesdico = {}
		for grade in grades:
			gradesdico[grade.jury] = []
		for grade in grades:
			gradesdico[grade.jury].append(grade)

		juryallgrades = [{'juryroundsgrades': gradesdico[jury], 'name': jury.name+" "+jury.surname} for jury in gradesdico.keys()]
		print juryallgrades

		# meangrades and summary grades
		meanroundsgrades = []

		for round in roomrounds:
			meangrades = []
			meangrades.append(round.score_reporter)
			meangrades.append(round.score_opponent)
			meangrades.append(round.score_reviewer)
			meanroundsgrades.append(meangrades)

		teams_involved = get_involved_teams_dict(roomrounds)
		finished = (roomrounds.count() == len(teams_involved))

		if params.display_pf_summary:
			summary_grades = {team: [team.presentation_coefficients()[int(pfid) - 1]] for team in teams_involved}
			for team in teams_involved:
				for r in roomrounds:
					summary_grades[team].append(
						# TODO: looks like this is not the fastest way!
						team.get_scores_for_rounds(rounds=roomrounds.filter(round_number=r.round_number), include_bonus=False)[0]
					)
				summary_grades[team].append(sum(summary_grades[team][1:]))

			summary_grades = sorted(summary_grades.items(), key=lambda x: x[1][-1], reverse=True)

			if finished:
				for team_summary in summary_grades:
					reporter_round = roomrounds.filter(reporter_team=team_summary[0])[0]
					team_summary[1].append(reporter_round.bonus_points_reporter)
		else:
			summary_grades = None


		infos = {"pf": pfid, "room": room.name, "finished": finished}
		roundsgrades = [juryallgrades, meanroundsgrades, infos, summary_grades]
		roomgrades.append(roundsgrades)

	return render(request, 'IPT%s/physics_fight_detail.html' % params.app_version, {
		'params': params,
		'roomgrades': roomgrades,
		'ignore_rooms': int(pfid) > params.npf,
		'fight_name': params.fights['names'][int(pfid) - 1],
		'no_round_played': rounds.count() == 0,
	})


def rank_ordinal(value):
    try:
        value = int(value)
    except ValueError:
        return value
    lang = get_language()
    if lang == 'ru':
        t = ('-ый', '-ый', '-ой', '-ий', '-ый', '-ый', '-ой', '-ой', '-ой', '-ый')
        if not value:
            return "0-ой"
        if value in range(10, 20):
            return "%d-ый" % (value)
        return '%d%s' % (value, t[value % 10])
    else:
        t = ('th', 'st', 'nd', 'rd') + ('th',) * 6
        if value % 100 in (11, 12, 13):
            return u"%d%s" % (value, t[0])
        return u'%d%s' % (value, t[value % 10])

def create_ranking(teams):
    rankteams = []

    if len(teams) > 0:

        for ind, team in enumerate(teams):
            nrounds_as_rep = team.nrounds_as_rep
            nrounds_as_opp = team.nrounds_as_opp
            nrounds_as_rev = team.nrounds_as_rev
            pfsplayed = min(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev)
            team.pfsplayed = pfsplayed
            team.ongoingpf = False
            if max(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev) > pfsplayed:
                team.ongoingpf = True
                team.currentpf = pfsplayed + 1
            team.rank = rank_ordinal(ind + 1)
            rankteams.append(team)

    return rankteams


def create_semi_ranking():
	teams = Team.objects.filter(is_in_semi=True).order_by('-semi_points')
	if teams.count() == 0:
		return None

	return create_ranking(teams)


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def ranking(request):
	rankteams = create_ranking(Team.objects.order_by('-total_points'))
	rankteams[0].emphase = True

	semirankteams = create_semi_ranking()

	return render(request, 'IPT%s/ranking.html' % params.app_version, {
		'params': params,
		'rankteams': rankteams,
		'semirankteams': semirankteams,
	})

@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def poolranking(request):

	# Pool A
	rankteamsA = create_ranking(Team.objects.filter(pool="A").order_by('-total_points'))

	# Pool B
	rankteamsB = create_ranking(Team.objects.filter(pool="B").order_by('-total_points'))

	semirankteams = create_semi_ranking()

	return render(request, 'IPT%s/poolranking.html' % params.app_version, {
		'params': params,
		'rankteamsA': rankteamsA,
		'rankteamsB': rankteamsB,
		'semirankteams': semirankteams,
	})


def make_dict_from_csv_row(row):
	# This is just a map to control numbers of columns which are imported
	# No logic should be placed here!
	return {
		'name': row[1],
		'surname': row[3],
		'affiliation': row[4],
		'team': row[9],
		'role': row[10],
		'is_jury': row[11],
		'email': row[19],
	}


def make_row_importable(row):
	# All the logic needed to parse the row
	# Some edition-specific things are hardcoded here

	if row['team'] == 'Organisational Registration (IOC, ExeCom, invited guest, etc.)':
		# No team reference needed
		row['team'] = None
	else:
		# This also holds automated creation of teams
		row['team'], created = Team.objects.get_or_create(
			name=row['team']
		)

	row['is_jury'] = (row['is_jury'] != '0')

	if row['role'] == 'Team captain':
		row['role'] = 'TC'
	elif row['role'] == 'Team member':
		row['role'] = 'TM'
	else:
		row['role'] = None


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
@cache_page(cache_duration)
def upload_csv(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			csvfile = request.FILES['csvfile']
			reader = csv.reader(csvfile)
			next(reader)
			for row in reader:
				row = make_dict_from_csv_row(row)
				make_row_importable(row)
				print row

				# If a person is not a jury member and has a role,
				# import him/her as a participant
				if not row['is_jury'] and row['role']:
					Participant.objects.get_or_create(
						name=row['name'],
						surname=row['surname'],
						affiliation=row['affiliation'],
						role=row['role'],
						team=row['team'],
					)
				elif row['is_jury']:
					Jury.objects.get_or_create(
						name=row['name'],
						surname=row['surname'],
						affiliation=row['affiliation'],
						team=row['team'],
					)
	else:
		form = UploadForm()

	return render(request, 'IPT%s/upload_csv.html' % params.app_version, {'form': form, 'params': params})
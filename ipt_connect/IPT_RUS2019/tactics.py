from django.shortcuts import render
from django.views.decorators.cache import cache_page
from models import *
from django.contrib.auth.decorators import user_passes_test
import parameters as params
from views import *

def build_tactics_for_two_teams(reporter_team, opponent_team):
	# A "challenge simulation" function.
	# For given reporter and opponent, forbidden problems are listed
	# and some additional information is collected

	# The rules state:
	# The Opponent may challenge the Reporter on any problem with the exception of a problem that:
	# a) was permanently rejected by the Reporter earlier;
	# b) was presented by the Reporter earlier;
	# c) was opposed by the Opponent earlier;
	# d) was presented by the Opponent earlier.
	# If there are no problems left to challenge, the bans d), c), b), a) are successively removed, in that order.

	problems_dict = {}
	all_problems = Problem.objects.all()
	all_rounds = Round.objects.all()

	for problem in all_problems:
		eter_rej =  EternalRejection.objects.filter(problem=problem)
		tact_rej = TacticalRejection.objects.filter(problem=problem)
		atrounds = all_rounds.filter(problem_presented=problem)
		problems_dict[problem] = {
			# Forbidden
			'eternally_rejected_by_reporter':
				map(
					lambda rejection: rejection.round,
					list(eter_rej.filter(round__reporter_team=reporter_team)),
				),
			'reported_by_reporter':
				list(atrounds.filter(reporter_team=reporter_team)),
			'opposed_by_opponent':
				list(atrounds.filter(opponent_team=opponent_team)),
			'reported_by_opponent':
				list(atrounds.filter(reporter_team=opponent_team)),

			# These categories are not forbidden, but are valuable knowledge

			# If the opponent tried to challenge for a problem and received a rejection,
			# it is likely that the opponent will try to challenge for the same problem again.
			# This knowledge is obviously valuable for the reporter ;-)
			'tried_by_opponent':
				map(
					lambda rejection: rejection.round,
					list(tact_rej.filter(round__opponent_team=opponent_team))
					+
					list(eter_rej.filter(round__opponent_team=opponent_team)),
				),

			# The same thing for reviewing
			'reviewed_by_opponent':
				list(atrounds.filter(reviewer_team=opponent_team)),

			# reporter's oppositions...
			'opposed_by_reporter':
				list(atrounds.filter(opponent_team=reporter_team)),

			# ... and for reporter's reviews - no idea what for
			'reviewed_by_reporter':
				list(atrounds.filter(reviewer_team=reporter_team)),

			# Crazyness must go on!
			'tried_by_reporter':
				map(
					lambda rejection: rejection.round,
					list(tact_rej.filter(round__opponent_team=reporter_team))
					+
					list(eter_rej.filter(round__opponent_team=reporter_team)),
				),
		}

	return problems_dict


def sort_raw_tactics_data(problems_dict):

	# The first list consists of banned problems
	# sorted in reverse order on when the bans are removed

	bans = []
	for reason in [
		'eternally_rejected_by_reporter',
		'reported_by_reporter',
		'opposed_by_opponent',
		'reported_by_opponent',
	]:
		for problem in list(problems_dict)[::-1]:
			if len(problems_dict[problem][reason]) > 0:
				bans.append((problem, problems_dict.pop(problem)))

	# The second list consists of available problems

	# Firstly, we collect the problems which the teams has already interacted with

	info = []
	for reason in [
		'tried_by_opponent',
		'reviewed_by_opponent',
		'opposed_by_reporter',
		'reviewed_by_reporter',
		'tried_by_reporter',
	]:
		for problem in list(problems_dict):
			if len(problems_dict[problem][reason]) > 0:
				info.append((problem, problems_dict.pop(problem)))

	# And then we append all the other problems

	for problem in list(problems_dict):
		info.append((problem, problems_dict.pop(problem)))

	return bans, info


from django import forms


class TacticsForm(forms.Form):
	try:
		# This fails if no teams are registered (which is essentially for a new tournament)
		all_teams = Team.objects.all()
		team_choices = map(lambda team : (team.pk, team), all_teams)
		reporter_team = forms.ChoiceField(label='Reporter team', choices=team_choices)
		opponent_team = forms.ChoiceField(label='Opponent team', choices=team_choices)
	except:
		pass


@user_passes_test(ninja_test, redirect_field_name=None, login_url='/IPT%s/soon' % params.app_version)
@cache_page(cache_duration)
def build_tactics(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TacticsForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			tactics = sort_raw_tactics_data(build_tactics_for_two_teams(
				Team.objects.get(pk=form['reporter_team'].value()),
				Team.objects.get(pk=form['opponent_team'].value()),
			))
			tactics = (tactics[0][::-1], tactics[1])
			return render(request, 'IPT%s/build_tactics.html' % params.app_version, {
				'params': params,
				'form': form,
				'tactics': tactics,
			})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = TacticsForm()

	return render(request, 'IPT%s/build_tactics.html' % params.app_version, {'params': params, 'form': form})
# coding=utf8
import django
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import math

os.environ['DJANGO_SETTINGS_MODULE'] = "ipt_connect.settings"
django.setup()

from IPT2016.models import *
jurys = Jury.objects.all()



jurygrades = JuryGrade.objects.filter(round__pf_number=1) | JuryGrade.objects.filter(round__pf_number=2) | JuryGrade.objects.filter(round__pf_number=3) | JuryGrade.objects.filter(round__pf_number=4)  # discard the final

#jurygrades = JuryGrade.objects.filter(round__pf_number=1)

jurys = [jury for jury in jurys if len(jurygrades.filter(jury__name=jury.name))>=3 and jury.name != "Erwan Allys"]
jurys = sorted(jurys, key=lambda jury: jury.name)

#sys.exit()

teams = Team.objects.all()
teams = teams[0].ranking()[0][::-1]  # rank the teams (take some time)

plt.figure(figsize=(25, 16))
ax = plt.subplot(1, 1, 1)
ax.set_xticks(np.arange(len(teams)))
ax.set_xticklabels([team.name for team in teams])

ax.set_yticks(np.arange(len(jurys)))
ax.set_yticklabels([jury.name for jury in jurys])
for i in np.arange(len(jurys)):
	ax.axhline(i, ls='--', alpha=0.5, color='grey')


for indt, team in enumerate(teams):
	team.jurys = []
	mygrades = jurygrades.filter(round__reporter_team__name=team.name) | jurygrades.filter(round__opponent_team__name=team.name) | jurygrades.filter(round__reviewer_team__name=team.name)
	for indj, jury in enumerate(jurys):
		if indt == 0:
			jury.gradscatters = []

		jgrades = mygrades.filter(jury__name=jury.name)
		# vals contains the grade put by a specific jury member to a specific team
		vals = [] # each element contains (grade in a specific fight, scatter from mean grade in this fight, role coefficient)
		for jgrade in jgrades:
			if jgrade.round.reporter_team.name == team.name:
				repgrades = [jg.grade_reporter for jg in JuryGrade.objects.filter(round__reporter_team__name=team.name) if jg.round == jgrade.round]
				avggrade = np.mean(repgrades)
				vals.append((jgrade.grade_reporter, jgrade.grade_reporter-avggrade, 3))
			if jgrade.round.opponent_team.name == team.name:
				oppgrades = [jg.grade_opponent for jg in JuryGrade.objects.filter(round__opponent_team__name=team.name) if jg.round == jgrade.round]
				avggrade = np.mean(oppgrades)
				vals.append((jgrade.grade_opponent, jgrade.grade_opponent-avggrade, 2))
			if jgrade.round.reviewer_team.name == team.name:
				revgrades = [jg.grade_reviewer for jg in JuryGrade.objects.filter(round__reviewer_team__name=team.name) if jg.round == jgrade.round]
				avggrade = np.mean(revgrades)
				vals.append((jgrade.grade_reviewer, jgrade.grade_reviewer-avggrade, 1))

		gradscatters = []
		grads = []
		for v in vals:
			for ind in np.arange(v[2]):
				gradscatters.append(v[1])
				grads.append(v[0])

		jury.gradscatters.append(np.mean(gradscatters))
		if np.mean(gradscatters) >= 0:
			color='royalblue'
		elif np.mean(gradscatters) < 0:
			color='crimson'
		maxscatter=1.0
		if len(grads) > 0 :
			ax.scatter(indt, indj, s=np.sum([v[2] for v in vals]*15), c=color, alpha=max(min(np.abs(np.mean(gradscatters))/maxscatter, 1), 0.4), linewidths=0.2)
			team.jurys.append(jury) # jurys that have judged team

maxscatter = 1.0
jcolors = []
jalphas = []
for jury in jurys:
	if np.nanmean(jury.gradscatters) >= 0:
		color='royalblue'
	elif np.nanmean(jury.gradscatters) < 0:
		color='crimson'
	alpha=max(min(np.abs(np.nanmean(jury.gradscatters))/maxscatter, 1), 0.6)
	jcolors.append(color)
	jalphas.append(alpha)

[t.set_color(jcolors[ind]) for ind, t in enumerate(ax.yaxis.get_ticklabels())]
[t.set_alpha(jalphas[ind]) for ind, t in enumerate(ax.yaxis.get_ticklabels())]

tcolors = []
talphas = []
tvals = []
maxscatter = 0.5
for team in teams:
	if np.nanmean([np.nanmean(jury.gradscatters) for jury in team.jurys]) >= 0:
		color='royalblue'
	elif np.nanmean([np.nanmean(jury.gradscatters) for jury in team.jurys]) < 0:
		color='crimson'
	val = np.nanmean([np.nanmean(jury.gradscatters) for jury in team.jurys])
	alpha = max(min(np.abs(np.nanmean([np.nanmean(jury.gradscatters) for jury in team.jurys]))/maxscatter, 1), 0.7)
	tcolors.append(color)
	talphas.append(alpha)
	tvals.append(val)

ax.set_xticklabels([team.name + '\n' + str("%.2f" % tvals[ind]) for ind, team in enumerate(teams)])
[t.set_color(tcolors[ind]) for ind, t in enumerate(ax.xaxis.get_ticklabels())]
[t.set_alpha(talphas[ind]) for ind, t in enumerate(ax.xaxis.get_ticklabels())]

plt.show()
sys.exit()

plt.show()
sys.exit()
# first easy thing, look at the mean, median and std of every jury grade distrbution
for jury in jurys:

	mygrades = JuryGrade.objects.filter(jury__name=jury.name)

	#if len(mygrades) == 0:
		#continue

	grades_rep = [grade.grade_reporter for grade in mygrades]
	grades_opp = [grade.grade_opponent for grade in mygrades]
	grades_rev = [grade.grade_reviewer for grade in mygrades]
	grades_all = grades_rep + grades_opp + grades_rev

	jury.mean_rep = np.mean(grades_rep)
	jury.mean_opp = np.mean(grades_opp)
	jury.mean_rev = np.mean(grades_rev)
	jury.mean_all = np.mean(grades_all)

	jury.std_rep = np.std(grades_rep)
	jury.std_opp = np.std(grades_opp)
	jury.std_rev = np.std(grades_rev)
	jury.std_all = np.std(grades_all)

	jury.med_rep = np.median(grades_rep)
	jury.med_opp = np.median(grades_opp)
	jury.med_rev = np.median(grades_rev)
	jury.med_all = np.median(grades_all)


meds_rep = [jury.med_rep for jury in jurys if not math.isnan(jury.med_rep)]
meds_opp = [jury.med_opp for jury in jurys if not math.isnan(jury.med_opp)]
meds_rev = [jury.med_rev for jury in jurys if not math.isnan(jury.med_rev)]
meds_all = [jury.med_all for jury in jurys if not math.isnan(jury.med_all)]

stds_rep = [jury.std_rep for jury in jurys if not math.isnan(jury.std_rep)]
stds_opp = [jury.std_opp for jury in jurys if not math.isnan(jury.std_opp)]
stds_rev = [jury.std_rev for jury in jurys if not math.isnan(jury.std_rev)]
stds_all = [jury.std_all for jury in jurys if not math.isnan(jury.std_all)]


if 0:
	# medians
	title = "jury members with at least 12 PFs"
	plt.figure(figsize=(8, 10))
	plt.subplot(4,1,1)
	plt.hist(meds_rep, bins=20, color="sage", label='reporter')
	plt.legend()
	plt.ylabel("#", fontsize=14)
	plt.title(title, fontsize =18)
	plt.subplot(4,1,2)
	plt.hist(meds_opp, bins=20, color="crimson", label='opponent')
	plt.ylabel("#", fontsize=14)
	plt.legend()
	plt.subplot(4,1,3)
	plt.hist(meds_rev, bins=20, color="gray", label='reviewer')
	plt.ylabel("#", fontsize=14)
	plt.legend()
	plt.subplot(4,1,4)
	plt.hist(meds_all, bins=20, color="royalblue", label='all grades')
	plt.xlabel("Median of jury member grades", fontsize=14)
	plt.ylabel("#", fontsize=14)
	plt.legend()


	# standard deviations
	title = "jury members with at least 12 PFs"
	plt.figure(figsize=(8, 10))
	plt.subplot(4,1,1)
	plt.hist(stds_rep, bins=20, color="sage", label='reporter')
	plt.legend()
	plt.ylabel("#", fontsize=14)
	plt.title(title, fontsize =18)
	plt.subplot(4,1,2)
	plt.hist(stds_opp, bins=20, color="crimson", label='opponent')
	plt.ylabel("#", fontsize=14)
	plt.legend()
	plt.subplot(4,1,3)
	plt.hist(stds_rev, bins=20, color="gray", label='reviewer')
	plt.ylabel("#", fontsize=14)
	plt.legend()
	plt.subplot(4,1,4)
	plt.hist(stds_all, bins=20, color="royalblue", label='all grades')
	plt.xlabel("Standard deviation of jury member grades ", fontsize=14)
	plt.ylabel("#", fontsize=14)
	plt.legend()

	# meds vs std
	title = "jury members with at least 12 PFs"
	plt.figure(figsize=(8, 10))
	plt.subplot(4,1,1)
	plt.scatter(meds_rep, stds_rep, s=60, color="sage", label='reporter')
	plt.legend()
	plt.ylabel("Std", fontsize=14)
	plt.title(title, fontsize =18)
	plt.subplot(4,1,2)
	plt.scatter(meds_opp, stds_opp, s=60, color="crimson", label='opponent')
	plt.ylabel("Std", fontsize=14)
	plt.legend()
	plt.subplot(4,1,3)
	plt.scatter(meds_rev, stds_rev, s=60, color="grey", label='reviewer')
	plt.ylabel("Std", fontsize=14)
	plt.legend()
	plt.subplot(4,1,4)
	plt.scatter(meds_all, stds_all, s=60, color="royalblue", label='all grades')
	plt.xlabel("Median of jury member grades", fontsize=14)
	plt.ylabel("Std", fontsize=14)
	plt.legend()












plt.show()

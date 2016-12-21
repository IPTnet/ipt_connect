# coding: utf8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from uuid import uuid4
from django.utils.encoding import iri_to_uri
from string import replace
import sys
from django.utils.deconstruct import deconstructible


def mean(vec):
	return float(sum(vec)) / len(vec)


@deconstructible
class UploadToPathAndRename(object):

	def __init__(self, path):
		self.sub_path = path

	def __call__(self, instance, filename):
		ext = filename.split('-')[-1]
		# get filename
		if instance.pk:
			filename = iri_to_uri(replace((u'{}_{}_{}.{}').format(instance.team,instance.surname,instance.name, ext),' ','_'))
		else:
			# set filename as random string
			filename = '{}.{}'.format(uuid4().hex, ext)
		# return the whole path to the file
		return os.path.join(self.sub_path, filename)


class Participant(models.Model):

	"""
	This class represent the basic model of our program, a participant.
	It can be a student competing, a team-leader, a jury member, an IOC or an external jury or even a staff, basically anyone taking part in the tournament."""


	GENDER_CHOICES = ( ('M','Male'), ('F','Female'),  ('D','Decline to report'))

	ROLE_CHOICES = ( ('TM','Team Member'), ('TC','Team Captain'), ('TL','Team Leader'), ('ACC','Accompanying') )

	DIET_CHOICES = ( ('NO','No specific diet'), ('NOPORK','No pork'), ('NOMEAT','No meat'), ('NOFISH','No fish'), ('NOMEAT_NOEGG','No meat, No eggs') )

	SHIRT_SIZES = (
		('S', 'Small'),
		('M', 'Medium'),
		('L', 'Large'),
		('XL', 'Extra Large'),
	)

	# parameters
	name = models.CharField(max_length=50,default=None,verbose_name='Nom')
	surname = models.CharField(max_length=50,default=None,verbose_name='Prénom')
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
	email = models.EmailField(help_text='This address will be used to send the participant every important infos about the tournament.')
	birthdate = models.DateField(default='1900-01-31')
	photo = models.ImageField(upload_to=UploadToPathAndRename('FPT2017/id_photo'),help_text='Please use a clear ID photo. This will be used for badges and transportation cards.', null=True)
	team = models.ForeignKey('Team', null=True)
	role = models.CharField(max_length=20,choices=ROLE_CHOICES,help_text='The Team Captain is one of the students (only one).The Team Leaders are the supervisors (up to two).', default="TM")
	affiliation = models.CharField(max_length=50,default='XXX University')
	veteran = models.BooleanField(default=False,help_text='Has the participant already participated in the IPT?')
	#diet = models.CharField(max_length=20,choices=DIET_CHOICES,help_text='Does the participant have a specific diet?')
	#shirt_size = models.CharField(max_length=2,choices=SHIRT_SIZES)
	remark = models.TextField(blank=True)


	# functions
	def fullname(self):
		"""
		:return: return the full name of the participant
		"""
		return self.name+' '+self.surname

	def __unicode__(self):
		"""
		:return: return the full name of the participant
		"""
		return self.fullname()

	def compute_average_grades(self, pfnumber=None, rounds=None, verbose=False):
		"""
		I collect all the grades from the Jury members that are addressed to me and compute the average grade for each physic fight

		:param verbose: verbosity of the function
		:param pfnumber: Physics Fight to consider. If None, I consider all the physics fights.
		:param rounds: rounds to consider. Has to priority over the pfnumber param. If None, I consider pfnumber.
		:return: I return a list of dictionaries, each of them with the following fields: {"value", "round", "role"}
		"""
		#TODO: find a way to credit the points to the second reporter as well, without adding them to the total amount of team points (maybe this issue should be in the Team class ????)

		average_grades=[]

		# get all the grades that concerns me
		if verbose:
			print "="*20,"Personal History","="*20
			print "My name is", self.name, self.surname
		jurygrades = JuryGrade.objects.filter(round__reporter=self) | JuryGrade.objects.filter(round__opponent=self) | JuryGrade.objects.filter(round__reviewer=self)

		# get all the rounds I'm in
		if rounds != None:
			myrounds = list(set([jurygrade.round for jurygrade in jurygrades if jurygrade.round in rounds]))
			if verbose:
				print "I consider only the Rounds in the given subset that I've played on:"

		else:
			if pfnumber == None:
				myrounds = list(set([jurygrade.round for jurygrade in jurygrades]))
				if verbose:
					print "I consider all the Rounds played so far."
			else:
				assert pfnumber in [1, 2, 3, 4, 5], "Your pfnumber is %i. This is odd." % (pfnumber)
				myrounds = list(set([jurygrade.round for jurygrade in jurygrades if jurygrade.round.pf_number == pfnumber]))
				if verbose:
					print "I consider only the Rounds from Physics Fight %i" % int(pfnumber)


		if verbose:
			print "I played in %i Rounds" % len(myrounds)


		for myround in myrounds:
			# get my role in this round:
			if myround.reporter == self:
				role = 'reporter'
				roundgrades = list(sorted([jurygrade.grade_reporter for jurygrade in jurygrades if jurygrade.round == myround]))

			elif myround.opponent == self:
				role = 'opponent'
				roundgrades = list(sorted([jurygrade.grade_opponent for jurygrade in jurygrades if jurygrade.round == myround]))
			elif myround.reviewer == self:
				role = 'reviewer'
				roundgrades = list(sorted([jurygrade.grade_reviewer for jurygrade in jurygrades if jurygrade.round == myround]))
			else:
				print myround
				print myround.reporter.fullname()
				print myround.opponent.fullname()
				print myround.reviewer.fullname()
				print self.fullname
				print "Something wrong here...I must have a defined role !"
				sys.exit()


			if verbose:
				print "In %s, I was the %s" % (myround, role)

			# Rule for grade rejection: divide the number of jury by 4.
			# Round the result (if result is X.5, round up to X+1)
			# If the result is even, reject result/2 lowest and result/2 highest marks
			# If the result is odd, reject result/2 + 0.5 lowest and result/2 - 0.5 highest marks.
			# Example : 7 jury members --> /4 = 1.75 --> round = 2 --> reject 1 highest and 1 lowest marks


			if len(roundgrades) in [5, 6]:
				nreject = 1
			elif len(roundgrades) in [7, 8]:
				nreject = 2
			else:
				nreject = round(len(roundgrades) / 4.0)

			if round(nreject / 2.0) == nreject / 2.0:
				nlow = int(nreject / 2.0)
				nhigh = int(nlow)
			else:
				nlow = int(nreject / 2.0 + 0.5)
				nhigh = int(nreject / 2.0 - 0.5)

			if verbose:
				print "\t%i Jury Members graded me" % len(roundgrades)
				print "\t%i lowest mark(s) and %i highest mark(s) are discarded"  % (nlow, nhigh)

			i = 0
			while i < nhigh:
				roundgrades.pop(-1)
				i += 1

			i = 0
			while i < nlow:
				roundgrades.pop(0)
				i += 1

			average_grades.append({"value": mean(roundgrades), "round":myround, "role":role})
			if verbose:
				print '\tI scored %.2f points' % mean(roundgrades)

		# return the average grade for all physics fight
		return average_grades

	def points(self, pfnumber=None, rounds=None, verbose=False):
		"""
		:param verbose: verbosity of the function
		:param pfnumber: physics fights to consider. If None, I consider all the physics fights
		:param rounds: rounds to consider. Has to priority over the pfnumber param. If None, I consider pfnumber.
		:return: Return the number of points gathered by a single participant. The multiplicative coefficient associated to his/her role is not taken into account here.
		"""
		points = 0.0
		average_grades = self.compute_average_grades(verbose=verbose, pfnumber=pfnumber, rounds=rounds)
		if verbose:
			if pfnumber == None:
				print "="*20, "Overall Summary", "="*20
			else:
				print "="*20, "Summary of Physics Fight %s" % pfnumber, "="*20
		for grade in average_grades:
			points += grade["value"]
			if verbose:
				print "In %s, I gathered %.2f points as a %s" % (grade["round"], grade["value"], grade["role"])
		if verbose:
			print "In total, I gathered %.2f points" % points
		return points


	def ranking(self, pool='all', pfnumber=None, rounds=None, verbose=True):
		"""
		:param pool: can be "team", "gender" or "all". Select the participant you want to be ranked with
		:param pfnumber: physics fights to consider. If None, I consider all the physics fights
		:param rounds: rounds to consider. Has to priority over the pfnumber param. If None, I consider pfnumber.
		:param verbose: verbosity of the function
		:return: return a tuple whose first element is an ordered list of participants according to the number of points they gathered, and second element is the current participant's ranking in this list
		"""

		# select only the real participants, not the accompanying persons, IOC, team-leader, etc...
		participants = Participant.objects.filter(role='TM') | Participant.objects.filter(role='TC')

		if pool == 'team':
			participants = participants.filter(team=self.team)
		elif pool == 'gender':
			participants = participants.filter(gender=self.gender)
		elif pool == 'all':
			participants = participants
		else:
			print "pool value does not compute"
			sys.exit()

		participants = sorted(participants, key=lambda x : x.points(pfnumber=pfnumber, rounds=rounds, verbose=verbose))[::-1]

		if verbose:
			print "="*20, "Ranking", "="*20
			for ind, participant in enumerate(participants):

				if participant==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+unicode(participant.fullname())+" - "+str(participant.points(pfnumber=pfnumber, rounds=rounds, verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+unicode(participant.fullname())+" - "+str(participant.points(pfnumber=pfnumber, rounds=rounds, verbose=False))+" points"
					print msg

		return participants, participants.index(self)+1



class Problem(models.Model):
	"""
	This model represents one of the 17 problems
	"""
	name = models.CharField(max_length=50, default=None)
	description = models.CharField(max_length=500, default=None)
	def __unicode__(self):
		return self.name

	def status(self, verbose=True, meangradesonly=False):
		"""

		:return:
		"""

		# first, get a list of who presented what
		rounds = Round.objects.filter(problem_presented=self)
		reporters = []
		opponents = []
		reviewers = []
		for round in rounds:
			if len(JuryGrade.objects.filter(round=round)) > 0:
				reporterinfo = round.reporter.compute_average_grades(rounds=[round], verbose=verbose)[0]
				opponentinfo = round.opponent.compute_average_grades(rounds=[round], verbose=verbose)[0]
				reviewerinfo = round.reviewer.compute_average_grades(rounds=[round], verbose=verbose)[0]
				reporters.append({"name": round.reporter.team.name, "round": reporterinfo["round"], "value": reporterinfo["value"]})
				opponents.append({"name": round.opponent.team.name, "round": opponentinfo["round"], "value": opponentinfo["value"]})
				reviewers.append({"name": round.reviewer.team.name, "round": reviewerinfo["round"], "value": reviewerinfo["value"]})

		# use this to compute the mean grades
                if 0 in [len(reporters), len(opponents), len(reviewers)]:
                        meangrades = {"report": 0, "opposition": 0, "review": 0}
                else:
                        meangrades = {"report": mean([reporter["value"] for reporter in reporters]), "opposition": mean([opponent["value"] for opponent in opponents]), "review": mean([reviewer["value"] for reviewer in reviewers])}


		if meangradesonly==False:
			# then, reorder that list per teams
			myteamsnames = list(sorted([elt["name"] for elt in reporters+opponents+reviewers]))

			teamresults = []
			for name in myteamsnames:
				if not name in [teamresult["name"] for teamresult in teamresults]:
					teamresult = {}
					teamresult["name"] = name

					# They can be multiple report/oppos/review on the same problem by the same team !!!
					reports=[]
					oppositions=[]
					reviews=[]
					# get the scores from presentations
					for reporter in reporters:
						if reporter["name"] == name:
							reports.append({"round": reporter["round"], "value": reporter["value"]})
					# get the scores from oppositions
					for opponent in opponents:
						if opponent["name"] == name:
							oppositions.append({"round": opponent["round"], "value": opponent["value"]})
					# get the scores from reviews
					for reviewer in reviewers:
						if reviewer["name"] == name:
							reviews.append({"round": reviewer["round"], "value": reviewer["value"]})

					teamresult["reports"] = reports
					teamresult["oppositions"] = oppositions
					teamresult["reviews"] = reviews

					teamresults.append(teamresult)
				else:
					pass

			return (meangrades, teamresults)
		else:
			return meangrades


class Team(models.Model):
	"""
	This model represent a team, to which all the participants belong to
	"""

	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50, null=True, blank=True, default=None)
	IOC = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='Team_FPT2017')
	def __unicode__(self):

		return self.name

	def presentation_coefficients(self, verbose=False):
		"""
		Modify the presentation coefficient from a given round up to the end of the physics fights if more than three problems are tactically rejected.

		The coefficient loses 0.2 points for every additional rejection. This penality is carried over all the subsequents rounds, but disappear for the Final

		:param verbose: Verbosity flag
		:return: Return a list with the coefficient for every round
		"""

		pfs = [1, 2, 3, 4]
		eternalrejections = EternalRejection.objects.filter(round__reporter__team=self)

		beforetactical = []
		netrej = 0
		for pf in pfs:
			netrej += len(eternalrejections.filter(round__pf_number=pf))
			beforetactical.append(3.0 - 0.2*max(0, (netrej-1)))


		# get all the tactical rejections
		rejections = TacticalRejection.objects.filter(round__reporter__team=self)



		prescoeffs = []
		npenalities = 0
		if verbose:
			print "="*20, "Tactical Rejection Penalites for Team %s" % self.name, "="*20
		for ind, pf in enumerate(pfs):
			pfrejections = [rejection for rejection in rejections if rejection.round.pf_number == pf]
			if verbose:
				print "%i tactical rejections by Team %s in Physics Fight %i" % (len(pfrejections), self, pf)
			if len(pfrejections) > 3:
				npenalities += len(pfrejections) - 3
			if verbose:
				if npenalities > 0:
					print "Penality of %.1f points on the Reporter Coefficient" %  float(0.2*npenalities)
				else:
					print "No penality"
			prescoeffs.append(beforetactical[ind] - 0.2 * npenalities)

		# add the coeff for the final, 3.0 by default
		prescoeffs.append(3.0)
		return prescoeffs

	# functions
	def bonuspoints(self, pfnumber=None, rounds=None, verbose=False, maxround=3):
		"""
		Check if the pfs where I played are complete, and return the according number of bonus points (2 if first, 1 if second, split equally if ex-aequo)

		:param verbose: verbosity of the function
		:param maxpf: maximum number of physics fight per round
		:return: Return the number of bonus points
		"""

		# get all the rounds where my participants are involved in
		rounds = Round.objects.filter(reporter__team=self) | Round.objects.filter(opponent__team=self) | Round.objects.filter(reviewer__team=self)
		mypfnumbers = [1, 2, 3, 4]

		bonuspoints = []
		for mypfnumber in mypfnumbers:
			pfrounds = rounds.filter(pf_number=mypfnumber) # for a given round, I am always in the same room

			# refine to match user params
			if rounds != None:
				pfrounds = [round for round in pfrounds if round in rounds]
			elif roundnumber != None:
				pfrounds = [round for round in rounds if round.pf_number == pfnumber]
			else:
				pass

			assert len(pfrounds) <= maxround, "Team %s played %s rounds in Physics Fight %s. Check your database!" % (self.name, str(len(pfrounds)), str(mypfnumber))
			if len(pfrounds) == maxround: # then all the fights are played
				teams = [pfrounds[0].reporter.team, pfrounds[0].opponent.team, pfrounds[0].reviewer.team]
				if verbose:
					print "="*20, "Bonus Points", "="*20
					print "PF %i opposes teams from %s, %s and %s" % (int(mypfnumber), teams[0].name, teams[1].name, teams[2].name)
				results = []
				for team in teams:
					prescoeff = team.presentation_coefficients(verbose=False)
					teampfpoints = 0
					for participant in Participant.objects.filter(team=team):
						average_grades = participant.compute_average_grades(pfnumber=mypfnumber, rounds=pfrounds, verbose=False)
						for grade in average_grades:
							if grade["role"] == "reporter":
								teampfpoints += grade["value"] * prescoeff[grade["round"].pf_number - 1]
							elif grade["role"] == "opponent":
								teampfpoints += grade["value"] * 2.0
							elif grade["role"] == "reviewer":
								teampfpoints += grade["value"]
							else:
								print "Role undefined : %s" % grade["role"]
								sys.exit()
					if verbose:
						print "Team %s gathered %.2f points in Physics Fight %i" % (team.name, teampfpoints, int(mypfnumber))
					results.append({"name": team.name, "points": teampfpoints})

				results = sorted(results, key=lambda x: x["points"])[::-1]

				# Now finally give the bonus point
				if verbose:
					print "PF %i ranking:" % mypfnumber
				for ind, result in enumerate(results):
					if result["name"] == self.name:
						# If everyone is ex-aequo
						if results[0]["points"] == results[1]["points"] and results[1]["points"] == results[2]["points"]:
							bonuspoint=1.0
						# If 1 and 2 are ex-aequo
						elif ind in [0,1] and results[0]["points"] == results[1]["points"]:
							bonuspoint=1.5
						# If I win the pf
						elif ind==0 and results[1]["points"] < results[0]["points"]:
							bonuspoint=2.0
						# If 2 and 3 are ex-aequo
						elif ind in [1,2] and results[1]["points"] == results[2]["points"]:
							bonuspoint=0.5
						# If I am second
						elif ind==1 and results[1]["points"] > results[2]["points"]:
							bonuspoint=1.0
						# all the rest got nothing
						else:
							bonuspoint=0.0

					if verbose:
						msg = "\t%i) Team %s -- %.2f points" % (ind+1, result["name"], result["points"])
						if result["name"] == self.name:
							print '\x1b[32m%s\x1b[0m' % msg

						else:
							print msg
				if verbose:
					print "On top of that, team %s wins %.1f additional bonus point(s)" % (self.name, bonuspoint)
				bonuspoints.append(bonuspoint)

			else:  # Not all the rounds are played, I skip
				if verbose:
					print "Not all rounds in PF %i have been played yet!" % int(mypfnumber)
				bonuspoints.append(0.0)

		return bonuspoints


	def points(self, pfnumber=None, rounds=None, verbose=False, bonuspoints=True):
		"""
		I get all the participants that are in my team and sum their average grades, multiplied by their roles.
		If all the fights from a round are played, I add the corresponding bonus points

		:return: Return the total number of points of self
		"""

		participants = Participant.objects.filter(team=self)
		if verbose:
			print "="*20, "Points of Team %s" % self.name, "="*20
			print "There are %i participants" % (len(participants))

		allpoints = 0
		for participant in participants:
			points = 0
			if verbose:
				if pfnumber==None:
					msg = 'In overall, I scored'
				else:
					msg = 'In PF %i, I scored' % int(pfnumber)
			average_grades = participant.compute_average_grades(pfnumber=pfnumber, rounds=rounds, verbose=verbose)
			prescoeff = self.presentation_coefficients(verbose=False)
			for grade in average_grades:
				if grade["role"] == "reporter":
					pfprescoeff = prescoeff[grade["round"].pf_number - 1]
					points += grade["value"]*pfprescoeff
					if verbose:
						msg+='\n\t%.2f*%.1f = %.2f points as a reporter,' % (grade["value"], pfprescoeff, grade["value"]*pfprescoeff)
				elif grade["role"] == "opponent":
					points += grade["value"]*2.0
					if verbose:
						msg+='\n\t%.2f*2 = %.2f points as an opponent,' % (grade["value"], grade["value"]*2)
				elif grade["role"] == "reviewer":
					points += grade["value"]
					if verbose:
						msg+='\n\t%.2f points as a reviewer,' % (grade["value"])

				else:
					print "Something wrong here...my role is not defined !"
					sys.exit()

			if verbose:
				msg+='\nfor a total of %.2f points' % points
				print msg
			allpoints += points

		# add bonus points for winning rounds, etc...
		if bonuspoints:
			allpoints += sum(self.bonuspoints(pfnumber=pfnumber, rounds=rounds, verbose=verbose))


		if verbose:
			print "Team %s has %.2f points so far !"  % (self.name, allpoints)
		return allpoints

	def ranking(self, pfnumber=None, rounds=None, verbose=False, selectedteams=None):
		"""
		:param verbose:  Verbosity flag
		:return: (teams, position of self). Return all the teams, ranked by points and return my position amongst the rank.
		"""

		if selectedteams:
			teams = [team for team in Team.objects.all() if team.name in selectedteams]
			if verbose:
				print "I select only %i teams:" % len(selectedteams)
				for team in selectedteams:
					print team.name
		else:
			teams = Team.objects.all()

		# exclude the IOC team

		teams = sorted(teams, key=lambda x : x.points(pfnumber=pfnumber, rounds=rounds, verbose=verbose))[::-1]
		if verbose:
			print "="*20, "Team Ranking", "="*20
			for ind, team in enumerate(teams):
				if team==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(pfnumber=pfnumber, rounds=rounds, verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(pfnumber=pfnumber, rounds=rounds, verbose=False))+" points"
					print msg

		return teams, teams.index(self)+1

	def problems(self, verbose=False, currentround=None):
		"""
		Get all the problems that I cannot present(already presented or eternal rejection) and cannot oppose(already opposed)

		:param verbose: verbosity Flag
		:param currentround: A Round instance. Return all the unpresentable problems before the current round. If none, return on all the round. This sentence is terribly unclear. Rephrase.

		:return: tuple of three lists. each list contains the problems that are eternally rejected, already presented and already opposed
		"""

		if verbose:
			print "="*20, "Problems of Team %s" % self.name, "="*20
		noproblems=[]

		if currentround !=None:
			pf_number = currentround.pf_number
		else: #TODO: remove these stupid 999 values and implement the pf rejection properly
			round_number = 999

		# the eternal rejection
		eternal_rejections = EternalRejection.objects.filter(round__reporter__team=self)
		# assert len(eternal_rejections) < 2, "Team %s has more than one eternal rejection. This is forbidden!" % self.name
		# Well, apparently it is...
		reject = []
		if len(eternal_rejections) > 0 and eternal_rejections[0].round.pf_number < pf_number:
			if verbose:
				print "Team %s rejected eternally problem %s" %(self.name, eternal_rejections[0].problem.name)
			reject.append(eternal_rejections[0].problem)
		noproblems.append(reject)

		# now all the problems already presented
		rounds = Round.objects.filter(reporter__team=self)
		rounds = [round for round in rounds if round.pf_number < pf_number]
		presented = []
		for round in rounds:
			if verbose:
				print "In %s, I presented problem %s" % (round, round.problem_presented)
			presented.append(round.problem_presented)
		noproblems.append(presented)

		# and problems already opposed
		rounds = Round.objects.filter(opponent__team=self)
		rounds = [round for round in rounds if round.pf_number < pf_number]
		opposed = []
		for round in rounds:
			if verbose:
				print "In %s, I opposed problem %s" % (round, round.problem_presented)
			opposed.append(round.problem_presented)
		noproblems.append(opposed)

		assert len(noproblems) == 3, "Something wrong with your rejected problem..."
		return noproblems




class Room(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

	def ident(self):
		rooms = Room.objects.all()
		for ind, room in enumerate(rooms):
			if room==self:
				return ind+1

class Jury(models.Model):
	name = models.CharField(max_length=50)
	team = models.ForeignKey('Team', null=True, blank=True)

	def __unicode__(self):
		return self.name

class Round(models.Model):

	pf_number = models.IntegerField(
			choices=(((ind+1, 'Fight '+str(ind+1)) for ind in range(5))),
			default=None
			)
	round_number = models.IntegerField(
			choices=(((ind+1, 'Round '+str(ind+1)) for ind in range(4))),
			default=None
			)
	room = models.ForeignKey(Room)
	reporter_team = models.ForeignKey(Team, related_name='reporterteam', blank=True, null=True)
	opponent_team = models.ForeignKey(Team, related_name='opponentteam', blank=True, null=True)
	reviewer_team = models.ForeignKey(Team, related_name='reviewerteam', blank=True, null=True)
	reporter = models.ForeignKey(Participant, related_name='reporter_name_1', blank=True, null=True)
	reporter_2 = models.ForeignKey(Participant, blank=True, null=True, related_name='reporter_name_2')
	opponent = models.ForeignKey(Participant, related_name='opponent_name', blank=True, null=True)
	reviewer = models.ForeignKey(Participant, related_name='reviewer_name', blank=True, null=True)
	problem_presented = models.ForeignKey(Problem, blank=True, null=True)
	submitted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

	def __unicode__(self):
		return "Fight %i | Round %i | Room %s" % (self.pf_number, self.round_number, self.room.name)

	def ident(self):
		return "%s%s%s" %(self.pf_number, self.round_number, self.room.ident())

	def unavailable_problems(self, verbose=False):
		"""
		From the rules:

		The Opponent may challenge the Reporter on any problem with the exception of a problem that:
		a) was permanently rejected by the Reporter earlier;
		b) was presented by the Reporter earlier;
		c) was opposed by the Opponent earlier;
		d) was presented by the Opponent earlier.
		If there are no problems left to challenge, the bans d), c), b), a) are successively removed, in that order.

		:param verbose: verbosity flag
		:return: return a tuple with five lists : ([already_presented_this_round], [a], [b], [c], [d])
		"""

		# remind that these below are ([eternal rejection], [presented], [opposed])
		reporter_problems = self.reporter_team.problems(verbose=False, currentround=self)
		opponent_problems = self.opponent_team.problems(verbose=False, currentround=self)
		eternal_rejection = reporter_problems[0]

		if verbose:
			print "="*10, "Problem rejection for %s" % self, "="*10
			if len(eternal_rejection) != 0:
				print "Team %s eternally rejected problem \n\t%s" % (self.reporter_team, eternal_rejection[0])
		presented_by_reporter = reporter_problems[1]
		if verbose:
			msg = "Team %s already presented the following problems:" % self.reporter_team
			for problem in presented_by_reporter:
				msg += "\n\t%s" % problem
			print msg
		opposed_by_opponent = opponent_problems[2]
		if verbose:
			msg = "Team %s already opposed the following problems:" % self.opponent_team
			for problem in opposed_by_opponent:
				msg += "\n\t%s" % problem
			print msg
		presented_by_opponent = opponent_problems[1]
		if verbose:
			msg = "Team %s already presented the following problems:" % self.opponent_team
			for problem in presented_by_opponent:
				msg += "\n\t%s" % problem
			print msg

		# Finally, problems already presented in this Fight, in the current room
		thispfrounds = Round.objects.filter(pf_number=self.pf_number).filter(room=self.room)
		presented_this_pf = [round.problem_presented for round in thispfrounds if round.round_number < self.round_number]
		if verbose:
			msg = "In this fight, problems already presented are:"
			for problem in presented_this_pf:
				msg += "\n\t%s" % problem
			print msg

		unavailable_problems = {}
		unavailable_problems["presented_this_pf"] = [p for p in presented_this_pf if p != None]
		unavailable_problems["eternal_rejection"] = [p for p in eternal_rejection if p != None]
		unavailable_problems["presented_by_reporter"] = [p for p in presented_by_reporter if p != None]
		unavailable_problems["opposed_by_opponent"] = [p for p in opposed_by_opponent if p != None]
		unavailable_problems["presented_by_opponent"] = [p for p in presented_by_opponent if p != None]

		return unavailable_problems


class JuryGrade(models.Model):

	round = models.ForeignKey(Round, null=True)
	jury = models.ForeignKey(Jury)

	grade_reporter = models.IntegerField(
			choices=(((ind, ind) for ind in range(10+1))),
			default=None
			)

	grade_opponent = models.IntegerField(
			choices=(((ind, ind) for ind in range(10+1))),
			default=None
			)

	grade_reviewer = models.IntegerField(
			choices=(((ind, ind) for ind in range(10+1))),
			default=None
			)

	def __unicode__(self):
		return "Grade of %s" % self.jury.name

	def info(self):
		print "=" * 36
		print u"Grade of %s" % self.jury.name
		print self.round
		print "Reporter %s from %s : %i" % (self.round.name_reporter, self.round.reporter, self.grade_reporter)
		print "Opponent %s from %s : %i" % (self.round.name_opponent, self.round.opponent, self.grade_opponent)
		print "Reviewer %s from %s : %i" % (self.round.name_reviewer, self.round.reviewer, self.grade_reviewer)


class TacticalRejection(models.Model):

	round = models.ForeignKey(Round, null=True)
	problem = models.ForeignKey(Problem)

	def __unicode__(self):
		return "Problem rejected : %s" % self.problem

class EternalRejection(models.Model):

	round = models.ForeignKey(Round, null=True)
	problem = models.ForeignKey(Problem)

	def __unicode__(self):
		return "Problem rejected : %s" % self.problem

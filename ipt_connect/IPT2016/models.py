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
		ext = filename.split('.')[-1]
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

	TOURISM_CHOICES = ( ('TOURISM_0','No') , ('TOURISM_1','Yes, one night'), ('TOURISM_2','Yes, two nights') )

	SHIRT_SIZES = (
		('S', 'Small'),
		('M', 'Medium'),
		('L', 'Large'),
		('XL', 'Extra Large'),
	)

	# parameters
	name = models.CharField(max_length=50,default='Richard')
	surname = models.CharField(max_length=50,default='Feynman')
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
	email = models.EmailField(help_text='This address will be used to send the participant every important infos about the tournament.')
	birthdate = models.DateField(default='1900-01-31')
	photo = models.ImageField(upload_to=UploadToPathAndRename('id_photo'),help_text='Please use a clear ID photo. This will be used for badges and transportation cards.',null=True)
	team = models.ForeignKey('Team')
	role = models.CharField(max_length=20,choices=ROLE_CHOICES,help_text='The Team Captain is one of the students (only one).The Team Leaders are the supervisors (up to two).')
	passport_number = models.CharField(max_length=20)
	affiliation = models.CharField(max_length=50,default='XXX University')
	veteran = models.BooleanField(default=False,help_text='Has the participant already participated in the IPT?')
	diet = models.CharField(max_length=20,choices=DIET_CHOICES,help_text='Does the participant have a specific diet?')
	tourism=models.CharField(max_length=20,choices=TOURISM_CHOICES,help_text='Would the participant like to stay some more days in Paris after the tournament? Please note the LOC would only book the rooms, but would not pay for it!')
	shirt_size = models.CharField(max_length=2,choices=SHIRT_SIZES)
	mixed_dormitory = models.BooleanField(default=True,help_text='Is it ok for the participant to be in mixed dorm?')
	remark = models.TextField(blank=True)
	hotel_room = models.CharField(max_length=20,blank=True)
	check_in = models.BooleanField(default=False,help_text='Has the participant arrived?')


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

	def compute_average_grades(self, roundnumber=None, physicsfights=None, verbose=True):
		"""
		I collect all the grades from the Jury members that are addressed to me and compute the average grade for each physic fight

		:param verbose: verbosity of the function
		:param roundnumber: round to consider. If None, I consider all the rounds.
		:param physicsfights: physics fights to consider. Has to priority over the roundnumber param. If None, I consider roundnumber.
		:return: I return a list of dictionaries, each of them with the following fields: {"value", "pf", "role"}
		"""
		#TODO: find a way to credit the points to the second reporter as well, without adding them to the total amount of team points (maybe this issue should be in the Team class ????)

		average_grades=[]

		# get all the grades that concerns me
		if verbose:
			print "="*20,"Personal History","="*20
			print "My name is", self.name, self.surname
		jurygrades = JuryGrade.objects.filter(physics_fight__reporter__name=self.name) | JuryGrade.objects.filter(physics_fight__opponent__name=self.name) | JuryGrade.objects.filter(physics_fight__reviewer__name=self.name)

		# get all the physics fights I'm in
		if physicsfights != None:
			pfs = list(set([jurygrade.physics_fight for jurygrade in jurygrades if jurygrade.physics_fight in physicsfights]))
			if verbose:
				print "I consider only the Physics Fights in the given subset that I've played on:"

		else:
			if roundnumber == None:
				pfs = list(set([jurygrade.physics_fight for jurygrade in jurygrades]))
				if verbose:
					print "I consider all the Physics Fights played so far."
			else:
				assert roundnumber in [1, 2, 3, 4]
				pfs = list(set([jurygrade.physics_fight for jurygrade in jurygrades if jurygrade.physics_fight.round_number == roundnumber]))
				if verbose:
					print "I consider only the Physics Fights from Round %i" % int(roundnumber)


		if verbose:
			print "I played in %i Physics Fights" % len(pfs)


		for pf in pfs:

			# get my role in this physics fight:
			if pf.reporter.name == self.name and pf.reporter.surname == self.surname:
				role = 'reporter'
				pfgrades = list(sorted([jurygrade.grade_reporter for jurygrade in jurygrades if jurygrade.physics_fight == pf]))

			elif pf.opponent.name == self.name and pf.opponent.surname == self.surname:
				role = 'opponent'
				pfgrades = list(sorted([jurygrade.grade_opponent for jurygrade in jurygrades if jurygrade.physics_fight == pf]))
			elif pf.reviewer.name == self.name and pf.reviewer.surname == self.surname:
				role = 'reviewer'
				pfgrades = list(sorted([jurygrade.grade_reviewer for jurygrade in jurygrades if jurygrade.physics_fight == pf]))
			else:
				print "Something wrong here...I must have a defined role !"
				sys.exit()


			if verbose:
				print "In %s, I was the %s" % (pf, role)

			# Rule for grade rejection: divide the number of jury by 4.
			# Round the result (if result is X.5, round up to X+1)
			# If the result is even, reject result/2 lowest and result/2 highest marks
			# If the result is odd, reject result/2 + 0.5 lowest and result/2 - 0.5 highest marks.
			# Example : 7 jury members --> /4 = 1.75 --> round = 2 --> reject 1 highest and 1 lowest marks


			nreject = round(len(pfgrades) / 4.0)

			if round(nreject / 2.0) == nreject / 2.0:
				nlow = int(nreject / 2.0)
				nhigh = int(nlow)
			else:
				nlow = int(nreject / 2.0 + 0.5)
				nhigh = int(nreject / 2.0 - 0.5)

			if verbose:
				print "\t%i Jury Members graded me" % len(pfgrades)
				print "\t%i lowest mark(s) and %i highest mark(s) are discarded"  % (nlow, nhigh)

			i = 0
			while i < nhigh:
				pfgrades.pop(-1)
				i += 1

			i = 0
			while i < nlow:
				pfgrades.pop(0)
				i += 1

			average_grades.append({"value": mean(pfgrades), "pf":pf, "role":role})
			if verbose:
				print '\tI scored %.2f points' % mean(pfgrades)

		# return the average grade for all physics fight
		return average_grades

	def points(self, roundnumber=None, physicsfights=None, verbose=True):
		"""
		:param verbose: verbosity of the function
		:param roundnumber: round to consider. If None, I consider all the rounds
		:param physicsfights: physics fights to consider. Has to priority over the roundnumber param. If None, I consider roundnumber.
		:return: Return the number of points gathered by a single participant. The multiplicative coefficient associated to his/her role is not taken into account here.
		"""
		points = 0.0
		average_grades = self.compute_average_grades(verbose=verbose, roundnumber=roundnumber, physicsfights=physicsfights)
		if verbose:
			if roundnumber == None:
				print "="*20, "Overall Summary", "="*20
			else:
				print "="*20, "Summary of Round %s" % roundnumber, "="*20
		for grade in average_grades:
			points += grade["value"]
			if verbose:
				print "In %s, I gathered %.2f points as a %s" % (grade["pf"], grade["value"], grade["role"])
		if verbose:
			print "In total, I gathered %.2f points" % points
		return points


	def ranking(self, pool='all', roundnumber=None, physicsfights=None, verbose=True):
		"""
		:param pool: can be "team", "gender" or "all". Select the participant you want to be ranked with
		:param roundnumber: rounds to consider. If None, I consider all the PFs played so far.
		:param physicsfights: physics fights to consider. Has to priority over the roundnumber param. If None, I consider roundnumber.
		:param verbose: verbosity of the function
		:return: return a tuple whose first element is an ordered list of participants according to the number of points they gathered, and second element is the current participant's ranking in this list
		"""


		if pool == 'team':
			participants = Participant.objects.filter(team=self.team)
		elif pool == 'gender':
			participants = Participant.objects.filter(gender=self.gender)
		elif pool == 'all':
			participants = Participant.objects.all()
		else:
			print "pool value does not compute"
			sys.exit()

		participants = sorted(participants, key=lambda x : x.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=verbose))[::-1]

		if verbose:
			print "="*20, "Ranking", "="*20
			for ind, participant in enumerate(participants):

				if participant==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+unicode(participant.fullname())+" - "+str(participant.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+unicode(participant.fullname())+" - "+str(participant.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=False))+" points"
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


class Team(models.Model):
	"""
	This model represent a team, to which all the participants belong to
	"""

	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50, null=True, blank=True, default=None)
	IOC = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
	def __unicode__(self):

		return self.name

	def presentation_coefficients(self, verbose=True):
		"""
		Modify the presentation coefficient from a given round up to the end of the physics fights if more than three problems are tactically rejected.

		The coefficient loses 0.2 points for every additional rejection. This penality is carried over all the subsequents rounds, but disappear for the Final

		:param verbose: Verbosity flag
		:return: Return a list with the coefficient for every round
		"""

		# get all the tactical rejections
		rejections = TacticalRejection.objects.filter(physics_fight__reporter__team=self)
		rounds = [1, 2, 3, 4]

		prescoeffs = []
		npenalities = 0
		if verbose:
			print "="*20, "Tactical Rejection Penalites for Team %s" % self.name, "="*20
		for round in rounds:
			roundrejections = [rejection for rejection in rejections if rejection.physics_fight.round_number == round]
			if verbose:
				print "%i tactical rejections by Team %s in Round %i" % (len(roundrejections), self, round)
			if len(roundrejections) > 3:
				npenalities += len(roundrejections) - 3
			if verbose:
				if npenalities > 0:
					print "Penality of %.1f points on the Reporter Coefficient" %  float(0.2*npenalities)
				else:
					print "No penality"
			prescoeffs.append(3.0 - 0.2 * npenalities)

		return prescoeffs

	# functions
	def bonuspoints(self, roundnumber=None, physicsfights=None, verbose=True, maxpf=3):
		"""
		Check if the rounds where I played are complete, and return the according number of bonus points (2 if first, 1 if second, split equally if ex-aequo)

		:param verbose: verbosity of the function
		:param maxpf: maximum number of physics fight per round
		:return: Return the number of bonus points
		"""

		# get all the Physics Fights where my participants are involved in
		pfs = PhysicsFight.objects.filter(reporter__team=self) | PhysicsFight.objects.filter(opponent__team=self) | PhysicsFight.objects.filter(reviewer__team=self)
		myroundnumbers = [1, 2, 3, 4]

		bonuspoints = []
		for myroundnumber in myroundnumbers:
			roundpfs = pfs.filter(round_number=myroundnumber) # for a given round, I am always in the same room

			# refine to match user params
			if physicsfights != None:
				roundpfs = [pf for pf in roundpfs if pf in physicsfights]
			elif roundnumber != None:
				roundpfs = [pf for pf in roundpfs if pf.round_number == roundnumber]
			else:
				pass

			assert len(roundpfs) <= maxpf
			if len(roundpfs) == maxpf: # then all the fights are played
				teams = [roundpfs[0].reporter.team, roundpfs[0].opponent.team, roundpfs[0].reviewer.team]
				if verbose:
					print "="*20, "Bonus Points", "="*20
					print "Round %i opposes teams from %s, %s and %s" % (int(myroundnumber), teams[0].name, teams[1].name, teams[2].name)
				results = []
				for team in teams:
					prescoeff = team.presentation_coefficients(verbose=False)
					teamroundpoints = 0
					for participant in Participant.objects.filter(team=team):
						average_grades = participant.compute_average_grades(roundnumber=myroundnumber, physicsfights=physicsfights, verbose=False)
						for grade in average_grades:
							if grade["role"] == "reporter":
								teamroundpoints += grade["value"] * prescoeff[grade["pf"].round_number - 1]
							elif grade["role"] == "opponent":
								teamroundpoints += grade["value"] * 2.0
							elif grade["role"] == "reviewer":
								teamroundpoints += grade["value"]
							else:
								print "Role undefined : %s" % grade["role"]
								sys.exit()
					if verbose:
						print "Team %s gathered %.2f points in Round %i" % (team.name, teamroundpoints, int(myroundnumber))
					results.append({"name": team.name, "points": teamroundpoints})

				results = sorted(results, key=lambda x: x["points"])[::-1]

				# Now finally give the bonus point
				if verbose:
					print "Round %i ranking:" % myroundnumber
				for ind, result in enumerate(results):
					if result["name"] == self.name:
						# If everyone is ex-aequo
						if results[0]["points"] == results[1]["points"] and results[1]["points"] == results[2]["points"]:
							bonuspoint=1.0
						# If 1 and 2 are ex-aequo
						elif ind in [0,1] and results[0]["points"] == results[1]["points"]:
							bonuspoint=1.5
						# If I win the round
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

			else:  # Not all the fights are played, I skip
				if verbose:
					print "Not all physics fights in Round %i have been played yet!" % int(myroundnumber)
				bonuspoints.append(0.0)

		return bonuspoints


	def points(self, roundnumber=None, physicsfights=None, verbose=False):
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
				if roundnumber==None:
					msg = 'In overall, I scored'
				else:
					msg = 'In Round %i, I scored' % int(roundnumber)
			average_grades = participant.compute_average_grades(roundnumber=roundnumber, physicsfights=physicsfights, verbose=verbose)
			prescoeff = self.presentation_coefficients(verbose=False)
			for grade in average_grades:
				if grade["role"] == "reporter":
					roundprescoeff = prescoeff[grade["pf"].round_number - 1]
					points += grade["value"]*roundprescoeff
					if verbose:
						msg+='\n\t%.2f*%.1f = %.2f points as a reporter,' % (grade["value"], roundprescoeff, grade["value"]*roundprescoeff)
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
		allpoints += sum(self.bonuspoints(roundnumber=roundnumber, physicsfights=physicsfights, verbose=verbose))


		if verbose:
			print "Team %s has %.2f points so far !"  % (self.name, allpoints)
		return allpoints

	def ranking(self, roundnumber=None, physicsfights=None, verbose=True):
		"""
		:param verbose:  Verbosity flag
		:return: (teams, position of self). Return all the teams, ranked by points and return my position amongst the rank.
		"""

		teams = Team.objects.all()

		teams = sorted(teams, key=lambda x : x.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=verbose))[::-1]
		if verbose:
			print "="*20, "Team Ranking", "="*20
			for ind, team in enumerate(teams):
				if team==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(roundnumber=roundnumber, physicsfights=physicsfights, verbose=False))+" points"
					print msg

		return teams, teams.index(self)+1

	def problems(self, verbose=True, currentpf=None):
		"""
		Get all the problems that I cannot present(already presented or eternal rejection) and cannot oppose(already opposed)

		:param verbose: verbosity Flag
		:param currentpf: A PhysicsFight instance. Return all the unpresentable problems before the current physics fight. If none, return on all the physics fights. This sentence is terribly unclear. Rephrase.

		:return: tuple of three lists. each list contains the problems that are eternally rejected, already presented and already opposed
		"""

		if verbose:
			print "="*20, "Problems of Team %s" % self.name, "="*20
		noproblems=[]

		if currentpf !=None:
			round_number = currentpf.round_number
		else: #TODO: remove these stupid 999 values and implement the pf rejection properly
			round_number = 999

		# the eternal rejection
		eternal_rejections = EternalRejection.objects.filter(physics_fight__reporter__team=self)
		assert len(eternal_rejections) < 2
		reject = []
		if len(eternal_rejections) > 0 and eternal_rejections[0].physics_fight.round_number < round_number:
			if verbose:
				print "Team %s rejected eternally problem %s" %(self.name, eternal_rejections[0].problem.name)
			reject.append(eternal_rejections[0].problem)
		noproblems.append(reject)

		# now all the problems already presented
		physics_fights = PhysicsFight.objects.filter(reporter__team=self)
		physics_fights = [pf for pf in physics_fights if pf.round_number < round_number]
		presented = []
		for physics_fight in physics_fights:
			if verbose:
				print "In %s, I presented problem %s" % (physics_fight, physics_fight.problem_presented)
			presented.append(physics_fight.problem_presented)
		noproblems.append(presented)

		# and problems already opposed
		physics_fights = PhysicsFight.objects.filter(opponent__team=self)
		physics_fights = [pf for pf in physics_fights if pf.round_number < round_number]
		opposed = []
		for physics_fight in physics_fights:
			if verbose:
				print "In %s, I opposed problem %s" % (physics_fight, physics_fight.problem_presented)
			opposed.append(physics_fight.problem_presented)
		noproblems.append(opposed)

		assert len(noproblems) == 3
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

class PhysicsFight(models.Model):

	round_number = models.IntegerField(
			choices=(((ind+1, 'Round '+str(ind+1)) for ind in range(4))),
			default=None
			)
	fight_number = models.IntegerField(
			choices=(((ind+1, 'Fight '+str(ind+1)) for ind in range(4))),
			default=None
			)
	room = models.ForeignKey(Room)
	reporter = models.ForeignKey(Participant, related_name='reporter_team_1')
	reporter_2 = models.ForeignKey(Participant, blank=True, null=True, related_name='reporter_team_2')
	opponent = models.ForeignKey(Participant, related_name='opponent_team')
	reviewer = models.ForeignKey(Participant, related_name='reviewer_team')
	problem_presented = models.ForeignKey(Problem)
	submitted_date = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return "Round %i | Fight %i | Room %s" % (self.round_number, self.fight_number, self.room.name)

	def ident(self):
		return "%s%s%s" %(self.round_number, self.fight_number, self.room.ident())

	def unavailable_problems(self, verbose=True):
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
		reporter_problems = self.reporter.team.problems(verbose=False, currentpf=self)
		opponent_problems = self.opponent.team.problems(verbose=False, currentpf=self)
		eternal_rejection = reporter_problems[0]

		if verbose:
			print "="*10, "Problem rejection for %s" % self, "="*10
			if len(eternal_rejection) != 0:
				print "Team %s eternally rejected problem \n\t%s" % (self.reporter.team, eternal_rejection[0])
		presented_by_reporter = reporter_problems[1]
		if verbose:
			msg = "Team %s already presented the following problems:" % self.reporter.team
			for problem in presented_by_reporter:
				msg += "\n\t%s" % problem
			print msg
		opposed_by_opponent = opponent_problems[2]
		if verbose:
			msg = "Team %s already opposed the following problems:" % self.opponent.team
			for problem in opposed_by_opponent:
				msg += "\n\t%s" % problem
			print msg
		presented_by_opponent = opponent_problems[1]
		if verbose:
			msg = "Team %s already presented the following problems:" % self.opponent.team
			for problem in presented_by_opponent:
				msg += "\n\t%s" % problem
			print msg

		# Finally, problems already presented in this Round, in the current room
		thisroundpfs = PhysicsFight.objects.filter(round_number=self.round_number).filter(room=self.room)
		presented_this_round = [pf.problem_presented for pf in thisroundpfs if pf.fight_number < self.fight_number]
		if verbose:
			msg = "In this round, problems already presented are:"
			for problem in presented_this_round:
				msg += "\n\t%s" % problem
			print msg

		return (presented_this_round, eternal_rejection, presented_by_reporter, opposed_by_opponent, presented_by_opponent)


class JuryGrade(models.Model):

	physics_fight = models.ForeignKey(PhysicsFight)

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
		return "Grade of %s" % self.jury

	def info(self):
		print "=" * 36
		print "Grade of %s" % self.jury
		print self.physics_fight
		print "Reporter %s from %s : %i" % (self.physics_fight.name_reporter, self.physics_fight.reporter, self.grade_reporter)
		print "Opponent %s from %s : %i" % (self.physics_fight.name_opponent, self.physics_fight.opponent, self.grade_opponent)
		print "Reviewer %s from %s : %i" % (self.physics_fight.name_reviewer, self.physics_fight.reviewer, self.grade_reviewer)


class TacticalRejection(models.Model):

	physics_fight = models.ForeignKey(PhysicsFight)

	problem = models.ForeignKey(Problem)

	def __unicode__(self):
		return "Problem rejected : %s" % self.problem

class EternalRejection(models.Model):

	physics_fight = models.ForeignKey(PhysicsFight)

	problem = models.ForeignKey(Problem)

	def __unicode__(self):
		return "Problem rejected : %s" % self.problem


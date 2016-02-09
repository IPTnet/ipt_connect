from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import sys


def mean(vec):
	return float(sum(vec)) / len(vec)


class Participant(models.Model):

	GENDER_CHOICES = ( ('M','Male'), ('F','Female'))

	ROLE_CHOICES = ( ('TM','Team Member'), ('TC','Team Captain'), ('IOC','IOC'), ('ACC','Accompanying') )

	DIET_CHOICES = ( ('NO','No specific diet'), ('NOPORK','No pork'), ('NOMEAT','No meat'), ('NOFISH','No fish'), ('NOMEAT_NOEGG','No meat, No eggs') )

	TOURISM_CHOICES = ( ('TOURISM_0','No') , ('TOURISM_1','Yes, one night'), ('TOURISM_2','Yes, two nights') )

	SHIRT_SIZES = (
		('S', 'Small'),
		('M', 'Medium'),
		('L', 'Large'),
	)

	name = models.CharField(max_length=50,default='Richard')
	surname = models.CharField(max_length=50,default='Feynman')
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
	email = models.EmailField(help_text='This address will be used to send you every important infos about the tournament.')
	birthdate = models.DateField(default='1900-01-31')
	photo = models.ImageField(upload_to='id_photo',help_text='Used for badges and transportation cards.', blank=True, null=True)
	team = models.ForeignKey('Team')
	role = models.CharField(max_length=20,choices=ROLE_CHOICES)
	passport_number = models.CharField(max_length=20)
	affiliation = models.CharField(max_length=20,default='XXX University')
	veteran = models.BooleanField(default=False,help_text='Have you already participated in the IPT?')
	diet = models.CharField(max_length=20,choices=DIET_CHOICES,help_text='Do you have a specific diet?')
	tourism=models.CharField(max_length=20,choices=TOURISM_CHOICES,help_text='Would you like to stay some more days in Paris after the tournament? Please note the LOC would only book the rooms, not pay for it!')
	shirt_size = models.CharField(max_length=1,choices=SHIRT_SIZES)
	remark = models.TextField(blank=True)
	hotel_room = models.CharField(max_length=20,blank=True)
	check_in = models.BooleanField(default=False,help_text='Has the participant arrived?')

	# def colored_name(self):
	#     if self.name == 'Vivien':
	#         color = "green"
	#     else:
	#         color = "red"
	#     return "<span style=color:%s>%s</span>" % (color,self.name)
	# colored_name.allow_tags = True

	def fullname(self):
		return self.name+' '+self.surname

	def __str__(self):
		return self.fullname()

	def compute_average_grades(self, roundnumber=None, verbose=True):
		"""
		I collect all the grades from the Jury members that are addressed to me and compute the average grade for each fight

		:param verbose: verbosity of the function
		:param roundnumber: round to consider. If None, I consider all the rounds.
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

		return average_grades

	def points(self, roundnumber=None, verbose=True):
		"""

		:param verbose: verbosity of the function
		:param roundnumber: round to consider. If None, I consider all the rounds
		:return: Return the number of points gathered by a single participant. The multiplicative coefficient associated to his/her role is not taken into account here.
		"""
		points = 0.0
		average_grades = self.compute_average_grades(verbose=verbose, roundnumber=roundnumber)
		for grade in average_grades:
			points += grade["value"]
			if verbose:
				print "\tIn %s, I gathered %.2f points as a %s" % (grade["pf"], grade["value"], grade["role"])
		if verbose:
			print "In total, I gathered %.2f points" % points
		return points


	def ranking(self, pool='all', roundnumber=None, verbose=True):
		"""

		:param pool: can be "team", "gender" or "all". Select the participant you want to be ranked with
		:param roundnumber: rounds to consider. If None, I consider all the PFs played so far.
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

		participants = sorted(participants, key=lambda x : x.points(roundnumber=roundnumber, verbose=verbose))[::-1]

		if verbose:
			print "="*20, "Ranking", "="*20
			for ind, participant in enumerate(participants):

				if participant==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+str(participant.fullname())+" - "+str(participant.points(verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+str(participant.fullname())+" - "+str(participant.points(verbose=False))+" points"
					print msg

		return participants, participants.index(self)+1



class Problem(models.Model):
	name = models.CharField(max_length=50, default=None)
	description = models.CharField(max_length=500, default=None)
	def __str__(self):

		return self.name
		
class Team(models.Model):
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50, null=True, blank=True, default=None)
	IOC = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
	def __str__(self):

		return self.name


	def bonuspoints(self, verbose=True, maxpf=2):
		"""
		Check if the rounds where I played are complete, and return the according number of bonus points (2 if first, 1 if second, or 1.5 each in case of ex-aequo)

		:param verbose: verbosity of the function
		:param maxpf: maximum number of physics fight per round
		:return: Return the number of bonus points
		"""


		# get all the Physics Fights where my participants are involved in
		pfs = PhysicsFight.objects.filter(reporter__team=self) | PhysicsFight.objects.filter(opponent__team=self) | PhysicsFight.objects.filter(reviewer__team=self)
		#myrooms = [room for room in pfs.room]
		roundnumbers = [1, 2, 3, 4]

		bonuspoints = []
		for roundnumber in roundnumbers:
			roundpfs = pfs.filter(round_number=roundnumber) # for a given round, I am always in the same room
			if len(roundpfs) == maxpf: # then all the fights are played
				teams = [roundpfs[0].reporter.team, roundpfs[0].opponent.team, roundpfs[0].reviewer.team]
				if verbose:
					print "Round %i opposes teams from %s, %s and %s" % (int(roundnumber), teams[0].name, teams[1].name, teams[2].name)
				results = []
				for team in teams:
					teamroundpoints = 0
					for participant in Participant.objects.filter(team=team):
						average_grades = participant.compute_average_grades(roundnumber=roundnumber, verbose=False)
						for grade in average_grades:
							if grade["role"] == "reporter":
								teamroundpoints += grade["value"] * 3.0
							elif grade["role"] == "opponent":
								teamroundpoints += grade["value"] * 2.0
							elif grade["role"] == "reviewer":
								teamroundpoints += grade["value"]
							else:
								print "Role undefined : %s" % grade["role"]
								sys.exit()
					if verbose:
						print "Team %s gathered %.2f points in Round %i" % (team.name, teamroundpoints, int(roundnumber))
					results.append({"name": team.name, "points": teamroundpoints})

				results = sorted(results, key=lambda x: x["points"])[::-1]

				# Now finally give the bonus point
				if verbose:
					print "Round %i ranking:" % roundnumber
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
					print "On top of that, team %s win %.1f additional bonus points" % (self.name, bonuspoint)
				bonuspoints.append(bonuspoint)

			else:  # Not all the fights are played, I skip
				if verbose:
					print "Not all physics fights in Round %i have been played yet!" % int(roundnumber)
				bonuspoints.append(0.0)

		return bonuspoints


	def points(self, roundnumber=None, verbose=True):
		"""
		I get all the participants that are in my team and sum their average grades, multiplied by their roles.

		:return: Return the total number of points
		"""

		participants = Participant.objects.filter(team=self)

		if verbose:
			print "="*20, "Compute Team Points", "="*20
			print "There are %i participants in %s" % (len(participants), self.name)

		allpoints = 0
		for participant in participants:
			points = 0
			if verbose:
				if roundnumber==None:
					msg = 'In overall, I scored '
				else:
					msg = 'In Round %i, I scored' % int(roundnumber)
			average_grades = participant.compute_average_grades(roundnumber=roundnumber, verbose=verbose)
			for grade in average_grades:
				if grade["role"] == "reporter":
					points += grade["value"]*3.0
					if verbose:
						msg+='%.2f*3 = %.2f points as a reporter, ' % (grade["value"], grade["value"]*3)
				elif grade["role"] == "opponent":
					points += grade["value"]*2.0
					if verbose:
						msg+='%.2f*2 = %.2f points as an opponent, ' % (grade["value"], grade["value"]*2)
				elif grade["role"] == "reviewer":
					points += grade["value"]
					if verbose:
						msg+='%.2f points as a reviewer, ' % (grade["value"])

				else:
					print "Something wrong here...my role is not defined !"
					sys.exit()

			if verbose:
				msg+='for a total of %.2f points' % points
				print msg
			allpoints += points

		# add bonus points for winning rounds, etc...
		allpoints += sum(self.bonuspoints(verbose=verbose))


		if verbose:
			print "Team %s has %.2f points so far !"  % (self.name, allpoints)
		return allpoints

	def ranking(self, verbose=True):

		teams = Team.objects.all()

		teams = sorted(teams, key=lambda x : x.points(verbose=True))[::-1]
		if verbose:
			print "="*20, "Team Ranking", "="*20
			for ind, team in enumerate(teams):
				if team==self and sys.stdout.isatty():
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(verbose=False))+" points"
					print '\x1b[32m%s\x1b[0m' % msg
				else:
					msg = str(ind+1)+") "+str(team.name)+" - "+str(team.points(verbose=False))+" points"
					print msg

		return teams, teams.index(self)+1



class Room(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):

		return self.name

class Jury(models.Model):
	name = models.CharField(max_length=50)
	team = models.ForeignKey('Team', null=True, blank=True)
	def __str__(self):

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

	def __str__(self):
		return "Round %i | Fight %i | Room %s" % (self.round_number, self.fight_number, self.room.name)


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

	def __str__(self):
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

	def __str__(self):
		return "Problem rejected : %s" % self.problem

class EternalRejection(models.Model):

	physics_fight = models.ForeignKey(PhysicsFight)

	problem = models.ForeignKey(Problem)

	def __str__(self):
		return "Problem rejected : %s" % self.problem


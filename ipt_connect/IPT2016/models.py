from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from config import *


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


	def __str__(self):

		"""

		Cette methode que nous definirons dans tous les modeles

		nous permettra de reconnaitre facilement les differents objets que

		nous traiterons plus tard et dans l'administration

		"""

		return self.surname

	def compute_average_grades(self, verbose=True):
		"""
		I collect all the grades from the Jury members and compute the average grade for the current Participant.
		WARNING : Note that there is certainly a way to do it in a more djangoist way (using the relation between JuryGrade associated Participants and the current Participant) but I don't know it, and I don't have muche time yet...to be inverstigated later.
		"""


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

	def compute_teampoints(self, participants):
		"""
		:param participants: list of Participant instance

		I browse through the list of participants and add the mean grades to all of them who belongs to me
		"""



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
			choices=(((ind+1, 'Round '+str(ind+1)) for ind in range(maxrounds))),
			default=None
			)

	fight_number = models.IntegerField(
			choices=(((ind+1, 'Fight '+str(ind+1)) for ind in range(maxfights))),
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
			choices=(((ind, ind) for ind in range(maxgrade+1))),
			default=None
			)

	grade_opponent = models.IntegerField(
			choices=(((ind, ind) for ind in range(maxgrade+1))),
			default=None
			)

	grade_reviewer = models.IntegerField(
			choices=(((ind, ind) for ind in range(maxgrade+1))),
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


import django
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = "ipt_connect.settings"
django.setup()
execfile("config.py")  # Have to get rid of this at some point!!


populate_db = False

from IPT2016.models import *


if not populate_db:

	"""
	# create the Participant instances
	participants = []
	for country in [France, Denmark, Ukraine]:
		for participant in country["participants"]:
			participants.append(Participant(name=participant, country=country["name"], grades=[], average_grades=[]))
	"""

	# get all the participants
	participants = []
	allparticipants = Participant.objects.all()
	for participant in allparticipants:
		participants.append()

	# get the grades from the Jury

	jurygrades = JuryGrade.objects.all()


	# assign all the grades to the participants
	for jurygrade in jurygrades:

		for participant in participants:

			if participant.name == jurygrade.physics_fight.name_reporter:
				value = jurygrade.grade_reporter
				pf = jurygrade.physics_fight
				participant.grades.append({"value" : value, "role" : "reporter", "pf" : pf, "jury" : jurygrade.name})

			elif participant.name == jurygrade.physics_fight.name_opponent:
				value = jurygrade.grade_opponent
				pf = jurygrade.physics_fight
				participant.grades.append({"value" : value, "role" : "opponent", "pf" : pf, "jury" : jurygrade.name})

			elif participant.name == jurygrade.physics_fight.name_reviewer:
				value = jurygrade.grade_reviewer
				pf = jurygrade.physics_fight
				participant.grades.append({"value" : value, "role" : "reviewer", "pf" : pf, "jury" : jurygrade.name})



	# compute the average grades for the participants
	for participant in participants:
		print participant


	# compute the points per country
	for country in ["France", "Denmark", "Ukraine"]:
		compute_teampoints(participants, country=country)




if populate_db: #populating the database

	#Teams
	Team.objects.create(name="France", surname="Baguette")
	Team.objects.create(name="Germany", surname="Kartoffelns")
	Team.objects.create(name="Russia", surname="Voudkash")

	France = Team.objects.filter(name="France")[0]
	Germany = Team.objects.filter(name="Germany")[0]
	Russia = Team.objects.filter(name="Russia")[0]


	#Problems
	Problem.objects.create(name='1 - La chaussette', description="pourquoi les chaussettes se perdent dans les machines a laver ?")
	Problem.objects.create(name='2 - Le fromage', description="Pourquoi le fromage pue ?")
	Problem.objects.create(name='3 - Le temps', description="Pourquoi le temps passe vite ?")

	Problem1 = Problem.objects.filter(name='1 - La chaussette')[0]
	Problem2 = Problem.objects.filter(name='2 - Le fromage')[0]
	Problem3 = Problem.objects.filter(name='3 - Le temps')[0]

	#Rooms
	Room.objects.create(name='1 - Toilets')
	Room.objects.create(name='2 - Boudoir')

	Room1 = Room.objects.filter(name='1 - Toilets')[0]
	Room2 = Room.objects.filter(name='2 - Boudoir')[0]

	#Jurys
	Jury.objects.create(name='Henri Poincare', team=France)
	Jury.objects.create(name='Marie Curie', team=France)
	Jury.objects.create(name='Albert Einstein', team=Germany)
	Jury.objects.create(name='Hanz Heisenberg', team=Germany)
	Jury.objects.create(name='Lev Landau', team=Russia)
	Jury.objects.create(name='Lev Lifschitz', team=Russia)
	Jury.objects.create(name='Pedro DelPoncho')

	JuryF1 = Jury.objects.filter(name='Henri Poincare')[0]
	JuryF2 = Jury.objects.filter(name='Marie Curie')[0]
	JuryG1 = Jury.objects.filter(name='Albert Einstein')[0]
	JuryG2 = Jury.objects.filter(name='Hanz Heisenberg')[0]
	JuryR1 = Jury.objects.filter(name='Lev Landau')[0]
	JuryR2 = Jury.objects.filter(name='Lev Lifschitz')[0]
	JuryNC = Jury.objects.filter(name='Pedro DelPoncho')[0]

	#Participants

	Participant.objects.create(name='Henri', surname='Riant', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=France, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Jean', surname='Valjean', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=France, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Hank', surname='Friesch', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Germany, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Helmut', surname='Heinz', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Germany, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Ivan', surname='Valogray', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Russia, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Andrii', surname='Kushkin', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Russia, role='TM', passport_number='ASDFG123', affiliation='Montcul University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Part1F = Participant.objects.filter(name='Henri')[0]
	Part2F = Participant.objects.filter(name='Jean')[0]

	Part1G = Participant.objects.filter(name='Hank')[0]
	Part2G = Participant.objects.filter(name='Helmut')[0]

	Part1R = Participant.objects.filter(name='Ivan')[0]
	Part2R = Participant.objects.filter(name='Andrii')[0]


	# Physics Fights
	PhysicsFight.objects.create(round_number=1, fight_number=1, room=Room1, reporter=Part1F, opponent=Part2G, reviewer=Part1R, problem_presented=Problem1)

	PhysicsFight.objects.create(round_number=1, fight_number=2, room=Room1, reporter=Part2R, opponent=Part2F, reviewer=Part1F, problem_presented=Problem2)

	PF1 = PhysicsFight.objects.filter(fight_number=1)[0]  # Ill-design selection !!
	PF2 = PhysicsFight.objects.filter(fight_number=2)[0]  # Same


	# Jury Grade

	JuryGrade.objects.create(physics_fight=PF1, jury=JuryF1, grade_reporter=8, grade_opponent=5, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryF2, grade_reporter=7, grade_opponent=6, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryG1, grade_reporter=8, grade_opponent=5, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryG2, grade_reporter=9, grade_opponent=5, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryR1, grade_reporter=6, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryR2, grade_reporter=8, grade_opponent=5, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryNC, grade_reporter=7, grade_opponent=4, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF2, jury=JuryF1, grade_reporter=4, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryF2, grade_reporter=5, grade_opponent=6, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryG1, grade_reporter=4, grade_opponent=7, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryG2, grade_reporter=3, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryR1, grade_reporter=5, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryR2, grade_reporter=4, grade_opponent=8, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryNC, grade_reporter=4, grade_opponent=7, grade_reviewer=9)


	# Rejections

	TacticalRejection.objects.create(physics_fight=PF1, problem=Problem3)
	EternalRejection.objects.create(physics_fight=PF2, problem=Problem3)

	sys.exit()

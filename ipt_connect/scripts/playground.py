# coding=utf-8
import django
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = "ipt_connect.settings"
django.setup()


populate_db = False  # If you start from a fresh or flushed db and want to repopulate it quickly with test data.

from IPT2016.models import *

if not populate_db:


	teams = Team.objects.all()
	participants = Participant.objects.all()
	rooms = Room.objects.all()
	pfs = PhysicsFight.objects.all()



	for participant in participants:
		#participant.ranking(roundnumber=None, pool='all', verbose=True)
		#participant.compute_average_grades()
		#participant.points(roundnumber=2)
		#sys.exit()
		pass

	for pf in pfs[::-1]:
		#problems = pf.unavailable_problems()
		#sys.exit()
		pass


	for team in teams:
		if team.name == "Greece":
			team.points()
			#ranking = team.ranking(verbose=True)
			#print ranking
			#noproblems = team.problems()
			#coeffs = team.presentation_coefficients()
			#points = team.bonuspoints(verbose=True)
			#print points
	sys.exit()


	sys.exit()



if populate_db: #populating the database

	#Teams
	Team.objects.create(name="France", surname="Baguette")
	Team.objects.create(name="Germany", surname="Kartoffelns")
	Team.objects.create(name="Russia", surname="Voudkash")
	Team.objects.create(name="China", surname="HRW")
	Team.objects.create(name="Spain", surname="Vamosalaplaya")
	Team.objects.create(name="Greece", surname="OuzosXX")


	France = Team.objects.filter(name="France")[0]
	Germany = Team.objects.filter(name="Germany")[0]
	Russia = Team.objects.filter(name="Russia")[0]
	China = Team.objects.filter(name="China")[0]
	Spain = Team.objects.filter(name="Spain")[0]
	Greece = Team.objects.filter(name="Greece")[0]


	#Problems
	Problem.objects.create(name='1 - La chaussette', description="Pourquoi les chaussettes se perdent dans les machines a laver ?")
	Problem.objects.create(name='2 - Le fromage', description="Pourquoi le fromage pue ?")
	Problem.objects.create(name='3 - Le temps', description="Pourquoi le temps passe vite ?")
	Problem.objects.create(name='4 - Le ressort', description="Pourquoi le ressort ne reste pas a l'interieur?")
	Problem.objects.create(name='5 - La banane', description="Pourquoi les bananes ne sont pas bleues ?")
	Problem.objects.create(name='6 - Le tambour', description="Pourquoi le temps est a la bourre ?")
	Problem.objects.create(name='7 - La fontaine', description="Pourquoi l'eau des fontaines mouille ?")
	Problem.objects.create(name='8 - Le slip', description="Peut-on transformer un slip en catapulte?")
	Problem.objects.create(name='9 - Le train', description="Pourquoi les trains font choo choo?")



	Problem1 = Problem.objects.filter(name='1 - La chaussette')[0]
	Problem2 = Problem.objects.filter(name='2 - Le fromage')[0]
	Problem3 = Problem.objects.filter(name='3 - Le temps')[0]
	Problem4 = Problem.objects.filter(name='4 - Le ressort')[0]
	Problem5 = Problem.objects.filter(name='5 - La banane')[0]
	Problem6 = Problem.objects.filter(name='6 - Le tambour')[0]
	Problem7 = Problem.objects.filter(name='7 - La fontaine')[0]
	Problem8 = Problem.objects.filter(name='8 - Le slip')[0]
	Problem9 = Problem.objects.filter(name='9 - Le train')[0]

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
	Jury.objects.create(name='Aston Martin')
	Jury.objects.create(name='Georges Lemaitre', team=China)
	Jury.objects.create(name='Xi Winping', team=China)
	Jury.objects.create(name='Salomon Planck', team=Spain)
	Jury.objects.create(name='Tortillas DelBosque', team=Spain)
	Jury.objects.create(name='Aristote Lajolie', team=Greece)
	Jury.objects.create(name='Leonidas Tropetitas', team=Greece)

	JuryF1 = Jury.objects.filter(name='Henri Poincare')[0]
	JuryF2 = Jury.objects.filter(name='Marie Curie')[0]
	JuryG1 = Jury.objects.filter(name='Albert Einstein')[0]
	JuryG2 = Jury.objects.filter(name='Hanz Heisenberg')[0]
	JuryR1 = Jury.objects.filter(name='Lev Landau')[0]
	JuryR2 = Jury.objects.filter(name='Lev Lifschitz')[0]
	JuryNC1 = Jury.objects.filter(name='Pedro DelPoncho')[0]
	JuryNC2 = Jury.objects.filter(name='Aston Martin')[0]
	JuryC1 = Jury.objects.filter(name='Georges Lemaitre')[0]
	JuryC2 = Jury.objects.filter(name='Xi Winping')[0]
	JuryS1 = Jury.objects.filter(name='Salomon Planck')[0]
	JuryS2 = Jury.objects.filter(name='Tortillas DelBosque')[0]
	JuryE1 = Jury.objects.filter(name='Aristote Lajolie')[0]
	JuryE2 = Jury.objects.filter(name='Leonidas Tropetitas')[0]



	#Participants

	Participant.objects.create(name='Henri', surname='Riant', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=France, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Jean', surname=u'Valjeané', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=France, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Paul', surname='DePaul', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=France, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Hank', surname='Friesch', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Germany, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Angela', surname='Heinz', gender='F', email='toto@toto.com', birthdate='1900-01-31', team=Germany, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Max', surname='Kolz', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Germany, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Ivan', surname='Valogray', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Russia, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Andrii', surname='Kushkin', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Russia, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Katerina', surname='Ivanov', gender='F', email='toto@toto.com', birthdate='1900-01-31', team=Russia, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)



	Participant.objects.create(name='Yao', surname='Zhe', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=China, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Bao', surname='Bounni', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=China, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Yu', surname='Weiwei', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=China, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Marcellos', surname='Ramon', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Spain, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Caterina', surname='Oleole', gender='F', email='toto@toto.com', birthdate='1900-01-31', team=Spain, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Jose', surname='Dias', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Spain, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Tassos', surname='Spagettos', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Greece, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Leos', surname='Homere', gender='M', email='toto@toto.com', birthdate='1900-01-31', team=Greece, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)

	Participant.objects.create(name='Laylas', surname='Minas', gender='F', email='toto@toto.com', birthdate='1900-01-31', team=Greece, role='TM', passport_number='ASDFG123', affiliation='Trololo University', veteran=False, diet='NO', tourism='TOURISM_0', shirt_size='M', check_in=False)


	Part1F = Participant.objects.filter(name='Henri')[0]
	Part2F = Participant.objects.filter(name='Jean')[0]
	Part3F = Participant.objects.filter(name='Paul')[0]

	Part1G = Participant.objects.filter(name='Hank')[0]
	Part2G = Participant.objects.filter(name='Max')[0]
	Part3G = Participant.objects.filter(name='Angela')[0]

	Part1R = Participant.objects.filter(name='Ivan')[0]
	Part2R = Participant.objects.filter(name='Andrii')[0]
	Part3R = Participant.objects.filter(name='Katerina')[0]

	Part1C = Participant.objects.filter(name='Yao')[0]
	Part2C = Participant.objects.filter(name='Bao')[0]
	Part3C = Participant.objects.filter(name='Yu')[0]

	Part1S = Participant.objects.filter(name='Marcellos')[0]
	Part2S = Participant.objects.filter(name='Caterina')[0]
	Part3S = Participant.objects.filter(name='Jose')[0]

	Part1E = Participant.objects.filter(name='Tassos')[0]
	Part2E = Participant.objects.filter(name='Leos')[0]
	Part3E= Participant.objects.filter(name='Laylas')[0]



	# Physics Fights
	PhysicsFight.objects.create(round_number=1, fight_number=1, room=Room1, reporter=Part1F, opponent=Part2G, reviewer=Part1R, problem_presented=Problem1)
	PhysicsFight.objects.create(round_number=1, fight_number=2, room=Room1, reporter=Part2R, opponent=Part2F, reviewer=Part1G, problem_presented=Problem2)
	PhysicsFight.objects.create(round_number=1, fight_number=3, room=Room1, reporter=Part3G, opponent=Part3R, reviewer=Part1F, problem_presented=Problem3)

	PhysicsFight.objects.create(round_number=1, fight_number=1, room=Room2, reporter=Part1C, opponent=Part2E, reviewer=Part1S, problem_presented=Problem4)
	PhysicsFight.objects.create(round_number=1, fight_number=2, room=Room2, reporter=Part2S, opponent=Part2C, reviewer=Part1E, problem_presented=Problem5)
	PhysicsFight.objects.create(round_number=1, fight_number=3, room=Room2, reporter=Part3E, opponent=Part3S, reviewer=Part1C, problem_presented=Problem6)

	PhysicsFight.objects.create(round_number=2, fight_number=1, room=Room1, reporter=Part1C, opponent=Part3R, reviewer=Part1F, problem_presented=Problem7)
	PhysicsFight.objects.create(round_number=2, fight_number=2, room=Room1, reporter=Part2R, opponent=Part2F, reviewer=Part2C, problem_presented=Problem8)
	PhysicsFight.objects.create(round_number=2, fight_number=3, room=Room1, reporter=Part3F, opponent=Part3C, reviewer=Part1R, problem_presented=Problem9)

	PhysicsFight.objects.create(round_number=2, fight_number=1, room=Room2, reporter=Part3E, opponent=Part2S, reviewer=Part3G, problem_presented=Problem7)
	PhysicsFight.objects.create(round_number=2, fight_number=2, room=Room2, reporter=Part2G, opponent=Part2E, reviewer=Part1S, problem_presented=Problem8)
	PhysicsFight.objects.create(round_number=2, fight_number=3, room=Room2, reporter=Part2S, opponent=Part1G, reviewer=Part1E, problem_presented=Problem9)


	PF1 = PhysicsFight.objects.filter(fight_number=1).filter(round_number=1).filter(room=Room1)[0]
	PF2 = PhysicsFight.objects.filter(fight_number=2).filter(round_number=1).filter(room=Room1)[0]
	PF3 = PhysicsFight.objects.filter(fight_number=3).filter(round_number=1).filter(room=Room1)[0]

	PF4 = PhysicsFight.objects.filter(fight_number=1).filter(round_number=1).filter(room=Room2)[0]
	PF5 = PhysicsFight.objects.filter(fight_number=2).filter(round_number=1).filter(room=Room2)[0]
	PF6 = PhysicsFight.objects.filter(fight_number=3).filter(round_number=1).filter(room=Room2)[0]

	PF7 = PhysicsFight.objects.filter(fight_number=1).filter(round_number=2).filter(room=Room1)[0]
	PF8 = PhysicsFight.objects.filter(fight_number=2).filter(round_number=2).filter(room=Room1)[0]
	PF9 = PhysicsFight.objects.filter(fight_number=3).filter(round_number=2).filter(room=Room1)[0]

	PF10 = PhysicsFight.objects.filter(fight_number=1).filter(round_number=2).filter(room=Room2)[0]
	PF11 = PhysicsFight.objects.filter(fight_number=2).filter(round_number=2).filter(room=Room2)[0]
	PF12 = PhysicsFight.objects.filter(fight_number=3).filter(round_number=2).filter(room=Room2)[0]

	# Jury Grade

	JuryGrade.objects.create(physics_fight=PF1, jury=JuryS1, grade_reporter=8, grade_opponent=5, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryS2, grade_reporter=7, grade_opponent=6, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryC1, grade_reporter=8, grade_opponent=5, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryC2, grade_reporter=9, grade_opponent=5, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryE1, grade_reporter=6, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryE2, grade_reporter=8, grade_opponent=5, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF1, jury=JuryNC1, grade_reporter=7, grade_opponent=4, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF2, jury=JuryS1, grade_reporter=4, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryS2, grade_reporter=5, grade_opponent=6, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryC1, grade_reporter=4, grade_opponent=7, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryC2, grade_reporter=3, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryE1, grade_reporter=5, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryE2, grade_reporter=4, grade_opponent=8, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF2, jury=JuryNC1, grade_reporter=4, grade_opponent=7, grade_reviewer=9)

	JuryGrade.objects.create(physics_fight=PF3, jury=JuryS1, grade_reporter=3, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryS2, grade_reporter=4, grade_opponent=8, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryC1, grade_reporter=4, grade_opponent=7, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryC2, grade_reporter=3, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryE1, grade_reporter=5, grade_opponent=7, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryE2, grade_reporter=4, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF3, jury=JuryNC1, grade_reporter=5, grade_opponent=7, grade_reviewer=9)

	JuryGrade.objects.create(physics_fight=PF4, jury=JuryF1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryF2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryG1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryG2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryR1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryR2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF4, jury=JuryNC2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF5, jury=JuryF1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryF2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryG1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryG2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryR1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryR2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF5, jury=JuryNC2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF6, jury=JuryF1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryF2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryG1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryG2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryR1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryR2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF6, jury=JuryNC2, grade_reporter=8, grade_opponent=7, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF7, jury=JuryS1, grade_reporter=8, grade_opponent=7, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryS2, grade_reporter=8, grade_opponent=7, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryG1, grade_reporter=6, grade_opponent=5, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryG2, grade_reporter=7, grade_opponent=6, grade_reviewer=6)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryE1, grade_reporter=8, grade_opponent=8, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryE2, grade_reporter=7, grade_opponent=6, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF7, jury=JuryNC1, grade_reporter=8, grade_opponent=6, grade_reviewer=6)

	JuryGrade.objects.create(physics_fight=PF8, jury=JuryS1, grade_reporter=4, grade_opponent=9, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryS2, grade_reporter=4, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryG1, grade_reporter=3, grade_opponent=9, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryG2, grade_reporter=5, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryE1, grade_reporter=4, grade_opponent=9, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryE2, grade_reporter=6, grade_opponent=9, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF8, jury=JuryNC1, grade_reporter=3, grade_opponent=7, grade_reviewer=10)

	JuryGrade.objects.create(physics_fight=PF9, jury=JuryS1, grade_reporter=2, grade_opponent=4, grade_reviewer=5)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryS2, grade_reporter=1, grade_opponent=4, grade_reviewer=3)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryG1, grade_reporter=4, grade_opponent=5, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryG2, grade_reporter=3, grade_opponent=4, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryE1, grade_reporter=2, grade_opponent=6, grade_reviewer=3)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryE2, grade_reporter=3, grade_opponent=5, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF9, jury=JuryNC1, grade_reporter=5, grade_opponent=4, grade_reviewer=5)

	JuryGrade.objects.create(physics_fight=PF10, jury=JuryF1, grade_reporter=2, grade_opponent=5, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryF2, grade_reporter=1, grade_opponent=4, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryC1, grade_reporter=1, grade_opponent=6, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryC2, grade_reporter=1, grade_opponent=5, grade_reviewer=7)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryR1, grade_reporter=2, grade_opponent=4, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryR2, grade_reporter=3, grade_opponent=5, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF10, jury=JuryNC2, grade_reporter=2, grade_opponent=5, grade_reviewer=7)

	JuryGrade.objects.create(physics_fight=PF11, jury=JuryF1, grade_reporter=2, grade_opponent=8, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryF2, grade_reporter=3, grade_opponent=7, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryC1, grade_reporter=2, grade_opponent=9, grade_reviewer=9)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryC2, grade_reporter=4, grade_opponent=8, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryR1, grade_reporter=3, grade_opponent=7, grade_reviewer=10)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryR2, grade_reporter=2, grade_opponent=8, grade_reviewer=8)
	JuryGrade.objects.create(physics_fight=PF11, jury=JuryNC2, grade_reporter=3, grade_opponent=8, grade_reviewer=8)

	JuryGrade.objects.create(physics_fight=PF12, jury=JuryF1, grade_reporter=6, grade_opponent=7, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryF2, grade_reporter=5, grade_opponent=6, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryC1, grade_reporter=7, grade_opponent=8, grade_reviewer=3)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryC2, grade_reporter=6, grade_opponent=7, grade_reviewer=5)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryR1, grade_reporter=5, grade_opponent=6, grade_reviewer=4)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryR2, grade_reporter=7, grade_opponent=5, grade_reviewer=3)
	JuryGrade.objects.create(physics_fight=PF12, jury=JuryNC2, grade_reporter=5, grade_opponent=7, grade_reviewer=4)


	# Rejections

	TacticalRejection.objects.create(physics_fight=PF1, problem=Problem2)

	TacticalRejection.objects.create(physics_fight=PF6, problem=Problem7)
	TacticalRejection.objects.create(physics_fight=PF6, problem=Problem1)

	TacticalRejection.objects.create(physics_fight=PF8, problem=Problem3)
	TacticalRejection.objects.create(physics_fight=PF8, problem=Problem4)
	TacticalRejection.objects.create(physics_fight=PF8, problem=Problem5)
	TacticalRejection.objects.create(physics_fight=PF8, problem=Problem7)

	EternalRejection.objects.create(physics_fight=PF1, problem=Problem3)
	EternalRejection.objects.create(physics_fight=PF2, problem=Problem6)
	EternalRejection.objects.create(physics_fight=PF4, problem=Problem9)
	sys.exit()

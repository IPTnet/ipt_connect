### config file ###

def mean(l):
	return float(sum(l))/len(l)

# General

maxrounds = 4
maxfights = 3
maxrooms = 5
maxgrade = 10
minjurys = 4

problems = [

	"1 - Popsicle Stick Cobra",
	"2 - The Torque",
	"3 - Cooling Jug",
	"4 - Ferromagnetic Sea",
	"5 - Cracks On The Glass",
	"6 - The Silencer",
	"7 - Greenhouse Effect",
	"8 - Drop Jumping Jack",
	"9 - Sultry Day",
	"10 - Water Bomb",
	"11 - True Quantum Randomizer",
	"12 - Half Empty Bottle",
	"13 - Cross Talking Metronomes",
	"14 - Sticky Balloon",
	"15 - Electric Fountain",
	"16 - Magnetic Cannon",
	"17 - Looking For The Signs Of Civilization",
]


# Rounds Organisation

countries= ["Ukraine", "Denmark", "France"]
jury = ["Alfred Nobel", "Thomas Edison", "Nikola Tesla", "Marie Curie"]

countries.sort()
jury.sort()


# Participants list

Ukraine = {"participants": ["Dom Domkek", "Vlad Vladek", "Piotr Piotrek"], "name":"Ukraine"}

Denmark = {"participants": ["Olaf Olafsson", "Negus Negusson", "Jonas Jonasson"], "name":"Denmark"}

France = {"participants": ["Henri Riant", "Pierre Rocque","Jean Valjean"], "name": "France"}


allparticipants = []
allcountries = [Ukraine, Denmark, France]
for country in allcountries:
	for participant in country["participants"]:
		allparticipants.append(participant)

allparticipants.sort()


# Teams are a collection of participants. Each participant is a Participant class instance
# Participant has a name, a serie of grade+role, a country,


class Participant:

	def __init__(self, name=None, country=None, grades=None, average_grades=None):

		"""

		:param name: sting, name of the participant
		:param country: string, country of the participant
		:param grades: list of dicts. Each dict contains the corresponding jury, value, role and pf.
		:param average_grades: list of dicts. Each dict contains the average grade per pf.
		"""
		self.name = name
		self.country = country
		self.grades = grades
		self.average_grades = average_grades

	def compute_average_grades(self, verbose=True):

		pfs = list(set([self.grade["pf"] for self.grade in self.grades]))

		for pf in pfs:
			pfgrades = list(sort([self.grade["value"] for self.grade in self.grades if self.grade["pf"] == pf]))

			# WARNING ! CHECK THE RULES ABOUT IT !!!!
			# Rule for grade rejection: divide the number of jury by 4.
			# Round the result (if result is X.5, round down to X)
			# If the result is even, reject result/2 lowest and result/2 highest marks
			# If the result is odd, reject result/2 -0.5 lowest and result/2 + 0.5 highest marks.
			# Example : 7 jury members --> /4 = 1.75 --> round = 2 --> reject 1 highest and 1 lowest marks


			eps = 1e-8
			nreject = round( len(pfgrades) / 4.0  - eps)  # remove an epsilon to round down if round(X.5)

			if round(nreject/2.0) == nreject/2.0:
				nlow = int(nreject/2.0)
				nhigh = int(nlow)
			else:
				nlow = int(nreject/2.0 + 0.5)
				nhigh = int(nreject/2.0 - 0.5)

			if verbose:
				print "I reject %i lowest mark(s) and %i highest mark(s)"  % (nlow, nhigh)

			i = 0
			while i < nhigh:
				pfgrades.pop(-1)
				i += 1

			i = 0
			while i < nlow:
				pfgrades.pop(0)
				i += 1


			for name, role in zip([pf.name_reporter, pf.name_opponent, pf.name_reviewer], ["reporter", "opponent", "reviewer"]):
				if self.name == name:
					myrole = role

			try:
				assert myrole
			except:
				print "User not found in the physics fight ! Something fishy here..."

			average_grade = {"value": mean(pfgrades), "pf": pf, "role": myrole}

			self.average_grades.append(average_grade)


	def __str__(self):

		self.compute_average_grades(verbose=False)

		msg = "="*40
		msg += "\nName: %s  | Country: %s " % (self.name, self.country)
		if self.average_grades:
			msg += "\nGrades so far:"
			for self.grade in self.average_grades:
				msg += "\n\t %s | %.2f points as %s" %(self.grade["pf"], self.grade["value"], self.grade["role"])
		else:
			msg += "\nNo grade so far."

		return msg



def compute_teampoints(participants, country=None):

	"""
	To be inserted in the team class
	function to compute the number of points per team
	"""

	countrypoints = []
	for participant in [participant for participant in participants if participant.country == country]:

		for average_grade in participant.average_grades:
			for ind, role in enumerate(["reviewer", "opponent", "reporter"]):
				if average_grade["role"] == role:
					mult = ind+1

			countrypoints.append(average_grade["value"]*mult)


	print "*"*40
	print "%s have %.2f points" % (country, sum(countrypoints))



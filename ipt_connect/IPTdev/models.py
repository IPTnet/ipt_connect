# coding: utf8
import os
import time
from string import replace
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal
from django.dispatch import receiver
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.encoding import iri_to_uri
from solo.models import SingletonModel

import func_mean as means
import parameters as params
from func_bonus import distribute_bonus_points

# Useful static variables
selective_fights = [i + 1 for i in range(params.npf)]
selective_fights_and_semifinals = [
    i + 1 for i in range(params.npf + params.semifinals_quantity)
]
semifinals = [i + 1 for i in range(params.npf, params.npf + params.semifinals_quantity)]
npf_tot = params.npf + params.semifinals_quantity + int(params.with_final_pf)
final_fight_number = params.npf + params.semifinals_quantity + 1
grade_choices = [(ind, ind) for ind in range(10 + 1)]
mean = means.mean

special_mean = getattr(means, params.mean)


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('-')[-1]
        # get filename
        if instance.pk:
            filename = iri_to_uri(
                replace(
                    (u'{}_{}_{}.{}').format(
                        instance.team, instance.surname, instance.name, ext
                    ),
                    ' ',
                    '_',
                )
            )
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class Participant(models.Model):
    """
    This class represent the basic model of our program, a participant.
    It can be a student competing, a team-leader, a jury member, an IOC or an external jury or even a staff, basically anyone taking part in the tournament."""

    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('D', 'Decline to report'))

    ROLE_CHOICES = (
        ('TM', 'Team Member'),
        ('TC', 'Team Captain'),
        ('TL', 'Team Leader'),
        ('ACC', 'Accompanying'),
    )

    DIET_CHOICES = (
        ('NO', 'No specific diet'),
        ('NOPORK', 'No pork'),
        ('NOMEAT', 'No meat'),
        ('NOFISH', 'No fish'),
        ('NOMEAT_NOEGG', 'No meat, No eggs'),
        ('OTHER', 'Other (see remarks)'),
    )

    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    STATUS_CHOICES = (
        ('B', 'Bachelor student'),
        ('M', 'Master student'),
        ('S', 'Specialist student'),
        ('O', 'Other'),
    )

    # parameters
    name = models.CharField(max_length=50, default=None, verbose_name='Name')
    surname = models.CharField(max_length=50, default=None, verbose_name='Surname')
    gender = models.CharField(
        blank=True, max_length=1, choices=GENDER_CHOICES, verbose_name='Gender'
    )
    email = models.EmailField(
        blank=True,
        help_text='This address will be used to send the participant every important infos about the tournament.',
        verbose_name='Email',
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[phone_regex],
        blank=True,
        help_text="Compulsory for the Team Leaders.",
    )  # validators should be a list
    passport_number = models.CharField(blank=True, max_length=50)
    birthdate = models.DateField(default='1900-01-31', verbose_name='Birthdate')
    # photo = models.ImageField(upload_to=UploadToPathAndRename(params.instance_name+'/id_photo'),help_text="Please use a clear ID photo. This will be used for badges and transportation cards.", null=True)
    team = models.ForeignKey('Team', null=True, verbose_name='Team')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="The team must consist of a Team Captain (student), between two and five Team Members (students), and between one and two Team Leaders (Prof., PhD, Postdoc in physics). Don't forget to register yourself!",
        default="TM",
        verbose_name='Role',
    )
    affiliation = models.CharField(blank=True, max_length=50, default='XXX University')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, blank=True, verbose_name='Student status'
    )
    veteran = models.BooleanField(
        default=False,
        help_text="Has the participant already participated in the tournament? (informative only)",
        verbose_name='Veteran',
    )
    diet = models.CharField(
        blank=True,
        max_length=20,
        choices=DIET_CHOICES,
        help_text='Does the participant have a specific diet?',
    )
    mixed_gender_accommodation = models.BooleanField(
        default=True,
        help_text="Is it ok for the participant to be in a mixed gender hotel room?",
        verbose_name='Mixed gender accommodation?',
    )
    shirt_size = models.CharField(blank=True, max_length=2, choices=SHIRT_SIZES)
    remark = models.TextField(blank=True, verbose_name='Remarks')

    total_points = models.FloatField(default=0.0, editable=False)
    mean_score_as_reporter = models.FloatField(default=0.0, editable=False)
    mean_score_as_opponent = models.FloatField(default=0.0, editable=False)
    mean_score_as_reviewer = models.FloatField(default=0.0, editable=False)
    tot_score_as_reporter = models.FloatField(default=0.0, editable=False)
    tot_score_as_opponent = models.FloatField(default=0.0, editable=False)
    tot_score_as_reviewer = models.FloatField(default=0.0, editable=False)

    # functions
    def fullname(self):
        """
        :return: return the full name of the participant
        """
        return self.name + ' ' + self.surname

    def __unicode__(self):
        """
        :return: return the full name of the participant
        """
        return self.fullname()

    def update_scores(self):
        # print "Updating scores for", self
        rounds_as_reporter = Round.objects.filter(reporter=self)
        rounds_as_opponent = Round.objects.filter(opponent=self)
        rounds_as_reviewer = Round.objects.filter(reviewer=self)

        self.tot_score_as_reporter = sum(
            [round.score_reporter for round in rounds_as_reporter]
        )
        self.tot_score_as_opponent = sum(
            [round.score_opponent for round in rounds_as_opponent]
        )
        self.tot_score_as_reviewer = sum(
            [round.score_reviewer for round in rounds_as_reviewer]
        )

        self.mean_score_as_reporter = self.tot_score_as_reporter / max(
            len(rounds_as_reporter), 1
        )
        self.mean_score_as_opponent = self.tot_score_as_opponent / max(
            len(rounds_as_opponent), 1
        )
        self.mean_score_as_reviewer = self.tot_score_as_reviewer / max(
            len(rounds_as_reviewer), 1
        )

        res = 0.0
        res += sum([round.points_reporter for round in rounds_as_reporter])
        res += self.tot_score_as_opponent * 2.0
        res += self.tot_score_as_reviewer

        self.total_points = res

        self.save()

    def set_personal_score(self):
        pr = params.personal_ranking
        self.personal_score = 0

        rounds = Round.objects.filter(pf_number__lte=pr['up_to_fight'])

        for r in rounds.filter(reporter=self):
            if r.score_reporter > pr['rep_threshold']:
                self.personal_score += (r.score_reporter - pr['rep_threshold']) * pr[
                    'rep_coeff'
                ]

        for r in rounds.filter(opponent=self):
            if r.score_opponent > pr['opp_threshold']:
                self.personal_score += (r.score_opponent - pr['opp_threshold']) * pr[
                    'opp_coeff'
                ]

        for r in rounds.filter(reviewer=self):
            if r.score_reviewer > pr['rev_threshold']:
                self.personal_score += (r.score_reviewer - pr['rev_threshold']) * pr[
                    'rev_coeff'
                ]

    @classmethod
    def fast_team_ranking(cls, team):
        participants = Participant.objects.filter(
            role='TM', team=team
        ) | Participant.objects.filter(role='TC', team=team)
        return sorted(participants, key=lambda x: x.total_points)[::-1]


class Problem(models.Model):
    """
    This model represents one of the 17 problems
    """

    name = models.CharField(max_length=50, default=None)
    description = models.TextField(max_length=4096, default=None)
    author = models.CharField(blank=True, max_length=128, default='')

    mean_score_of_reporters = models.FloatField(default=0.0, editable=False)
    mean_score_of_opponents = models.FloatField(default=0.0, editable=False)
    mean_score_of_reviewers = models.FloatField(default=0.0, editable=False)

    def __unicode__(self):
        return self.name

    def status(self, verbose=True, meangradesonly=False):
        """
        Compute mean grades of the problem

        :return:
        """

        # first, get a list of who presented what
        rounds = Round.objects.filter(problem_presented=self)
        reporters = []
        opponents = []
        reviewers = []
        for round in rounds:
            if len(JuryGrade.objects.filter(round=round)) > 0:
                if round.reporter_team and round.score_reporter:
                    reporters.append(
                        {
                            "name": round.reporter_team.name,
                            "round": round,
                            "value": round.score_reporter,
                        }
                    )
                if round.opponent_team and round.score_opponent:
                    opponents.append(
                        {
                            "name": round.opponent_team.name,
                            "round": round,
                            "value": round.score_opponent,
                        }
                    )
                if round.reviewer_team and round.score_reviewer:
                    reviewers.append(
                        {
                            "name": round.reviewer_team.name,
                            "round": round,
                            "value": round.score_reviewer,
                        }
                    )

        # TODO: replace "value" with "score" for better readability
        # TODO: the algorithm looks EXTRA WEIRD. Probably all this code should be refactored
        # use this to compute the mean grades
        meangrades = {
            "report": mean([reporter["value"] for reporter in reporters]),
            "opposition": mean([opponent["value"] for opponent in opponents]),
            "review": mean([reviewer["value"] for reviewer in reviewers]),
        }

        if meangradesonly == False:
            # then, reorder that list per teams
            myteamsnames = list(
                sorted([elt["name"] for elt in reporters + opponents + reviewers])
            )

            teamresults = []
            for name in myteamsnames:
                if not name in [teamresult["name"] for teamresult in teamresults]:
                    teamresult = {}
                    teamresult["name"] = name

                    # They can be multiple report/oppos/review on the same problem by the same team !!!
                    reports = []
                    oppositions = []
                    reviews = []
                    # get the scores from presentations
                    for reporter in reporters:
                        if reporter["name"] == name:
                            reports.append(
                                {"round": reporter["round"], "value": reporter["value"]}
                            )
                    # get the scores from oppositions
                    for opponent in opponents:
                        if opponent["name"] == name:
                            oppositions.append(
                                {"round": opponent["round"], "value": opponent["value"]}
                            )
                    # get the scores from reviews
                    for reviewer in reviewers:
                        if reviewer["name"] == name:
                            reviews.append(
                                {"round": reviewer["round"], "value": reviewer["value"]}
                            )

                    teamresult["reports"] = reports
                    teamresult["oppositions"] = oppositions
                    teamresult["reviews"] = reviews

                    teamresults.append(teamresult)
                else:
                    pass

            return (meangrades, teamresults)
        else:
            return meangrades

    def update_scores(self):
        # print "Updating scores for", self
        rounds = Round.objects.filter(problem_presented=self)

        self.mean_score_of_reporters = mean([round.score_reporter for round in rounds])
        self.mean_score_of_opponents = mean([round.score_opponent for round in rounds])
        self.mean_score_of_reviewers = mean([round.score_reviewer for round in rounds])

        self.save()


class Team(models.Model):
    """
    This model represent a team, to which all the participants belong to
    """

    POOL_CHOICES = (('A', 'Pool A'), ('B', 'Pool B'), ('O', 'Not attributed'))

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, null=True, blank=True, default=None)
    IOC = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Team_' + params.instance_name,
        verbose_name="Admin",
    )
    pool = models.CharField(
        max_length=1, choices=POOL_CHOICES, verbose_name='Pool', null=True, blank=True
    )

    total_points = models.FloatField(default=0.0, editable=False)
    semi_points = models.FloatField(default=0.0, editable=False)
    final_points = models.FloatField(default=0.0, editable=False)
    is_in_semi = models.BooleanField(default=False, editable=True)
    is_in_final = models.BooleanField(default=False, editable=True)
    bonus_points = models.FloatField(default=0.0, editable=params.manual_bonus_points)
    nrounds_as_rep = models.IntegerField(default=0, editable=False)
    nrounds_as_opp = models.IntegerField(default=0, editable=False)
    nrounds_as_rev = models.IntegerField(default=0, editable=False)

    def __unicode__(self):

        return self.name

    def presentation_coefficients(self, verbose=False):
        """
        Modify the presentation coefficient from a given round up to the end of the physics fights if more than three problems are tactically rejected.

        The coefficient loses 0.2 points for every additional rejection. This penality is carried over all the subsequents rounds, but disappear for the Final

        :param verbose: Verbosity flag
        :return: Return a list with the coefficient for every round
        """

        eternalrejections = EternalRejection.objects.filter(
            round__reporter_team=self, extra_free=False
        )

        beforetactical = []
        netrej = 0
        for pf in selective_fights_and_semifinals:
            netrej += len(eternalrejections.filter(round__pf_number=pf))
            beforetactical.append(
                3.0 - params.reject_malus * max(0, (netrej - params.netreject_max))
            )

        # get all the tactical rejections
        rejections = TacticalRejection.objects.filter(
            round__reporter_team=self, extra_free=False
        )

        prescoeffs = []
        npenalities = 0
        if verbose:
            print(
                (
                    "=" * 20,
                    "Tactical Rejection Penalites for Team %s" % self.name,
                    "=" * 20,
                )
            )
        for ind, pf in enumerate(selective_fights_and_semifinals):
            pfrejections = [
                rejection for rejection in rejections if rejection.round.pf_number == pf
            ]
            if verbose:
                print(
                    (
                        "%i tactical rejections by Team %s in Physics Fight %i"
                        % (len(pfrejections), self, pf)
                    )
                )
            if len(pfrejections) > params.npfreject_max:
                npenalities += len(pfrejections) - params.npfreject_max
            if verbose:
                if npenalities > 0:
                    print(
                        (
                            "Penality of %.1f points on the Reporter Coefficient"
                            % float(params.reject_malus * npenalities)
                        )
                    )
                else:
                    print("No penality")
            prescoeffs.append(beforetactical[ind] - params.reject_malus * npenalities)

        # add the coeff for the final, 3.0 by default
        if params.with_final_pf:
            prescoeffs.append(3.0)

        return prescoeffs

    def get_scores_for_rounds(self, rounds, include_bonus=True):

        rounds_as_reporter = rounds.filter(reporter_team=self)
        rounds_as_opponent = rounds.filter(opponent_team=self)
        rounds_as_reviewer = rounds.filter(reviewer_team=self)

        res = 0.0

        res += sum([round.points_reporter for round in rounds_as_reporter])
        res += sum([round.points_opponent for round in rounds_as_opponent])
        res += sum([round.points_reviewer for round in rounds_as_reviewer])

        if include_bonus:
            # Bonus points for winning the fight are stored in a round
            # at which the appropriate team was the reporter
            res += sum([round.bonus_points_reporter for round in rounds_as_reporter])

        return (
            res,
            len(rounds_as_reporter),
            len(rounds_as_opponent),
            len(rounds_as_reviewer),
        )

    def update_scores(self):
        # print "Updating scores for", self

        qfrounds = Round.objects.filter(pf_number__range=(1, params.npf))
        qfscores = self.get_scores_for_rounds(qfrounds)

        self.total_points = qfscores[0]
        self.nrounds_as_rep = qfscores[1]
        self.nrounds_as_opp = qfscores[2]
        self.nrounds_as_rev = qfscores[3]

        if params.manual_bonus_points:
            self.total_points += self.bonus_points

        if self.is_in_semi:
            semirounds = Round.objects.filter(
                pf_number__range=(
                    params.npf + 1,
                    params.npf + params.semifinals_quantity,
                )
            )
            self.semi_points = self.get_scores_for_rounds(semirounds)[0]
            if not params.reset_points_before_semi:
                self.semi_points += self.total_points

        if self.is_in_final:
            finalrounds = Round.objects.filter(pf_number=final_fight_number)
            self.final_points = self.get_scores_for_rounds(finalrounds)[0]
            if not params.reset_points_before_final:
                self.final_points += self.total_points

        self.save()

        participants = Participant.objects.filter(team=self)
        for p in participants:
            p.update_scores()

    @classmethod
    def fast_ranking(cls):
        teams = cls.objects.all()
        teams = sorted(teams, key=lambda x: x.total_points, reverse=True)
        return teams

    def problems(self, verbose=False, currentround=None):
        """
        Get all the problems that I cannot present(already presented or eternal rejection) and cannot oppose(already opposed)

        :param verbose: verbosity Flag
        :param currentround: A Round instance. Return all the unpresentable problems before the current round. If none, return on all the round. This sentence is terribly unclear. Rephrase.

        :return: tuple of three lists. each list contains the problems that are eternally rejected, already presented and already opposed
        """

        if verbose:
            print(("=" * 20, "Problems of Team %s" % self.name, "=" * 20))
        noproblems = []

        if currentround != None:
            pf_number = currentround.pf_number
        else:  # TODO: remove these stupid 999 values and implement the pf rejection properly
            pf_number = 999

        # the eternal rejection
        eternal_rejections = EternalRejection.objects.filter(round__reporter__team=self)
        # assert len(eternal_rejections) < 2, "Team %s has more than one eternal rejection. This is forbidden!" % self.name
        # Well, apparently it is...
        reject = []

        for eternal_rejection in eternal_rejections:
            if eternal_rejection.round.pf_number < pf_number:
                if verbose:
                    print(
                        (
                            "Team %s rejected eternally problem %s"
                            % (self.name, eternal_rejection.problem.name)
                        )
                    )
                reject.append(eternal_rejection.problem)

        noproblems.append(reject)

        # now all the problems already presented
        rounds = Round.objects.filter(reporter__team=self)
        rounds = [round for round in rounds if round.pf_number < pf_number]
        presented = []
        for round in rounds:
            if verbose:
                print(
                    ("In %s, I presented problem %s" % (round, round.problem_presented))
                )
            presented.append(round.problem_presented)
        noproblems.append(presented)

        # and problems already opposed
        rounds = Round.objects.filter(opponent__team=self)
        rounds = [round for round in rounds if round.pf_number < pf_number]
        opposed = []
        for round in rounds:
            if verbose:
                print(
                    ("In %s, I opposed problem %s" % (round, round.problem_presented))
                )
            opposed.append(round.problem_presented)
        noproblems.append(opposed)

        assert len(noproblems) == 3, "Something wrong with your rejected problem..."
        return noproblems


class Room(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=2083, blank=True, default='')

    def __unicode__(self):
        return self.name

    @property
    def get_link(self):
        return self.link

    def ident(self):
        rooms = Room.objects.all()
        for ind, room in enumerate(rooms):
            if room == self:
                return ind + 1


class Jury(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    surname = models.CharField(max_length=50, verbose_name='Surname')

    def fullname(self):
        """
        :return: return the full name of the jury member
        """
        return self.name + ' ' + self.surname

    def __unicode__(self):
        return self.fullname()

    email = models.EmailField(
        help_text='This address will be used to send the participant every important infos about the tournament.',
        verbose_name='Email',
        blank=True,
    )
    affiliation = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Affiliation to display',
        help_text='Will be used for export (badges and web).',
    )
    team = models.ForeignKey('Team', null=True, blank=True)
    # TODO: unhardcode PF number!
    pf1 = models.BooleanField(default=False, verbose_name='PF 1')
    pf2 = models.BooleanField(default=False, verbose_name='PF 2')
    pf3 = models.BooleanField(default=False, verbose_name='PF 3')
    pf4 = models.BooleanField(default=False, verbose_name='PF 4')
    final = models.BooleanField(default=False, verbose_name='Final')
    remark = models.TextField(blank=True, verbose_name='Remarks')

    class Meta:
        verbose_name = "Juror"


class Round(models.Model):
    pf_number = models.IntegerField(
        choices=(((ind + 1, params.fights['names'][ind]) for ind in range(npf_tot))),
        default=None,
    )
    round_number = models.IntegerField(
        choices=(
            (
                (ind + 1, 'Round ' + str(ind + 1))
                for ind in range(params.max_rounds_in_pf)
            )
        ),
        default=None,
    )
    room = models.ForeignKey(Room)
    reporter_team = models.ForeignKey(
        Team, related_name='reporterteam', blank=True, null=True
    )
    opponent_team = models.ForeignKey(
        Team, related_name='opponentteam', blank=True, null=True
    )
    reviewer_team = models.ForeignKey(
        Team, related_name='reviewerteam', blank=True, null=True
    )
    reporter = models.ForeignKey(
        Participant, related_name='reporter_name_1', blank=True, null=True
    )
    reporter_2 = models.ForeignKey(
        Participant, related_name='reporter_name_2', blank=True, null=True
    )
    opponent = models.ForeignKey(
        Participant, related_name='opponent_name', blank=True, null=True
    )
    reviewer = models.ForeignKey(
        Participant, related_name='reviewer_name', blank=True, null=True
    )
    problem_presented = models.ForeignKey(Problem, blank=True, null=True)
    submitted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    score_reporter = models.FloatField(default=0.0, editable=False)
    score_opponent = models.FloatField(default=0.0, editable=False)
    score_reviewer = models.FloatField(default=0.0, editable=False)

    points_reporter = models.FloatField(default=0.0, editable=False)
    points_opponent = models.FloatField(default=0.0, editable=False)
    points_reviewer = models.FloatField(default=0.0, editable=False)

    # Bonus points for the reporters team are stored in the Round
    # at which the team was reporting
    bonus_points_reporter = models.FloatField(
        default=0.0, editable=params.manual_bonus_points
    )

    def __unicode__(self):
        try:
            fight_name = params.fights['names'][self.pf_number - 1]
        except:
            # TODO: send a report to the admins!
            fight_name = 'Unknown Fight (possibly an error!)'

        return (
            fight_name
            + " | Round %i" % self.round_number
            + (" | Room " + self.room.name if self.pf_number <= params.npf else "")
        )

    def save(self, *args, **kwargs):
        jurygrades = JuryGrade.objects.filter(round=self)
        print(("Update scores for", self))

        reporter_grades = list(
            sorted([jurygrade.grade_reporter for jurygrade in jurygrades])
        )
        opponent_grades = list(
            sorted([jurygrade.grade_opponent for jurygrade in jurygrades])
        )
        reviewer_grades = list(
            sorted([jurygrade.grade_reviewer for jurygrade in jurygrades])
        )

        ngrades = min(len(reporter_grades), len(opponent_grades), len(reviewer_grades))
        if ngrades > 1:
            self.score_reporter = special_mean(reporter_grades)
            self.score_opponent = special_mean(opponent_grades)
            self.score_reviewer = special_mean(reviewer_grades)

            prescoeff = self.reporter_team.presentation_coefficients()[
                self.pf_number - 1
            ]

            self.points_reporter = self.score_reporter * prescoeff
            self.points_opponent = self.score_opponent * 2.0
            self.points_reviewer = self.score_reviewer

            if params.score_precision != None:
                self.points_reporter = round(
                    self.points_reporter, params.score_precision
                )
                self.points_opponent = round(
                    self.points_opponent, params.score_precision
                )
                self.points_reviewer = round(
                    self.points_reviewer, params.score_precision
                )

        super(Round, self).save(*args, **kwargs)

    def ident(self):
        return "%s%s%s" % (self.pf_number, self.round_number, self.room.ident())

    def can_add_next(self):
        # We don't want to create the next Round, if...

        # ...maximal quantity of Rounds has been already reached, i.e. current Round is the last one
        if self.round_number >= params.max_rounds_in_pf:
            return False

        # ...current Round has no number
        if self.round_number == None:
            return False

        roomrounds = Round.objects.filter(pf_number=self.pf_number, room=self.room)

        # ...the next Round already exists
        if len(roomrounds.filter(round_number=self.round_number + 1)) > 0:
            return False

        teams_involved = get_involved_teams_dict(roomrounds)

        # If a team (probably a reviewer) is not stated - just omit it
        if params.optional_reviewers:
            teams_involved.pop(None, None)

        # ... each team has already done a report (approximately)
        if self.round_number >= len(teams_involved):
            return False

        return True

    def add_next(self):

        # Create a whole new Round
        next_round = Round()

        # Basic properties of the new Round
        next_round.pf_number = self.pf_number
        next_round.room = self.room
        next_round.round_number = self.round_number + 1

        # The Teams undercome a loop
        # TODO: 4-fights and 2-fights
        next_round.reporter_team = self.opponent_team
        next_round.opponent_team = self.reviewer_team
        next_round.reviewer_team = self.reporter_team

        # 2-fights
        if params.optional_reviewers and next_round.round_number == 2:
            if next_round.reviewer_team != None and next_round.reporter_team == None:
                next_round.reporter_team = next_round.reviewer_team
                next_round.reviewer_team = None
            elif next_round.reviewer_team != None and next_round.opponent_team == None:
                next_round.opponent_team = next_round.reviewer_team
                next_round.reviewer_team = None

        # Jurors! They are the same
        jurygrades = JuryGrade.objects.filter(round=self)

        # We have to save the round twice to be able to link jury grades to it
        # See also https://github.com/IPTnet/ipt_connect/issues/89
        next_round.save()

        for grade in jurygrades:
            empty_grade = JuryGrade()
            empty_grade.round = next_round
            empty_grade.jury = grade.jury

            # Set the grades to 0 - otherwise we run into a crash
            empty_grade.grade_reporter = 0
            empty_grade.grade_opponent = 0
            empty_grade.grade_reviewer = 0

            empty_grade.save()

        next_round.save()

        return next_round

    class Meta:
        permissions = (("update_all", "Can see and trigger update_all links"),)


class JuryGrade(models.Model):
    round = models.ForeignKey(Round, null=True)
    jury = models.ForeignKey(Jury)

    grade_reporter = models.IntegerField(choices=grade_choices, default=None)

    grade_opponent = models.IntegerField(choices=grade_choices, default=None)

    grade_reviewer = models.IntegerField(choices=grade_choices, default=None)

    def __unicode__(self):
        return "Grade of %s" % self.jury.name

    def info(self):
        print(("=" * 36))
        print(("Grade of %s" % self.jury.name))
        print((self.round))
        print(
            (
                "Reporter %s from %s : %i"
                % (self.round.name_reporter, self.round.reporter, self.grade_reporter)
            )
        )
        print(
            (
                "Opponent %s from %s : %i"
                % (self.round.name_opponent, self.round.opponent, self.grade_opponent)
            )
        )
        print(
            (
                "Reviewer %s from %s : %i"
                % (self.round.name_reviewer, self.round.reviewer, self.grade_reviewer)
            )
        )


class TacticalRejection(models.Model):
    round = models.ForeignKey(Round, null=True)
    problem = models.ForeignKey(Problem)
    extra_free = models.BooleanField(
        default=False,
        verbose_name='Extra free rejection',
        editable=params.enable_extra_free_tactical_rejections,
    )

    def __unicode__(self):
        return "Problem rejected : %s" % self.problem.pk


class EternalRejection(models.Model):
    round = models.ForeignKey(Round, null=True)
    problem = models.ForeignKey(Problem)
    extra_free = models.BooleanField(
        default=False,
        verbose_name='Extra free rejection',
        editable=params.enable_extra_free_eternal_rejections,
    )

    def __unicode__(self):
        return "Problem rejected : %s" % self.problem.pk


class AprioriRejection(models.Model):
    team = models.ForeignKey(Team, null=True)
    problem = models.ForeignKey(Problem)

    def __unicode__(self):
        # TODO: also print the Team
        return "Problem rejected : %s" % self.problem.pk


# method for updating Teams and Participants when rounds are saved
@receiver(post_save, sender=Round, dispatch_uid="update_participant_team_points")
@receiver(post_delete, sender=Round, dispatch_uid="update_participant_team_points")
def update_points_condition(sender, instance, **kwargs):
    if not SiteConfiguration.get_solo().update_scores_manually:
        update_points(sender, instance)


def update_points(sender, instance, **kwargs):
    print(("Updating Round %s" % instance))
    if (
        (instance.reporter_team is None)
        or (instance.opponent_team is None)
        or (instance.reviewer_team is None and not params.optional_reviewers)
        or (instance.problem_presented is None)
    ):
        # then all teams aren't yet defined, there is no need to compute scores
        pass
    else:
        teams = [instance.reporter_team, instance.opponent_team, instance.reviewer_team]
        # then compute teams (and participants) scores
        for team in teams:
            if not team is None:
                team.update_scores()

        # and the problem mean scores
        instance.problem_presented.update_scores()


class SiteConfiguration(SingletonModel):
    only_staff_access = models.BooleanField(default=False)
    display_link_to_final_on_ranking_page = models.BooleanField(default=False)
    display_final_ranking_on_ranking_page = models.BooleanField(default=False)

    do_not_display_tactical_rejections = models.BooleanField(
        default=False, editable=params.enable_tactical_rejections
    )

    display_eternal_rejections_on_team_page = models.BooleanField(
        default=True, editable=params.enable_eternal_rejections
    )

    update_scores_manually = models.BooleanField(default=False)
    image_link_URL = models.URLField(default="http://blueballfixed.ytmnd.com/")
    image_URL = models.URLField(default="http://i.imgur.com/QH8aoXL.gif")
    image_repeat_count = models.IntegerField(default=6)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


def get_involved_teams_dict(round_list):
    teams_dict = {}
    for r in round_list:
        teams_dict[r.reporter_team] = {}
        teams_dict[r.opponent_team] = {}
        teams_dict[r.reviewer_team] = {}
    return teams_dict


def update_bonus_points():
    # the rounds must be saved first !
    rounds = Round.objects.all()

    for round in rounds.filter(round_number=2):

        bonuspts = {}
        thispfrounds = Round.objects.filter(pf_number=round.pf_number).filter(
            room=round.room
        )
        thispfteams = get_involved_teams_dict(thispfrounds)

        # If a team (probably a reviewer) is not stated - just omit it
        if params.optional_reviewers:
            thispfteams.pop(None, None)

        thispfteams = thispfteams.keys()

        if thispfrounds.count() != len(thispfteams):
            continue

        # set the bonus points to zero
        for team in thispfteams:
            bonuspts[team] = 0.0

        points_dict = {}
        for team in thispfteams:
            points_dict[team] = team.get_scores_for_rounds(
                rounds=thispfrounds, include_bonus=False
            )

        # get teams sorted by total points for the physics fight
        team_podium = sorted(thispfteams, key=lambda t: points_dict[t], reverse=True)
        points_list = [points_dict[t][0] for t in team_podium]

        bonus_list = distribute_bonus_points(points_list)

        # TODO: rewrite in python-ish way
        for i in range(len(points_list)):
            bonuspts[team_podium[i]] = bonus_list[i]

        with transaction.atomic():
            # It is safe to use atomic transaction here,
            # because the changes which are saved to the rounds
            # do not affect the .filter() condition
            # and, moreover, each round is edited only once
            for team in team_podium:
                round_with_report = thispfrounds.filter(
                    pf_number=round.pf_number, reporter_team=team
                )
                if round_with_report.count() == 1:
                    # We suppose that one team can be a reporter once per PF
                    round_with_report = round_with_report[0]
                    if (
                        round_with_report.bonus_points_reporter
                        != bonuspts[team]
                        * params.fights['bonus_multipliers'][round.pf_number - 1]
                    ):
                        round_with_report.bonus_points_reporter = (
                            bonuspts[team]
                            * params.fights['bonus_multipliers'][round.pf_number - 1]
                        )
                        # TODO: get rid of save()
                        round_with_report.save()


def remove_phantom_grades():
    allrounds = Round.objects.all()
    allgrades = JuryGrade.objects.all()

    # remove the phantom grades, if any
    rgrades = []
    for round in allrounds:
        mygrades = JuryGrade.objects.filter(round=round)
        for grade in mygrades:
            rgrades.append(grade)

    i = 0
    for grade in allgrades:
        if grade not in rgrades:
            i += 1
            grade.delete()
    print("I removed %i phantom grades..." % i)


update_signal = Signal()


@receiver(update_signal, sender=Round, dispatch_uid="update_all")
def update_all(sender, **kwargs):
    old_time = time.time()

    remove_phantom_grades()

    if not params.manual_bonus_points:
        print("Updating bonus points...")
        update_bonus_points()
        print("Done!")

    # The query must be refreshed: update_bonus_points() changed rounds and saved them
    allrounds = Round.objects.all()
    allrounds = sorted(allrounds, key=lambda round: round.round_number, reverse=False)
    allteams = Team.objects.all()

    # if 1:
    with transaction.atomic():
        # update rounds
        for round in allrounds:
            # we do not want to add the bonus points now, let's keep that for a next step (just to check, that might disappear later)
            update_points(sender, instance=round)
            round.save()
            # sys.exit()

        print(("=" * 15))
        for team in allteams:
            # print "----"
            # print team.name, team.total_points
            team.save()

        # just in case, update the problems
        for pb in Problem.objects.all():
            pb.update_scores()

    return (
        "Teams, participants and problems updated in ",
        int(time.time() - old_time),
        " seconds !",
    )

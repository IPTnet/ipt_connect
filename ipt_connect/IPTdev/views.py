# coding: utf8
import csv

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.translation import get_language

from cache_per_user import cache_per_user as cache_page
from forms import UploadForm
from model_SupplementaryMaterial import SupplementaryMaterial
from models import *


def home(request):
    text = (
        """<h1>"""
        + params.NAME.full
        + """</h1>

			  <p>Starting soon !</p>"""
    )

    return HttpResponse(text)


cache_duration_short = 1 * 1
cache_duration = 20 * 1


def ninja_test(user):
    return user.is_staff or not SiteConfiguration.get_solo().only_staff_access


@cache_page(cache_duration_short)
def soon(request):
    return render(
        request,
        '%s/bebacksoon.html' % params.instance_name,
        {
            'params': params,
        },
    )


#####################################################
################# SUPER USERS VIEWS #################
@user_passes_test(lambda u: u.is_superuser)
def participants_trombinoscope(request):
    participants = Participant.objects.all().order_by('team', 'surname')

    return render(
        request,
        '%s/participants_trombinoscope.html' % params.instance_name,
        {
            'participants': participants,
        },
    )


@user_passes_test(lambda u: u.is_superuser or u.username == 'magnusson')
def participants_export(request):
    participants = Participant.objects.all().order_by('team', 'role', 'name')

    return render(
        request,
        '%s/participants_export.html' % params.instance_name,
        {
            'participants': participants,
            'params': params,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def participants_export_web(request):
    participants = Participant.objects.exclude(role='ACC').order_by(
        'team', 'role', 'surname'
    )

    return render(
        request,
        '%s/listing_participants_web.html' % params.instance_name,
        {
            'participants': participants,
            'params': params,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def export_csv_ranking_timeline(request):
    import unicodecsv as csv
    from django.http import HttpResponse

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ranking_timeline.csv"'

    writer = csv.writer(response)

    allteams = list(Team.objects.all())
    writer.writerow([' '] + allteams)

    previous_scores = {}
    for team in allteams:
        previous_scores[team] = 0

    for pf_number in selective_fights_and_semifinals:
        fight_rounds = Round.objects.filter(pf_number=pf_number)
        for round_number in range(1, params.max_rounds_in_pf + 1):
            current_rounds = fight_rounds.filter(round_number=round_number)
            for team in allteams:
                previous_scores[team] += team.get_scores_for_rounds(
                    rounds=current_rounds, include_bonus=False
                )[0]

            writer.writerow(
                [
                    '%s | Round %s'
                    % (params.fights['names'][pf_number - 1], round_number)
                ]
                + [previous_scores[team] for team in allteams]
            )

        for team in allteams:
            previous_scores[team] += (
                team.get_scores_for_rounds(rounds=fight_rounds, include_bonus=True)[0]
                - team.get_scores_for_rounds(rounds=fight_rounds, include_bonus=False)[
                    0
                ]
            )
        writer.writerow(
            ['%s | Bonuses' % params.fights['names'][pf_number - 1]]
            + [previous_scores[team] for team in allteams]
        )

    return response


@user_passes_test(lambda u: u.is_superuser)
def jury_export(request):
    jurys = Jury.objects.all().order_by('surname')

    return render(
        request,
        '%s/listing_jurys.html' % params.instance_name,
        {
            'jurys': jurys,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def jury_export_web(request):
    jurys = Jury.objects.filter(team=None).order_by('surname')

    return render(
        request,
        '%s/listing_jurys_web.html' % params.instance_name,
        {
            'jurys': jurys,
        },
    )


@user_passes_test(lambda u: u.has_perm(params.instance_name + '.update_all'))
def update_all(request):
    list_receivers = update_signal.send(sender=Round)

    assert len(list_receivers) == 1, "len(list_receivers) is not 1 in view update_all"

    return HttpResponse(list_receivers[0][1])


@user_passes_test(lambda u: u.has_perm(params.instance_name + '.add_round'))
def round_add_next(request, pk):
    try:
        current_round = Round.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()

    if not current_round.can_add_next():
        raise Http404()
        # TODO: 500? 403? More informative error?

    next_round = current_round.add_next()

    # TODO: a more sane URL!
    return round_detail(request, next_round.pk)


@user_passes_test(lambda u: u.has_perm(params.instance_name + '.update_all'))
def verify_all(request):
    all_rounds = Round.objects.all()
    checks_successful = []
    checks_with_warnings = []
    checks_with_errors = []

    rounds_with_reporter_team_mismatch = []
    rounds_with_opponent_team_mismatch = []
    rounds_with_reviewer_team_mismatch = []
    rounds_with_reporter_2_team_mismatch = []

    for r in all_rounds:
        if r.reporter and r.reporter.team != r.reporter_team:
            rounds_with_reporter_team_mismatch.append(r)
        if r.opponent and r.opponent.team != r.opponent_team:
            rounds_with_opponent_team_mismatch.append(r)
        if r.reviewer and r.reviewer.team != r.reviewer_team:
            rounds_with_reviewer_team_mismatch.append(r)
        if r.reporter_2 and r.reporter_2.team != r.reporter_team:
            rounds_with_reporter_2_team_mismatch.append(r)

    simple_checks_for_rounds = [
        (
            all_rounds.filter(pf_number__gt=npf_tot),
            'Some Rounds have unexpected Fight number',
            'Each Round has a sane Fight number',
            checks_with_errors,
        ),
        (
            all_rounds.filter(problem_presented=None),
            'Some Rounds have no Problem presented',
            'Each Round has a presented Problem',
            checks_with_errors,
        ),
        (
            all_rounds.filter(reporter=None).exclude(reporter_2=None),
            'Some Rounds have no Reporter specified but a Coreporter specified',
            'If a Round has a Coreporter, it has a Reporter',
            checks_with_errors,
        ),
        (
            all_rounds.filter(reporter=None),
            'Some Rounds have no Reporter specified',
            'Each Round has a Reporter',
            checks_with_errors,
        ),
        (
            all_rounds.filter(opponent=None),
            'Some Rounds have no Opponent specified',
            'Each Round has an Opponent',
            checks_with_errors,
        ),
        (
            all_rounds.filter(reviewer=None),
            'Some Rounds have no Reviewer specified',
            'Each Round has a Reviewer',
            checks_with_errors
            if not params.optional_reviewers
            else checks_with_warnings,
        ),
        (
            all_rounds.filter(reporter_team=None),
            'Some Rounds have no Reporter Team specified',
            'Each Round has a Reporter Team',
            checks_with_errors,
        ),
        (
            all_rounds.filter(opponent_team=None),
            'Some Rounds have no Opponent Team specified',
            'Each Round has an Opponent Team',
            checks_with_errors,
        ),
        (
            all_rounds.filter(reviewer_team=None),
            'Some Rounds have no Reviewer Team specified',
            'Each Round has an Reviewer Team',
            checks_with_errors
            if not params.optional_reviewers
            else checks_with_warnings,
        ),
        (
            rounds_with_reporter_team_mismatch,
            'Some Rounds have a Reporter that is not a member of Reporter Team',
            'For each Round a Reporter (if any) is a member of Reporter Team',
            checks_with_errors,
        ),
        (
            rounds_with_opponent_team_mismatch,
            'Some Rounds have an Opponent that is not a member of Opponent Team',
            'For each Round an Opponent (if any) is a member of Opponent Team',
            checks_with_errors,
        ),
        (
            rounds_with_reviewer_team_mismatch,
            'Some Rounds have a Reviewer that is not a member of Reviewer Team',
            'For each Round a Reviewer (if any) is a member of Reviewer Team',
            checks_with_errors,
        ),
        (
            rounds_with_reporter_2_team_mismatch,
            'Some Rounds have a Coreporter that is not a member of Reporter Team',
            'For each Round a Coreporter (if any) is a member of Reporter Team',
            checks_with_errors,
        ),
    ]

    for check in simple_checks_for_rounds:
        rounds_with_the_issue = check[0]

        if rounds_with_the_issue:
            check[3].append(
                (
                    check[1],
                    list(rounds_with_the_issue),
                )
            )
        else:
            checks_successful.append(check[2])

    return render(
        request,
        '%s/verify_all.html' % params.instance_name,
        {
            'params': params,
            'checks_successful': checks_successful,
            'checks_with_warnings': checks_with_warnings,
            'checks_with_errors': checks_with_errors,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def jury_export_csv(request):
    import unicodecsv as csv
    from django.http import HttpResponse

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jurors.csv"'

    writer = csv.writer(response)

    for juror in Jury.objects.all():
        writer.writerow(
            [
                juror.pk,
                juror.name,
                juror.surname,
                juror.affiliation,
                juror.team,
                # TODO: unhardcode PF number!
                juror.pf1,
                juror.pf2,
                juror.pf3,
                juror.pf4,
            ]
        )

    return response


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def participants_overview(request):
    participants = Participant.objects.filter(role='TM') | Participant.objects.filter(
        role='TC'
    )
    pr = params.personal_ranking
    for participant in participants:
        participant.allpoints = (
            participant.tot_score_as_reporter
            + participant.tot_score_as_opponent
            + participant.tot_score_as_reviewer
        )

        rounds_as_reporter = Round.objects.filter(reporter=participant)
        rounds_as_opponent = Round.objects.filter(opponent=participant)
        rounds_as_reviewer = Round.objects.filter(reviewer=participant)
        rounds_as_participant = (
            rounds_as_reporter | rounds_as_opponent | rounds_as_reviewer
        )

        participant.max_grade_rep = max(
            [r.score_reporter for r in rounds_as_reporter] + [0.0]
        )
        participant.max_grade_opp = max(
            [r.score_opponent for r in rounds_as_opponent] + [0.0]
        )
        participant.max_grade_rev = max(
            [r.score_reviewer for r in rounds_as_reviewer] + [0.0]
        )

        participant.max_grade_tot = max(
            participant.max_grade_rep,
            participant.max_grade_opp,
            participant.max_grade_rev,
        )

        if len(rounds_as_participant) == 0:
            participant.avggrade = 0.0
        else:
            # TODO: all these computations should be performed when a round is saved
            participant.avggrade = participant.allpoints / len(rounds_as_participant)

        if pr['active']:
            participant.set_personal_score()

    participants = sorted(
        participants, key=lambda participant: participant.avggrade, reverse=True
    )

    return render(
        request,
        '%s/participants_overview.html' % params.instance_name,
        {
            'participants': participants,
            'params': params,
            'personal_ranking': pr['active'],
            'sister_tournament_postfix': 'participants',
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def participants_all(request):
    participants = Participant.objects.all().order_by('team', 'surname')

    return render(
        request,
        '%s/participants_all.html' % params.instance_name,
        {
            'participants': participants,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def participant_detail(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()

    rounds = (
        Round.objects.filter(reporter=participant)
        | Round.objects.filter(reporter_2=participant)
        | Round.objects.filter(opponent=participant)
        | Round.objects.filter(reviewer=participant)
    ).order_by('pf_number', 'round_number')

    # TODO: refactor to use each filter separately
    average_grades = []
    for round in rounds:
        if round.reporter == participant:
            average_grades.append(
                {"value": round.score_reporter, "round": round, "role": "reporter"}
            )

        elif round.opponent == participant:
            average_grades.append(
                {"value": round.score_opponent, "round": round, "role": "opponent"}
            )

        elif round.reporter_2 == participant:
            if params.display_coreporters:
                average_grades.append(
                    {
                        "value": round.score_reporter,
                        "round": round,
                        "role": "coreporter",
                    }
                )

        else:
            average_grades.append(
                {"value": round.score_reviewer, "round": round, "role": "reviewer"}
            )

    return render(
        request,
        '%s/participant_detail.html' % params.instance_name,
        {
            'participant': participant,
            'sister_tournament_postfix': 'participants',
            "average_grades": average_grades,
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def jurys_overview(request):
    jurys = Jury.objects.all().order_by('name')

    for jury in jurys:
        mygrades = JuryGrade.objects.filter(jury=jury)
        if mygrades:
            jury.meanrepgrade = mean([grade.grade_reporter for grade in mygrades])
        else:
            jury.meanrepgrade = 0.0
        if mygrades:
            jury.meanoppgrade = mean([grade.grade_opponent for grade in mygrades])
        else:
            jury.meanoppgrade = 0.0
        if mygrades:
            jury.meanrevgrade = mean([grade.grade_reviewer for grade in mygrades])
        else:
            jury.meanrevgrade = 0.0
    return render(
        request,
        '%s/jurys_overview.html' % params.instance_name,
        {
            'jurys': jurys,
            'sister_tournament_postfix': 'jurys',
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def jury_detail(request, pk):
    try:
        jury = Jury.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()

    mygrades = JuryGrade.objects.filter(jury=jury)
    return render(
        request,
        '%s/jury_detail.html' % params.instance_name,
        {
            'jury': jury,
            'grades': mygrades,
            'sister_tournament_postfix': 'jurys',
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def tournament_overview(request):
    return render(
        request,
        '%s/tournament_overview.html' % params.instance_name,
        {
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def teams_overview(request):
    teams = Team.objects.all()
    teams = sorted(teams, key=lambda team: team.name)
    return render(
        request,
        '%s/teams_overview.html' % params.instance_name,
        {
            'teams': teams,
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def team_detail(request, team_name):
    try:
        team = Team.objects.get(name=team_name)
    except ObjectDoesNotExist:
        raise Http404()

    ranking = Team.objects.order_by('-total_points')
    for i, t in enumerate(ranking):
        if t == team:
            team.rank = i + 1
    # team.rank = ranking.index(team) + 1
    participants = Participant.objects.filter(team=team).filter(
        role='TM'
    ) | Participant.objects.filter(team=team).filter(role='TC')

    rankedparticipants = participants.order_by('total_points')

    teamleaders_jury = Jury.objects.filter(team=team)
    val_teamlead = (
        Participant.objects.filter(team=team)
        .filter(role='TL')
        .values('name', 'surname')
    )
    val_jury = Jury.objects.filter(team=team).values('name', 'surname')
    delta_models = val_teamlead.difference(val_jury)
    if delta_models:
        teamleaders = delta_models
    else:
        teamleaders = Participant.objects.none()

    myreprounds = Round.objects.filter(reporter_team=team)
    myopprounds = Round.objects.filter(opponent_team=team)
    myrevrounds = Round.objects.filter(reviewer_team=team)

    allrounds = []

    bonus_points_displayed = 0.0

    if params.manual_bonus_points:
        bonus_points_displayed += team.bonus_points

    for round in myreprounds:
        # if len(JuryGrade.objects.filter(round=round)) > 0:
        if round.score_reporter > 0.0:
            round.myrole = "reporter"
            round.mygrade = round.score_reporter
            allrounds.append(round)
            bonus_points_displayed += round.bonus_points_reporter
            # print team_name, round.pf_number, round.bonus_points_reporter
    for round in myopprounds:
        # if len(JuryGrade.objects.filter(round=round)) > 0:
        if round.score_opponent > 0.0:
            round.myrole = "opponent"
            round.mygrade = round.score_opponent
            allrounds.append(round)
    for round in myrevrounds:
        # if len(JuryGrade.objects.filter(round=round)) > 0:
        if round.score_reviewer > 0.0:
            round.myrole = "reviewer"
            round.mygrade = round.score_reviewer
            allrounds.append(round)

    penalties = []
    prescoeffs = team.presentation_coefficients(verbose=False)

    for ind, p in enumerate(prescoeffs):
        if p != 3.0:
            penalties.append([ind + 1, p])

    if params.enable_apriori_rejections:
        apriori_rejections = AprioriRejection.objects.filter(team=team).order_by(
            'problem'
        )
    else:
        apriori_rejections = ()

    display_eternal_rejections = (
        params.enable_eternal_rejections
        and SiteConfiguration.get_solo().display_eternal_rejections_on_team_page
    )

    if display_eternal_rejections:
        eternal_rejections = EternalRejection.objects.filter(
            round__reporter_team=team
        ).order_by('problem')
    else:
        eternal_rejections = ()

    supplementary_materials = SupplementaryMaterial.objects.filter(team=team).order_by(
        'problem'
    )

    return render(
        request,
        '%s/team_detail.html' % params.instance_name,
        {
            'team': team,
            'participants': rankedparticipants,
            'teamleaders': teamleaders,
            'teamleaders_jury': teamleaders_jury,
            'supplementary_materials': supplementary_materials,
            'allrounds': allrounds,
            'penalties': penalties,
            'eternal_rejections': eternal_rejections,
            'display_eternal_rejections': display_eternal_rejections,
            'apriori_rejections': apriori_rejections,
            'sister_tournament_postfix': 'ranking',
            'bonus_points_displayed': bonus_points_displayed,
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def problems_overview(request):
    problems = Problem.objects.all()
    rounds = Round.objects.all()
    for problem in problems:
        problem.npres = len(rounds.filter(problem_presented=problem))
        problem.meangradrep = problem.mean_score_of_reporters
        problem.meangradopp = problem.mean_score_of_opponents
        problem.meangradrev = problem.mean_score_of_reviewers

    return render(
        request,
        '%s/problems_overview.html' % params.instance_name,
        {
            'sister_tournament_postfix': 'problems',
            'problems': problems,
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def problem_detail(request, pk):
    try:
        problem = Problem.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()

    (meangrades, teamresults) = problem.status(verbose=False)

    supplementary_materials = SupplementaryMaterial.objects.filter(
        problem=problem
    ).order_by('team')

    return render(
        request,
        '%s/problem_detail.html' % params.instance_name,
        {
            'problem': problem,
            'meangrades': meangrades,
            'teamresults': teamresults,
            'supplementary_materials': supplementary_materials,
            'sister_tournament_postfix': 'problems',
            'params': params,
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def rounds(request):
    rounds = Round.objects.all()
    rooms = Room.objects.order_by('name')

    orderedroundsperroom = []
    for room in rooms:
        room_round_list = []
        for pf in selective_fights:
            room_round_list.append(
                Round.objects.filter(pf_number=pf)
                .filter(room=room)
                .order_by('round_number')
            )
        thisroom = {"name": room.name, "link": room.get_link, "rounds": room_round_list}
        orderedroundsperroom.append(thisroom)

    render_data = {
        'params': params,
        'orderedroundsperroom': orderedroundsperroom,
        'selective_fight_names': zip(
            selective_fights, params.fights['names'][: params.npf]
        ),
        'sister_tournament_postfix': 'physics_fights',
    }

    if params.with_final_pf:
        myrounds = Round.objects.filter(pf_number=final_fight_number)
        finalrounds = sorted(myrounds, key=lambda round: round.round_number)
        try:
            finalteams = [
                finalrounds[0].reporter_team,
                finalrounds[0].opponent_team,
                finalrounds[0].reviewer_team,
            ]
            finalpoints = [
                team.points(pfnumber=final_fight_number, bonuspoints=False)
                for team in finalteams
            ]
        except:
            finalteams = ["---", "---", "---"]
            finalpoints = [0, 0, 0]

            finalranking = []
        for team, point in zip(finalteams, finalpoints):
            finalranking.append([team, point])

        render_data.update(
            {
                'final_fight_number': final_fight_number,
                'finalrounds': finalrounds,
                'finalranking': finalranking,
            }
        )

    if params.semifinals_quantity > 0:
        semifinal_rounds = []
        for pf in semifinals:
            semifinal_rounds.append(
                Round.objects.filter(pf_number=pf).order_by('round_number')
            )
        render_data.update(
            {
                'semifinal_data': zip(
                    params.fights['names'][
                        params.npf : params.npf + params.semifinals_quantity
                    ],
                    semifinal_rounds,
                )
            }
        )

    return render(
        request,
        '%s/rounds.html' % params.instance_name,
        render_data,
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def round_detail(request, pk):
    try:
        round = Round.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()

    # TODO: rewrite the following in pythonish way!!!
    from tactics import make_old_fashioned_list_from_tactics_data

    jurygrades = JuryGrade.objects.filter(round=round).order_by('jury__name')
    meangrades = []

    # has the round started ? If so, then reporter_team, opponent_team and reviewer_team must be defined

    started = (
        round.reporter_team != None
        and round.opponent_team != None
        and (round.reviewer_team != None or params.optional_reviewers)
    )

    # participants mean grades. If the fight is finished, then at least some jurygrades must exists
    if len(jurygrades) != 0:
        meangrades.append(round.score_reporter)
        meangrades.append(round.score_opponent)
        if round.reviewer_team or not params.optional_reviewers:
            meangrades.append(round.score_reviewer)
        finished = True
    else:
        finished = False

    if params.enable_tactical_rejections:
        tacticalrejections = TacticalRejection.objects.filter(round=round)
    else:
        tacticalrejections = []

    if params.enable_eternal_rejections:
        eternalrejection = EternalRejection.objects.filter(round=round)
    else:
        eternalrejection = []

    return render(
        request,
        '%s/round_detail.html' % params.instance_name,
        {
            'params': params,
            'round': round,
            'jurygrades': jurygrades,
            'meangrades': meangrades,
            'tacticalrejections': tacticalrejections,
            'eternalrejection': eternalrejection,
            'started': started,
            'finished': finished,
            'unavailable_problems': make_old_fashioned_list_from_tactics_data(round),
            'display_room_name': round.pf_number <= params.npf,
            'display_rejections': params.fights['challenge_procedure'][
                round.pf_number - 1
            ]
            and (params.enable_tactical_rejections or params.enable_eternal_rejections),
            'display_problems_forbidden': params.fights['problems_forbidden'][
                round.pf_number - 1
            ],
            'physics_fight_name': params.fights['names'][round.pf_number - 1],
            'sister_tournament_postfix': 'physics_fights',
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def physics_fight_detail(request, pfid):
    if float(pfid) not in range(1, npf_tot + 1):
        raise Http404()
    rounds = Round.objects.filter(pf_number=pfid)
    rooms = Room.objects.all().order_by('name')

    roomgrades = []
    for room in rooms:
        roomrounds = rounds.filter(room=room).order_by('round_number')

        grades = JuryGrade.objects.filter(
            round__room=room, round__pf_number=pfid
        ).order_by('round__round_number', 'jury__surname')
        gradesdico = {}
        for grade in grades:
            gradesdico[grade.jury] = []
        for grade in grades:
            gradesdico[grade.jury].append(grade)

        juryallgrades = [
            {
                'juryroundsgrades': gradesdico[jury],
                'name': jury.name + " " + jury.surname,
            }
            for jury in gradesdico.keys()
        ]
        print(juryallgrades)

        # meangrades and summary grades
        meanroundsgrades = []

        for round in roomrounds:
            meangrades = []
            meangrades.append(round.score_reporter)
            meangrades.append(round.score_opponent)
            if round.reviewer_team or not params.optional_reviewers:
                meangrades.append(round.score_reviewer)
            meanroundsgrades.append(meangrades)

        teams_involved = get_involved_teams_dict(roomrounds)

        # If a team (probably a reviewer) is not stated - just omit it
        if params.optional_reviewers:
            teams_involved.pop(None, None)

        finished = roomrounds.count() == len(teams_involved)

        if params.display_pf_summary:
            summary_grades = create_summary(roomrounds, teams_involved, finished)
        else:
            summary_grades = None

        infos = {"pf": pfid, "room": room.name, "finished": finished}
        roundsgrades = [juryallgrades, meanroundsgrades, infos, summary_grades]
        roomgrades.append(roundsgrades)

    return render(
        request,
        '%s/physics_fight_detail.html' % params.instance_name,
        {
            'params': params,
            'roomgrades': roomgrades,
            'ignore_rooms': int(pfid) > params.npf,
            'fight_name': params.fights['names'][int(pfid) - 1],
            'sister_tournament_postfix': 'physics_fights',
            'no_round_played': rounds.count() == 0,
        },
    )


def create_summary(roomrounds, teams_involved=None, finished=None):
    # print "finished =", finished
    # print "Teams:", teams_involved

    if teams_involved == None:
        teams_involved = get_involved_teams_dict(roomrounds)

    if finished == None:
        finished = roomrounds.count() == len(teams_involved)

    try:
        summary_grades = {
            team: [team.presentation_coefficients()[int(roomrounds[0].pf_number) - 1]]
            for team in teams_involved
        }
        for team in teams_involved:
            for r in roomrounds:
                summary_grades[team].append(
                    # TODO: looks like this is not the fastest way!
                    team.get_scores_for_rounds(
                        rounds=roomrounds.filter(round_number=r.round_number),
                        include_bonus=False,
                    )[0]
                )
            summary_grades[team].append(sum(summary_grades[team][1:]))

        summary_grades = sorted(
            summary_grades.items(), key=lambda x: x[1][-1], reverse=True
        )

        if finished and params.display_pf_summary_bonus_points:
            for team_summary in summary_grades:
                reporter_round = roomrounds.filter(reporter_team=team_summary[0])[0]
                team_summary[1].append(reporter_round.bonus_points_reporter)

        return summary_grades

    except:
        return None


def rank_ordinal(value):
    try:
        value = int(value)
    except ValueError:
        return value
    lang = get_language()
    if lang in ('ru', 'ruttn'):
        return "%dй" % (value)
    else:
        t = ('th', 'st', 'nd', 'rd') + ('th',) * 6
        if value % 100 in (11, 12, 13):
            return u"%d%s" % (value, t[0])
        return u'%d%s' % (value, t[value % 10])


def create_ranking(teams):
    rankteams = []

    if len(teams) > 0:

        for ind, team in enumerate(teams):
            nrounds_as_rep = team.nrounds_as_rep
            nrounds_as_opp = team.nrounds_as_opp
            nrounds_as_rev = team.nrounds_as_rev
            pfsplayed = min(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev)
            team.pfsplayed = pfsplayed
            team.ongoingpf = False
            if max(nrounds_as_rep, nrounds_as_opp, nrounds_as_rev) > pfsplayed:
                team.ongoingpf = True
                team.currentpf = pfsplayed + 1
            team.rank = rank_ordinal(ind + 1)
            rankteams.append(team)

    return rankteams


def create_final_ranking():
    teams = Team.objects.filter(is_in_final=True).order_by('-final_points')
    if teams.count() == 0:
        return None

    return create_ranking(teams)


def create_semi_ranking():
    teams = Team.objects.filter(is_in_semi=True).order_by('-semi_points')
    if teams.count() == 0:
        return None

    return create_ranking(teams)


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def ranking(request):
    rankteams = create_ranking(Team.objects.order_by('-total_points'))
    if rankteams:
        rankteams[0].emphase = True

    semirankteams = create_semi_ranking()

    if SiteConfiguration.get_solo().display_final_ranking_on_ranking_page:
        finalrankteams = create_final_ranking()
    else:
        finalrankteams = None

    return render(
        request,
        '%s/ranking.html' % params.instance_name,
        {
            'params': params,
            'final_fight_number': final_fight_number,
            'finalrankteams': finalrankteams,
            'rankteams': rankteams,
            'semirankteams': semirankteams,
            'sister_tournament_postfix': 'ranking',
        },
    )


@user_passes_test(
    ninja_test, redirect_field_name=None, login_url='/%s/soon' % params.instance_name
)
@cache_page(cache_duration)
def poolranking(request):
    # Pool A
    rankteamsA = create_ranking(Team.objects.filter(pool="A").order_by('-total_points'))

    # Pool B
    rankteamsB = create_ranking(Team.objects.filter(pool="B").order_by('-total_points'))

    semirankteams = create_semi_ranking()

    if SiteConfiguration.get_solo().display_final_ranking_on_ranking_page:
        finalrankteams = create_final_ranking()
    else:
        finalrankteams = None

    return render(
        request,
        '%s/poolranking.html' % params.instance_name,
        {
            'params': params,
            'final_fight_number': final_fight_number,
            'finalrankteams': finalrankteams,
            'rankteamsA': rankteamsA,
            'rankteamsB': rankteamsB,
            'sister_tournament_postfix': 'ranking',
            'semirankteams': semirankteams,
        },
    )


def make_dict_from_csv_row(row):
    # This is just a map to control numbers of columns which are imported
    # No logic should be placed here!
    return {
        'name': row[1],
        'surname': row[3],
        'affiliation': row[4],
        'team': row[9],
        'role': row[10],
        'is_jury': row[11],
        'email': row[19],
    }


def make_row_importable(row):
    # All the logic needed to parse the row
    # Some edition-specific things are hardcoded here

    if row['team'] == 'Organisational Registration (IOC, ExeCom, invited guest, etc.)':
        # No team reference needed
        row['team'] = None
    else:
        # This also holds automated creation of teams
        row['team'], created = Team.objects.get_or_create(name=row['team'])

    row['is_jury'] = row['is_jury'] != '0'

    if row['role'] == 'Team captain':
        row['role'] = 'TC'
    elif row['role'] == 'Team member':
        row['role'] = 'TM'
    else:
        row['role'] = None


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
@cache_page(cache_duration)
def upload_csv(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csvfile']
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                row = make_dict_from_csv_row(row)
                make_row_importable(row)
                print(row)

                # If a person is not a jury member and has a role,
                # import him/her as a participant
                if not row['is_jury'] and row['role']:
                    Participant.objects.get_or_create(
                        name=row['name'],
                        surname=row['surname'],
                        affiliation=row['affiliation'],
                        role=row['role'],
                        team=row['team'],
                    )
                elif row['is_jury']:
                    Jury.objects.get_or_create(
                        name=row['name'],
                        surname=row['surname'],
                        affiliation=row['affiliation'],
                        team=row['team'],
                    )
    else:
        form = UploadForm()

    return render(
        request,
        '%s/upload_csv.html' % params.instance_name,
        {
            'form': form,
            'params': params,
        },
    )


@user_passes_test(lambda u: u.is_staff, login_url='/admin')
def upload_problems(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csvfile']
            reader = csv.reader(csvfile)
            # Uncomment to skip header
            # next(reader)
            for row in reader:
                name = row[0]
                text = row[1] if len(row) > 1 else ''
                auth = row[2] if len(row) > 2 else ''
                Problem.objects.get_or_create(
                    name=name,
                    description=text,
                    author=auth,
                )

    else:
        form = UploadForm()

    return render(
        request,
        '%s/upload_problems.html' % params.instance_name,
        {
            'form': form,
            'params': params,
        },
    )

# coding: utf8
from django.conf.urls import url

import parameters
from forms import member_for_team
from tactics import *

app_name = parameters.instance_name

urlpatterns = [
    url(r"^$", tournament_overview),
    url(r"^tournament$", tournament_overview, name="tournament_overview"),
    url(r"^participants$", participants_overview, name="participants_overview"),
    url(
        r"^participants/(?P<pk>[0-9]+)/$", participant_detail, name="participant_detail"
    ),
    url(r"^jurys$", jurys_overview, name="jurys_overview"),
    url(r"^member_for_team$", member_for_team),
    url(r"^jurys/(?P<pk>[0-9]+)/$", jury_detail, name="jury_detail"),
    url(r"^problems$", problems_overview, name="problems_overview"),
    url(r"^problems/(?P<pk>[0-9]+)/$", problem_detail, name="problem_detail"),
    url(r"^rounds$", rounds, name="rounds"),
    url(r"^rounds/(?P<pk>[0-9]+)/$", round_detail, name="round_detail"),
    url(r"^round_add_next/(?P<pk>[0-9]+)/$", round_add_next, name="round_add_next"),
    url(r"^teams$", teams_overview, name="teams"),
    url(
        r"^teams/(?P<team_name>[A-Za-z0-9\w|\W\- ]+)/$", team_detail, name="team_detail"
    ),
    url(r"^physics_fights$", rounds, name="rounds"),
    url(r"^physics_fights/$", rounds, name="rounds"),
    url(
        r"^physics_fights/(?P<pfid>[0-9]+)/$",
        physics_fight_detail,
        name="physics_fight_detail",
    ),
    url(r"^ranking$", ranking, name="ranking"),
    url(r"^build_tactics$", build_tactics),
    url(r"^poolranking$", poolranking, name="poolranking"),
    url(r"^export_csv_ranking_timeline$", export_csv_ranking_timeline),
    url(r"^participants_export$", participants_export),
    url(r"^participants_export_web$", participants_export_web),
    url(r"^participants_all$", participants_all),
    url(r"^jury_export$", jury_export),
    url(r"^jury_export_csv$", jury_export_csv),
    url(r"^jury_export_web$", jury_export_web),
    url(r"^trombinoscope$", participants_trombinoscope),
    url(r"^soon", soon),
    url(r"^update_all", update_all, name="update_all"),
    url(r"^verify_all", verify_all, name="verify_all"),
    url(r"^upload_csv", upload_csv, name="upload_csv"),
    url(r"^upload_problems", upload_problems, name="upload_problems"),
]

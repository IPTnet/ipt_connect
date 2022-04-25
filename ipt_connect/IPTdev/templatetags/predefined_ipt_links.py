from django import template

from ..models import *

register = template.Library()

"""
This file provides a convenient way to put links to the models
into templates.
E.g. instead of:
	<a href="{% url params.instance_name|add:':team_detail' team_name=juryroundsgrade.round.reporter_team.name %}">{{juryroundsgrade.round.reporter_team.name}}</a>
you can now write just:
	{% team_link juryroundsgrade.round.reporter_team %}
(don't forget to `{% load predefined_ipt_links %}` in the beginning of the template!)

Please put all the models in the alphabetical order (be git-friendly!)

The refactoring is not finished yet :(
"""


@register.inclusion_tag(
    params.instance_name + "/includes/supplementary_material_link.html",
    takes_context=True,
)
def supplementary_material_link(context, supplementary_material):
    return {
        "name": supplementary_material.name,
        "link": supplementary_material.link,
        "params": context["params"],
    }


@register.inclusion_tag(
    params.instance_name + "/includes/team_link.html", takes_context=True
)
def team_link(context, team):
    if isinstance(team, Team):
        team = team.name
    return {
        "team_name": team,
        "params": context["params"],
    }

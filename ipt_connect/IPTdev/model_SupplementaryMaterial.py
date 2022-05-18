# coding: utf8

from django.db import models

import models as ipt_connect_models


class SupplementaryMaterial(models.Model):
    team = models.ForeignKey(ipt_connect_models.Team, null=True)
    problem = models.ForeignKey(ipt_connect_models.Problem)
    name = models.CharField(max_length=500)
    link = models.CharField(max_length=5000)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicsfight',
            name='name_opponent',
        ),
        migrations.RemoveField(
            model_name='physicsfight',
            name='name_reporter',
        ),
        migrations.RemoveField(
            model_name='physicsfight',
            name='name_reviewer',
        ),
        migrations.AddField(
            model_name='jury',
            name='team',
            field=models.ForeignKey(blank=True, to='IPT2016.Team', null=True),
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='reporter_2',
            field=models.ForeignKey(related_name='reporter_team_2', blank=True, to='IPT2016.Participant', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='description',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='team',
            name='surname',
            field=models.CharField(default=None, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='physicsfight',
            name='opponent',
            field=models.ForeignKey(related_name='opponent_team', to='IPT2016.Participant'),
        ),
        migrations.AlterField(
            model_name='physicsfight',
            name='reporter',
            field=models.ForeignKey(related_name='reporter_team_1', to='IPT2016.Participant'),
        ),
        migrations.AlterField(
            model_name='physicsfight',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewer_team', to='IPT2016.Participant'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]

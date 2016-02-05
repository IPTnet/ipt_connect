# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EternalRejection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Jury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JuryGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade_reporter', models.IntegerField(default=None, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('grade_opponent', models.IntegerField(default=None, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('grade_reviewer', models.IntegerField(default=None, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('jury', models.ForeignKey(to='IPT2016.Jury')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Richard', max_length=50)),
                ('surname', models.CharField(default=b'Feynman', max_length=50)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('email', models.EmailField(help_text=b'This address will be used to send you every important infos about the tournament.', max_length=254)),
                ('birthdate', models.DateField(default=b'1900-01-31')),
                ('photo', models.ImageField(help_text=b'Used for badges and transportation cards.', upload_to=b'id_photo')),
                ('role', models.CharField(max_length=20, choices=[(b'TM', b'Team Member'), (b'TC', b'Team Captain'), (b'IOC', b'IOC'), (b'ACC', b'Accompanying')])),
                ('passport_number', models.CharField(max_length=20)),
                ('affiliation', models.CharField(default=b'XXX University', max_length=20)),
                ('veteran', models.BooleanField(default=False, help_text=b'Have you already participated in the IPT?')),
                ('diet', models.CharField(help_text=b'Do you have a specific diet?', max_length=20, choices=[(b'NO', b'No specific diet'), (b'NOPORK', b'No pork'), (b'NOMEAT', b'No meat'), (b'NOFISH', b'No fish'), (b'NOMEAT_NOEGG', b'No meat, No eggs')])),
                ('tourism', models.CharField(help_text=b'Would you like to stay some more days in Paris after the tournament? Please note the LOC would only book the rooms, not pay for it!', max_length=20, choices=[(b'TOURISM_0', b'No'), (b'TOURISM_1', b'Yes, one night'), (b'TOURISM_2', b'Yes, two nights')])),
                ('shirt_size', models.CharField(max_length=1, choices=[(b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large')])),
                ('remark', models.TextField(blank=True)),
                ('hotel_room', models.CharField(max_length=20, blank=True)),
                ('check_in', models.BooleanField(default=False, help_text=b'Has the participant arrived?')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicsFight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField(default=None, choices=[(1, b'Round 1'), (2, b'Round 2'), (3, b'Round 3'), (4, b'Round 4')])),
                ('fight_number', models.IntegerField(default=None, choices=[(1, b'Fight 1'), (2, b'Fight 2'), (3, b'Fight 3')])),
                ('name_reporter', models.CharField(default=None, max_length=100, choices=[(b'Dom Domkek', b'Dom Domkek'), (b'Henri Riant', b'Henri Riant'), (b'Jean Valjean', b'Jean Valjean'), (b'Jonas Jonasson', b'Jonas Jonasson'), (b'Negus Negusson', b'Negus Negusson'), (b'Olaf Olafsson', b'Olaf Olafsson'), (b'Pierre Rocque', b'Pierre Rocque'), (b'Piotr Piotrek', b'Piotr Piotrek'), (b'Vlad Vladek', b'Vlad Vladek')])),
                ('name_opponent', models.CharField(default=None, max_length=100, choices=[(b'Dom Domkek', b'Dom Domkek'), (b'Henri Riant', b'Henri Riant'), (b'Jean Valjean', b'Jean Valjean'), (b'Jonas Jonasson', b'Jonas Jonasson'), (b'Negus Negusson', b'Negus Negusson'), (b'Olaf Olafsson', b'Olaf Olafsson'), (b'Pierre Rocque', b'Pierre Rocque'), (b'Piotr Piotrek', b'Piotr Piotrek'), (b'Vlad Vladek', b'Vlad Vladek')])),
                ('name_reviewer', models.CharField(default=None, max_length=100, choices=[(b'Dom Domkek', b'Dom Domkek'), (b'Henri Riant', b'Henri Riant'), (b'Jean Valjean', b'Jean Valjean'), (b'Jonas Jonasson', b'Jonas Jonasson'), (b'Negus Negusson', b'Negus Negusson'), (b'Olaf Olafsson', b'Olaf Olafsson'), (b'Pierre Rocque', b'Pierre Rocque'), (b'Piotr Piotrek', b'Piotr Piotrek'), (b'Vlad Vladek', b'Vlad Vladek')])),
                ('submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TacticalRejection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('physics_fight', models.ForeignKey(to='IPT2016.PhysicsFight')),
                ('problem', models.ForeignKey(to='IPT2016.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('IOC', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='opponent',
            field=models.ForeignKey(related_name='opponent_team', to='IPT2016.Team'),
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='problem_presented',
            field=models.ForeignKey(to='IPT2016.Problem'),
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='reporter',
            field=models.ForeignKey(related_name='reporter_team', to='IPT2016.Team'),
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewer_team', to='IPT2016.Team'),
        ),
        migrations.AddField(
            model_name='physicsfight',
            name='room',
            field=models.ForeignKey(to='IPT2016.Room'),
        ),
        migrations.AddField(
            model_name='participant',
            name='team',
            field=models.ForeignKey(to='IPT2016.Team'),
        ),
        migrations.AddField(
            model_name='jurygrade',
            name='physics_fight',
            field=models.ForeignKey(to='IPT2016.PhysicsFight'),
        ),
        migrations.AddField(
            model_name='eternalrejection',
            name='physics_fight',
            field=models.ForeignKey(to='IPT2016.PhysicsFight'),
        ),
        migrations.AddField(
            model_name='eternalrejection',
            name='problem',
            field=models.ForeignKey(to='IPT2016.Problem'),
        ),
    ]

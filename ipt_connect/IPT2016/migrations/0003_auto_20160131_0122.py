# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0002_auto_20160130_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='affiliation',
            field=models.CharField(default=b'XXX University', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='birthdate',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='diet',
            field=models.CharField(help_text=b'Do you have a specific diet?', max_length=20, choices=[(b'NO', b'No specific diet'), (b'NOPORK', b'No pork'), (b'NOMEAT', b'No meat'), (b'NOFISH', b'No fish'), (b'NOMEAT_NOEGG', b'No meat, No eggs')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(help_text=b'This address will be used to send you every important infos about the tournament.', max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='photo',
            field=models.ImageField(help_text=b'Used for badges and transportation cards.', upload_to=b'id_photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='tourism',
            field=models.CharField(help_text=b'Would you like to stay some more days in Paris after the tournament? Please note the LOC would only book the rooms, not paying it!', max_length=20, choices=[(b'TOURISM_0', b'No'), (b'TOURISM_1', b'Yes, one night'), (b'TOURISM_2', b'Yes, two nights')]),
            preserve_default=True,
        ),
    ]

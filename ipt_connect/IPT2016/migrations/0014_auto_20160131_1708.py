# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0013_auto_20160131_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tacticalrejection',
            name='tactical_rejection',
            field=models.IntegerField(default=None, choices=[(1, b'1 - Popsicle Stick Cobra'), (2, b'2 - The Torque'), (3, b'3 - Cooling Jug'), (4, b'4 - Ferromagnetic Sea'), (5, b'5 - Cracks On The Glass'), (6, b'6 - The Silencer'), (7, b'7 - Greenhouse Effect'), (8, b'8 - Drop Jumping Jack'), (9, b'9 - Sultry Day'), (10, b'10 - Water Bomb'), (11, b'11 - True Quantum Randomizer'), (12, b'12 - Half Empty Bottle'), (13, b'13 - Cross Talking Metronomes'), (14, b'14 - Sticky Balloon'), (15, b'15 - Electric Fountain'), (16, b'16 - Magnetic Cannon'), (17, b'17 - Looking For The Signs Of Civilization')]),
            preserve_default=True,
        ),
    ]

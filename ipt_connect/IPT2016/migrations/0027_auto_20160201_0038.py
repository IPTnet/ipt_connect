# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0026_auto_20160131_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jurygrade',
            name='jury',
            field=models.ForeignKey(to='IPT2016.Jury'),
            preserve_default=True,
        ),
    ]

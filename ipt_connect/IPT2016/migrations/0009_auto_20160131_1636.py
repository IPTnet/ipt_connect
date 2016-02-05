# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0008_auto_20160131_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='birthdate',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]

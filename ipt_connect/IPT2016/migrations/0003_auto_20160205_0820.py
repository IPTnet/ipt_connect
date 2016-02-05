# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0002_auto_20160204_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='photo',
            field=models.ImageField(help_text=b'Used for badges and transportation cards.', null=True, upload_to=b'id_photo', blank=True),
        ),
    ]

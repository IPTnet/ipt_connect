# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0014_auto_20160131_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='physicsfight',
            old_name='room_number',
            new_name='room',
        ),
    ]

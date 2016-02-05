# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0017_auto_20160131_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eternalrejection',
            old_name='eternal_rejection',
            new_name='problem',
        ),
        migrations.RenameField(
            model_name='tacticalrejection',
            old_name='tactical_rejection',
            new_name='problem',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='photo',
            field=models.ImageField(help_text=b'Used for badges and transportation cards.', upload_to=b'kim/id_photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participant',
            name='shirt_size',
            field=models.CharField(max_length=1, choices=[(b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large')]),
            preserve_default=True,
        ),
    ]

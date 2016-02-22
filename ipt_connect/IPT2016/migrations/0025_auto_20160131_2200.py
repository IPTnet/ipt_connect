# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0024_auto_20160131_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='jurygrade',
            name='name',
            field=models.ForeignKey(to='IPT2016.Jury'),
            preserve_default=True,
        ),
    ]

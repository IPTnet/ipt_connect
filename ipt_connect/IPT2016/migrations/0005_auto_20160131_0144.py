# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IPT2016', '0004_auto_20160131_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='participant',
            name='photo',
            field=models.ImageField(help_text=b'Used for badges and transportation cards.', upload_to=b'id_photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='physicsfight',
            name='problem_presented',
            field=models.ForeignKey(to='IPT2016.Problem'),
            preserve_default=True,
        ),
    ]

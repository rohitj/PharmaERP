# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pp', '__first__'),
        ('es', '__first__'),
        ('sd', '__first__'),
        ('fi', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mtype',
            fields=[
                ('mtype', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=20, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Packing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('packname', models.CharField(max_length=30)),
                ('tab_tp', models.CharField(max_length=1, null=True)),
                ('unitppack', models.IntegerField(blank=True, null=True)),
                ('qty_per_ca', models.IntegerField(blank=True, null=True)),
                ('box', models.IntegerField(blank=True, null=True)),
                ('ptype', models.IntegerField(blank=True, null=True)),
                ('cfactor', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)),
                ('rate_cs', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)),
                ('rate_bsd', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)),
                ('rate_bsg', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)),
                ('inv_1', models.IntegerField(blank=True, null=True)),
                ('inv_2', models.IntegerField(blank=True, null=True)),
                ('btype', models.IntegerField(blank=True, null=True)),
                ('dlfixed', models.CharField(blank=True, max_length=10, null=True)),
                ('series', models.IntegerField(blank=True, null=True)),
                ('sale_or_sample', models.CharField(max_length=1, default='D', choices=[('1', 'Sale'), ('2', 'Sample')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pbatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('batchname', models.CharField(max_length=20)),
                ('expiery', models.DateField(verbose_name='expiery date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pgroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('groupname', models.CharField(max_length=60)),
                ('bs_cat', models.CharField(blank=True, max_length=10, null=True)),
                ('isactive', models.BooleanField(default=True)),
                ('rmarea_id', models.ForeignKey(to='es.Rmarea')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Psr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fullcases', models.IntegerField(blank=True, null=True)),
                ('looseqty', models.IntegerField(blank=True, null=True)),
                ('quantity', models.DecimalField(max_digits=10, decimal_places=0)),
                ('pack_id', models.ForeignKey(to='mm.Packing')),
                ('pbatch_id', models.ForeignKey(to='mm.Pbatch')),
                ('vno_id', models.ForeignKey(blank=True, to='sd.Vno', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Psup',
            fields=[
                ('code', models.OneToOneField(to='fi.Code', serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('ref', models.CharField(max_length=2, choices=[('JV', 'Challan'), ('PI', 'Purchase Bill')])),
                ('date', models.DateField(null=True)),
                ('billno', models.CharField(blank=True, max_length=20, null=True)),
                ('billdate', models.DateField(blank=True, null=True)),
                ('aform', models.CharField(blank=True, max_length=10, null=True)),
                ('aformno', models.CharField(blank=True, max_length=20, null=True)),
                ('amount', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('saletax', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('excise', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('exciseinv', models.IntegerField(blank=True, null=True)),
                ('others', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('ismodvat', models.BooleanField()),
                ('thno', models.CharField(max_length=10, null=True)),
                ('typesup', models.CharField(max_length=10, null=True)),
                ('typedoc', models.CharField(max_length=10, null=True)),
                ('discount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('freight', models.DecimalField(max_digits=12, decimal_places=2)),
                ('challanno', models.DecimalField(max_digits=12, decimal_places=2)),
                ('paydays', models.IntegerField()),
                ('misc', models.IntegerField()),
                ('modvatcat', models.IntegerField()),
                ('ino', models.IntegerField(unique_for_year='date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rbatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pur_id', models.IntegerField(blank=True, null=True)),
                ('batchno', models.CharField(blank=True, max_length=20, null=True)),
                ('trno', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.DecimalField(max_digits=12, decimal_places=2)),
                ('rate', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('rate_cost', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('modvatcat', models.IntegerField(blank=True, null=True)),
                ('excise', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('cess', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('aform', models.CharField(blank=True, max_length=10, null=True)),
                ('thno', models.CharField(blank=True, max_length=10, null=True)),
                ('typesup', models.CharField(blank=True, max_length=10, null=True)),
                ('typedoc', models.CharField(blank=True, max_length=10, null=True)),
                ('ismodvat', models.BooleanField()),
                ('purity', models.DecimalField(max_digits=12, default=1, decimal_places=2)),
                ('ispass', models.BooleanField()),
                ('mfrr', models.CharField(blank=True, max_length=40, null=True)),
                ('mfgdate', models.DateField(blank=True, null=True)),
                ('lst', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('cst', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('expiery', models.DateField(blank=True, null=True)),
                ('mtype_id', models.ForeignKey(to='mm.Mtype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rname', models.CharField(max_length=60)),
                ('unit', models.CharField(max_length=2, choices=[('GM', 'Grams'), ('KG', 'Kilograms'), ('LT', 'Litres'), ('NO', 'Numbers')])),
                ('rcd', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(verbose_name='receipt date')),
                ('psup_id', models.ForeignKey(to='mm.Psup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rgroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('groupname', models.CharField(max_length=60)),
                ('dept', models.CharField(max_length=2, choices=[('RM', 'Raw Material'), ('PM', 'Packing Material')])),
                ('family', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rsr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('tab_tp', models.CharField(blank=True, max_length=1, null=True)),
                ('date', models.DateField(default=datetime.date(2015, 3, 28))),
                ('quantity', models.DecimalField(max_digits=12, decimal_places=4)),
                ('areato', models.ForeignKey(blank=True, to='es.Rmarea', null=True)),
                ('fstype_id', models.ForeignKey(blank=True, to='pp.Fstype', null=True)),
                ('mtype_id', models.ForeignKey(to='mm.Mtype')),
                ('rbatch_id', models.ForeignKey(to='mm.Rbatch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sup',
            fields=[
                ('code', models.OneToOneField(to='fi.Code', serialize=False, primary_key=True)),
                ('stno', models.CharField(verbose_name='Sale Tax No', blank=True, max_length=30, null=True)),
                ('eccno', models.CharField(blank=True, max_length=20, null=True)),
                ('identity', models.CharField(blank=True, max_length=10, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('test', models.CharField(max_length=100)),
                ('packing_id', models.ForeignKey(blank=True, to='mm.Packing', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('factor', models.DecimalField(max_digits=10, decimal_places=4)),
                ('quantity_id', models.ForeignKey(to='mm.Quantity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='uc',
            name='u1',
            field=models.ForeignKey(to='mm.Unit', related_name='fromunit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uc',
            name='u2',
            field=models.ForeignKey(to='mm.Unit', related_name='tounit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rcode',
            name='rgroup_id',
            field=models.ForeignKey(to='mm.Rgroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rcode',
            name='rmarea_id',
            field=models.ForeignKey(blank=True, to='es.Rmarea', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rbatch',
            name='rcode_id',
            field=models.ForeignKey(to='mm.Rcode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quantity',
            name='unit',
            field=models.ForeignKey(to='mm.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pur',
            name='sup_id',
            field=models.ForeignKey(to='mm.Sup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pbatch',
            name='recno_id',
            field=models.ForeignKey(to='mm.Recno'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='packing',
            name='pgroup_id',
            field=models.ForeignKey(to='mm.Pgroup'),
            preserve_default=True,
        ),
    ]

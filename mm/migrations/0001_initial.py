# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('fi', '__first__'),
        ('pp', '__first__'),
        ('es', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mtype',
            fields=[
                ('mtype', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('description', models.CharField(null=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Packing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('packname', models.CharField(max_length=30)),
                ('tab_tp', models.CharField(null=True, max_length=1)),
                ('unitppack', models.IntegerField(blank=True, null=True)),
                ('qty_per_ca', models.IntegerField(blank=True, null=True)),
                ('box', models.IntegerField(blank=True, null=True)),
                ('ptype', models.IntegerField(blank=True, null=True)),
                ('cfactor', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)),
                ('rate_cs', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)),
                ('rate_bsd', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)),
                ('rate_bsg', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)),
                ('inv_1', models.IntegerField(blank=True, null=True)),
                ('inv_2', models.IntegerField(blank=True, null=True)),
                ('btype', models.IntegerField(blank=True, null=True)),
                ('dlfixed', models.CharField(blank=True, null=True, max_length=10)),
                ('series', models.IntegerField(blank=True, null=True)),
                ('sale_or_sample', models.CharField(default='D', choices=[('1', 'Sale'), ('2', 'Sample')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pbatch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('groupname', models.CharField(max_length=60)),
                ('bs_cat', models.CharField(blank=True, null=True, max_length=10)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('vno_id', models.IntegerField()),
                ('fullcases', models.IntegerField(blank=True, null=True)),
                ('looseqty', models.IntegerField(blank=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=10)),
                ('pack_id', models.ForeignKey(to='mm.Packing')),
                ('pbatch_id', models.ForeignKey(to='mm.Pbatch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Psup',
            fields=[
                ('code', models.OneToOneField(serialize=False, primary_key=True, to='fi.Code')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pur',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ref', models.CharField(choices=[('JV', 'Challan'), ('PI', 'Purchase Bill')], max_length=2)),
                ('date', models.DateField(null=True)),
                ('billno', models.CharField(blank=True, null=True, max_length=20)),
                ('billdate', models.DateField(blank=True, null=True)),
                ('aform', models.CharField(blank=True, null=True, max_length=10)),
                ('aformno', models.CharField(blank=True, null=True, max_length=20)),
                ('amount', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('saletax', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('excise', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('exciseinv', models.IntegerField(blank=True, null=True)),
                ('others', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('ismodvat', models.BooleanField()),
                ('thno', models.CharField(null=True, max_length=10)),
                ('typesup', models.CharField(null=True, max_length=10)),
                ('typedoc', models.CharField(null=True, max_length=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('freight', models.DecimalField(decimal_places=2, max_digits=12)),
                ('challanno', models.DecimalField(decimal_places=2, max_digits=12)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rbatch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('pur_id', models.IntegerField(blank=True, null=True)),
                ('batchno', models.CharField(blank=True, null=True, max_length=20)),
                ('trno', models.CharField(blank=True, null=True, max_length=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('rate_cost', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('modvatcat', models.IntegerField(blank=True, null=True)),
                ('excise', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('cess', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('aform', models.CharField(blank=True, null=True, max_length=10)),
                ('thno', models.CharField(blank=True, null=True, max_length=10)),
                ('typesup', models.CharField(blank=True, null=True, max_length=10)),
                ('typedoc', models.CharField(blank=True, null=True, max_length=10)),
                ('ismodvat', models.BooleanField()),
                ('purity', models.DecimalField(default=1, decimal_places=2, max_digits=12)),
                ('ispass', models.BooleanField()),
                ('mfrr', models.CharField(blank=True, null=True, max_length=40)),
                ('mfgdate', models.DateField(blank=True, null=True)),
                ('lst', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
                ('cst', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rname', models.CharField(max_length=60)),
                ('unit', models.CharField(choices=[('GM', 'Grams'), ('KG', 'Kilograms'), ('LT', 'Litres'), ('NO', 'Numbers')], max_length=2)),
                ('rcd', models.CharField(blank=True, null=True, max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recno',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('groupname', models.CharField(max_length=60)),
                ('dept', models.CharField(choices=[('RM', 'Raw Material'), ('PM', 'Packing Material')], max_length=2)),
                ('family', models.CharField(blank=True, null=True, max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rsr',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tab_tp', models.CharField(blank=True, null=True, max_length=1)),
                ('date', models.DateField(default=datetime.date(2015, 3, 29))),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=12)),
                ('areato', models.ForeignKey(null=True, blank=True, to='es.Rmarea')),
                ('fstype_id', models.ForeignKey(null=True, blank=True, to='pp.Fstype')),
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
                ('code', models.OneToOneField(serialize=False, primary_key=True, to='fi.Code')),
                ('stno', models.CharField(verbose_name='Sale Tax No', blank=True, null=True, max_length=30)),
                ('eccno', models.CharField(blank=True, null=True, max_length=20)),
                ('identity', models.CharField(blank=True, null=True, max_length=10)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('test', models.CharField(max_length=100)),
                ('packing_id', models.ForeignKey(null=True, blank=True, to='mm.Packing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uc',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('factor', models.DecimalField(decimal_places=4, max_digits=10)),
                ('quantity_id', models.ForeignKey(to='mm.Quantity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='uc',
            name='u1',
            field=models.ForeignKey(related_name='fromunit', to='mm.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uc',
            name='u2',
            field=models.ForeignKey(related_name='tounit', to='mm.Unit'),
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
            field=models.ForeignKey(null=True, blank=True, to='es.Rmarea'),
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

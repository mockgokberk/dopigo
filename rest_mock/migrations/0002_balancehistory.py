# Generated by Django 3.0.3 on 2020-12-26 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_mock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeslot', models.DateTimeField()),
                ('value', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rest_mock.Account')),
            ],
        ),
    ]
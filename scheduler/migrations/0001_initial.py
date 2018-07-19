# Generated by Django 2.1rc1 on 2018-07-19 06:55

from django.db import migrations, models
import scheduler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('telephone', models.IntegerField()),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('repair_date', models.DateField()),
                ('repair_time', models.CharField(choices=[('T1', '08:00-11:00'), ('T2', '10:00-13:00'), ('T3', '12:00-15:00'), ('T4', '14:00-17:00'), ('T5', '16:00-19:00'), ('T6', '18:00-21:00')], default=scheduler.models.Scheduler.TimeChoice('08:00-11:00'), max_length=2)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sched_un_id', models.CharField(db_index=True, max_length=10, unique=True)),
            ],
        ),
    ]
# Generated by Django 2.2.4 on 2019-08-23 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clndr', '0038_auto_20190823_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift_day',
            name='calendar',
        ),
    ]

# Generated by Django 2.2.4 on 2019-08-21 20:16

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('clndr', '0020_remove_shift_day_props'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift_day',
            name='daytype',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='clndr.Day_types'),
        ),
    ]

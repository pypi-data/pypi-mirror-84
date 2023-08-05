# Generated by Django 2.2 on 2019-04-14 08:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('isc_common', '0018_auto_20190414_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AddField(
            model_name='history',
            name='deliting',
            field=models.BooleanField(default=True, verbose_name='Возможность удаления'),
        ),
        migrations.AddField(
            model_name='history',
            name='editing',
            field=models.BooleanField(default=True, verbose_name='Возможность редактирования'),
        ),
        migrations.AddField(
            model_name='history',
            name='id_old',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Идентификатор старый'),
        ),
        migrations.AddField(
            model_name='history',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AddField(
            model_name='params',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AddField(
            model_name='params',
            name='deliting',
            field=models.BooleanField(default=True, verbose_name='Возможность удаления'),
        ),
        migrations.AddField(
            model_name='params',
            name='editing',
            field=models.BooleanField(default=True, verbose_name='Возможность редактирования'),
        ),
        migrations.AddField(
            model_name='params',
            name='id_old',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Идентификатор старый'),
        ),
        migrations.AddField(
            model_name='params',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='history',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='params',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор'),
        ),
    ]

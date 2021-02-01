# Generated by Django 3.1.4 on 2020-12-07 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20201207_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environmentalconsequence',
            name='platform_type',
            field=models.ForeignKey(blank=True, default=11, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.platformtype', verbose_name='[ILOF-64] platform type'),
        ),
        migrations.AlterField(
            model_name='lastinspection',
            name='last_underwater_inspection_date',
            field=models.DateField(blank=True, null=True, verbose_name='[ILOF-11] last underwater inspection date'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='platform_manned_status',
            field=models.ForeignKey(blank=True, default=7, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.platformmannedstatus', verbose_name='[ILOF-63] platform manned status'),
        ),
    ]
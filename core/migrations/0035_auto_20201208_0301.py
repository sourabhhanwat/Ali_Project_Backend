# Generated by Django 3.1.4 on 2020-12-08 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20201208_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='platform_manned_status',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.platformmannedstatus', verbose_name='[ILOF-63] platform manned status'),
        ),
    ]
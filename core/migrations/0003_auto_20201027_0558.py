# Generated by Django 3.1.1 on 2020-10-27 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201024_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='platform_manned_status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.DO_NOTHING, to='core.platformmannedstatus', verbose_name='[ILOF-63] platform manned status'),
        ),
    ]
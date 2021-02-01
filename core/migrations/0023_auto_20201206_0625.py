# Generated by Django 3.1.4 on 2020-12-06 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20201203_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environmentalconsequence',
            name='platform_type',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.platformtype', verbose_name='[ILOF-64] platform type'),
        ),
        migrations.CreateModel(
            name='ScopeOfSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('above_water_visual_method', models.CharField(blank=True, max_length=100, null=True)),
                ('above_water_visual_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('anodes_method', models.CharField(blank=True, max_length=100, null=True)),
                ('anodes_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('appurtenance_survey_method', models.CharField(blank=True, max_length=100, null=True)),
                ('appurtenance_survey_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('caissons_method', models.CharField(blank=True, max_length=100, null=True)),
                ('caissons_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('cathodic_method', models.CharField(blank=True, max_length=100, null=True)),
                ('cathodic_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('coating_method', models.CharField(blank=True, max_length=100, null=True)),
                ('coating_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('conductor_method', models.CharField(blank=True, max_length=100, null=True)),
                ('conductor_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('debris_method', models.CharField(blank=True, max_length=100, null=True)),
                ('debris_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('deck_elevation_method', models.CharField(blank=True, max_length=100, null=True)),
                ('deck_elevation_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('flooded_method', models.CharField(blank=True, max_length=100, null=True)),
                ('flooded_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('general_visual_method', models.CharField(blank=True, max_length=100, null=True)),
                ('general_visual_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('joint_ndt_method', models.CharField(blank=True, max_length=100, null=True)),
                ('joint_ndt_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('jtube_method', models.CharField(blank=True, max_length=100, null=True)),
                ('jtube_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('marine_growth_method', models.CharField(blank=True, max_length=100, null=True)),
                ('marine_growth_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('risers_method', models.CharField(blank=True, max_length=100, null=True)),
                ('risers_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('scour_depth_method', models.CharField(blank=True, max_length=100, null=True)),
                ('scour_depth_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('supplemental_method', models.CharField(blank=True, max_length=100, null=True)),
                ('supplemental_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('underwater_cp_method', models.CharField(blank=True, max_length=100, null=True)),
                ('underwater_cp_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('visual_method', models.CharField(blank=True, max_length=100, null=True)),
                ('visual_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('wallut_method', models.CharField(blank=True, max_length=100, null=True)),
                ('wallut_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('weld_method', models.CharField(blank=True, max_length=100, null=True)),
                ('weld_scope', models.CharField(blank=True, max_length=100, null=True)),
                ('platform', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scope_of_survey', to='core.platform')),
            ],
        ),
        migrations.CreateModel(
            name='OtherDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corrosion_survey', models.BooleanField(blank=True, null=True)),
                ('debris_clearance', models.BooleanField(blank=True, null=True)),
                ('manode_confirmation', models.BooleanField(blank=True, null=True)),
                ('marine_growth_cleaning', models.BooleanField(blank=True, null=True)),
                ('other', models.BooleanField(blank=True, null=True)),
                ('scour_repair', models.BooleanField(blank=True, null=True)),
                ('weld_monitoring', models.BooleanField(blank=True, null=True)),
                ('platform', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='other_detail', to='core.platform')),
            ],
        ),
    ]
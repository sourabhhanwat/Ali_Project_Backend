import datetime
import logging
from decimal import Decimal

import pytz
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Q, Subquery, OuterRef, CheckConstraint
from django.db.models.functions import Coalesce
from django.utils import timezone
from .project import Project

from . import NumberOfLegsType, BracingType, PlatformMannedStatus, PlatformType
from .ownership import PlatformOwnership, SiteOwnership, ProjectOwnership

DATE_1969 = datetime.datetime(year=1969, month=1, day=1, tzinfo=pytz.utc)

DATE_1979 = datetime.datetime(year=1979, month=1, day=1, tzinfo=pytz.utc)

logger = logging.getLogger("core.models.platform")

NUMBER_OF_LEGS_AND_BRACING_METRICS = (
    (10, 10, 8, 6, 4),
    (10, 7, 5, 4, 3),
    (6, 5, 4, 3, 2),
)


class LegPileGrouting(models.Model):
    pile_in_leg_installation = models.BooleanField(
        default=False, verbose_name="[ILOF-6] Pile in leg installation"
    )

    leg_to_pile_annulus_grouted = models.BooleanField(
        default=False, verbose_name="[ILOF-7] leg to pile annulus grouted"
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="leg_pile_grouting"
    )


class ShallowGas(models.Model):
    shallow_gas_effect_detected = models.BooleanField(
        default=False, verbose_name="[ILOF-8] shallow gas effect detected?"
    )

    shallow_gas_monitored = models.BooleanField(
        default=False, verbose_name="[ILOF-9] shallow gas monitored?"
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="shallow_gas"
    )


class LastInspection(models.Model):
    last_underwater_inspection_date = models.DateTimeField(
        null=True, blank=True, verbose_name="[ILOF-11] last underwater inspection date"
    )

    rbui_inspection_interval = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(limit_value=0)],
        verbose_name="[ILOF-14] rbui inspection interval (years)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="last_inspection"
    )


class MechanicalDamage(models.Model):
    number_of_damaged_members = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(limit_value=0)],
        verbose_name="[ILOF-16] number of damaged members in last inspection "
                     "(if not known n left empty, if no damaged members "
                     "found during inspection enter '0')",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="mechanical_damage"
    )


class Corrosion(models.Model):
    platform_design_life = models.IntegerField(
        default=1,
        validators=[MinValueValidator(limit_value=1)],
        verbose_name="[ILOF-17] platform design life (years)",
    )

    cp_design_life = models.IntegerField(
        null=True, blank=True, verbose_name="[ILOF-19] cp design Life"
    )

    original_anode_installation_date = models.DateTimeField(
        default=timezone.now, verbose_name="[ILOF-20] Original anode installation date"
    )

    anode_retrofit_date = models.DateTimeField(
        blank=True, null=True, verbose_name="[ILOF-22] anode retrofit date",
    )

    anode_survey_inspection_date = models.DateTimeField(
        blank=True, null=True, verbose_name="[ILOF-24] anode survey/inspection date",
    )

    average_anode_depletion_from_survey = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="[ILOF-25] average anode depletion from survey (%)",
    )

    average_anode_potential_from_survey = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="[ILOF-27] average anode potential from survey (mV)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="corrosion"
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=(
                              Q(anode_survey_inspection_date__isnull=True)
                              & Q(average_anode_depletion_from_survey__isnull=True)
                      )
                      | (
                              Q(anode_survey_inspection_date__isnull=False)
                              & Q(average_anode_depletion_from_survey__isnull=False)
                      ),
                name="anode_depletion_survey_performed",
            ),
        )


class MarineGrowthQuerySet(models.QuerySet):
    def has_ownership(self, user: settings.AUTH_USER_MODEL):
        if user.is_superuser:
            return self

        return self.filter(
            Q(platform__users=user)
            | Q(platform__project__users=user)
        ).distinct()


class MarineGrowth(models.Model):
    marine_growth_depths_from_el = models.DecimalField(
        max_digits=10, decimal_places=5, verbose_name="[ILOF-29] marine growth depths", null=True, blank=True
    )
    marine_growth_depths_to_el = models.DecimalField(
        max_digits=10, decimal_places=5, verbose_name="[ILOF-29] marine growth depths", null=True, blank=True
    )
    marine_growth_inspected_thickness = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        verbose_name="[ILOF-30] marine growth inspected thickness",
    )
    marine_growth_design_thickness = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        verbose_name="[ILOF-31] marine growth design thickness",
    )
    platform = models.ForeignKey(
        "Platform", on_delete=models.CASCADE, related_name="marine_growths"
    )

    objects = MarineGrowthQuerySet.as_manager()


class Scour(models.Model):
    design_scour_depth = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-32] design scour depth (m)",
    )

    measured_scour_depth_during_inspection = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="[ILOF-34] measured scoured depth during inspection (m)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="scour"
    )


class FloodedMember(models.Model):
    number_of_flooded_members_in_last_inspection = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="[ILOF-36] number of flooded members in last inspection",
    )

    flooded_members_last_inspection_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="[ILOF-37] flooded member last inspection date",
    )

    previous_flooded_members_inspection_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="[ILOF-38] previous flooded members inspection date",
    )

    number_of_previous_inspection_flooded_members = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="[ILOF-39] number of previous inspection flooded members",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="flooded_member"
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=(
                              Q(number_of_flooded_members_in_last_inspection__isnull=True)
                              & Q(flooded_members_last_inspection_date__isnull=True)
                              & Q(previous_flooded_members_inspection_date__isnull=True)
                              & Q(number_of_previous_inspection_flooded_members__isnull=True)
                      )
                      | (
                              Q(number_of_flooded_members_in_last_inspection__isnull=False)
                              & Q(flooded_members_last_inspection_date__isnull=False)
                              & Q(previous_flooded_members_inspection_date__isnull=False)
                              & Q(number_of_previous_inspection_flooded_members__isnull=False)
                      ),
                name="flooded_member_check",
            ),
        )


class UnprotectedAppurtenances(models.Model):
    number_of_unprotected_gas_riser = models.IntegerField(
        blank=True, null=True, verbose_name="[ILOF-41] number of unprotected gas riser"
    )

    number_of_unprotected_conductor = models.IntegerField(
        blank=True, null=True, verbose_name="[ILOF-43] number of unprotected conductor"
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="unprotected_appurtenances"
    )


class DeckLoad(models.Model):
    original_topsides_design_load_known = models.BooleanField(
        default=False, verbose_name="[ILOF-44] original topsides design load known"
    )

    increase_in_topsides_load = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="[ILOF-46] increase in topsides load (%)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="deck_load"
    )


class DeckElevationWaveInDeck(models.Model):
    cellar_deck_height = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-48] cellar deck height (m)",
    )

    maximum_wave_height_10_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-49] maximum wave height (m) - 10 years",
    )

    storm_surge_10_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-50] storm surge (m) - 10 years",
    )

    maximum_wave_height_100_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-49] maximum wave height (m) - 100 years",
    )

    storm_surge_100_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-50] storm surge (m) - 100 years",
    )

    maximum_wave_height_10000_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-49] maximum wave height (m) - 10,000 years",
    )

    storm_surge_10000_years = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-50] storm surge (m) - 10,000 years",
    )

    highest_astronomical_tide = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-51] highest astronomical height (m)",
    )

    crest_height_factor = models.IntegerField(
        null=True, blank=True, default=0, verbose_name="[ILOF-52] crest height factor"
    )

    platform = models.OneToOneField(
        "Platform",
        on_delete=models.CASCADE,
        related_name="deck_elevation_wave_in_deck",
    )

    # class Meta:
    #     constraints = (
    #         CheckConstraint(
    #             check=(
    #                           Q(cellar_deck_height__isnull=True)
    #                           & Q(maximum_wave_height_10_years__isnull=True)
    #                           & Q(storm_surge_10_years__isnull=True)
    #                           & Q(maximum_wave_height_100_years__isnull=True)
    #                           & Q(storm_surge_100_years__isnull=True)
    #                           & Q(maximum_wave_height_10000_years__isnull=True)
    #                           & Q(storm_surge_10000_years__isnull=True)
    #                           & Q(highest_astronomical_tide__isnull=True)
    #                           & Q(crest_height_factor__isnull=True)
    #                   )
    #                   | (
    #                           Q(cellar_deck_height__isnull=False)
    #                           & Q(maximum_wave_height_10_years__isnull=False)
    #                           & Q(storm_surge_10_years__isnull=False)
    #                           & Q(maximum_wave_height_100_years__isnull=False)
    #                           & Q(storm_surge_100_years__isnull=False)
    #                           & Q(maximum_wave_height_10000_years__isnull=False)
    #                           & Q(storm_surge_10000_years__isnull=False)
    #                           & Q(highest_astronomical_tide__isnull=False)
    #                           & Q(crest_height_factor__isnull=False)
    #                   ),
    #             name="deck_elevation_wave_in_deck_check",
    #         ),
    #     )


class AdditionalAppurtenance(models.Model):
    number_of_design_risers = models.IntegerField(
        default=0, verbose_name="[ILOF-53] number of design risers"
    )

    number_of_design_caissons = models.IntegerField(
        default=0, verbose_name="[ILOF-54] number of design caissons"
    )

    number_of_design_conductors = models.IntegerField(
        default=0, verbose_name="[ILOF-55] number of design conductors"
    )

    number_of_additional_risers = models.IntegerField(
        default=0, verbose_name="[ILOF-56] number of additional risers"
    )

    number_of_additional_caissons = models.IntegerField(
        default=0, verbose_name="[ILOF-57] number of additional caissons"
    )

    number_of_additional_conductors = models.IntegerField(
        default=0, verbose_name="[ILOF-58] number of additional conductors"
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="additional_appurtenance",
    )


class FatigueLoad(models.Model):
    water_depth = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-59] water depth (m)",
    )

    platform_with_conductor_guide_frame = models.BooleanField(
        default=False,
        verbose_name="[ILOF-60] platform with conductor guide frame (cgf)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="fatigue_load",
    )


class ReserveStrengthRatioScore(models.Model):
    reserve_strength_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-61] reserve strength ratio (rsr)",
    )

    rsr_override = models.BooleanField(
        default=False, verbose_name="[ILOF-62] rsr override"
    )

    platform = models.OneToOneField(
        "Platform",
        on_delete=models.CASCADE,
        related_name="reserve_strength_ratio_score",
    )


class EnvironmentalConsequence(models.Model):
    platform_type = models.ForeignKey(
        PlatformType,
        default = 2,
        on_delete=models.DO_NOTHING,
        verbose_name="[ILOF-64] platform type",null=True,blank=True,
    )

    daily_oil_production = models.IntegerField(
        default=0,
        verbose_name="[ILOF-65] daily oil production (if there "
                     "is no oil production, input value '0') "
                     "(bbl)",
    )

    estimated_fraction_of_oil_production_loss_due_to_leakage = models.DecimalField(
        null=True,
        default=0,
        max_digits=10,
        decimal_places=5,
        verbose_name="[ILOF-66] estimated fraction of oil production loss due to leakage (%)",
    )

    fixed_cost_for_spill_cleanup = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-67] fixed cost for spill clean-up ($)",
    )

    variable_cost_for_spill_cleanup = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-68] variable cost for spill clean-up ($/bbl)",
    )

    oil_price = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-69] oil price ($/bbl)",
    )

    platform = models.OneToOneField(
        "Platform", on_delete=models.CASCADE, related_name="environmental_consequence",
    )


class EconomicImpactConsequence(models.Model):
    daily_gas_production = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-70] daily gas production (mscf)",
    )

    gas_price = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-71] gas price ($/mscf)",
    )

    discount_date_for_interrupted_production = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-72] discount rate for interrupted production (%)",
    )

    fraction_of_remaining_production_loss = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=100,
        verbose_name="[ILOF-73] fraction of remaining production loss (%)",
    )

    platform_replacement_cost = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="[ILOF-74] platform replacement cost (usd)",
    )

    platform_replacement_time = models.IntegerField(
        default=0, verbose_name="[ILOF-75] platform replacement time (days)"
    )

    platform = models.OneToOneField(
        "Platform",
        on_delete=models.CASCADE,
        related_name="economic_impact_consequence",
    )

class OtherDetail(models.Model):
    platform = models.OneToOneField(
        "Platform",
        on_delete=models.CASCADE,
        related_name="other_detail",
    )
    corrosion_survey = models.BooleanField(null=True, blank=True)
    debris_clearance = models.BooleanField(null=True, blank=True)
    manode_confirmation = models.BooleanField(null=True, blank=True)
    marine_growth_cleaning = models.BooleanField(null=True, blank=True)
    other = models.BooleanField(null=True, blank=True)
    scour_repair = models.BooleanField(null=True, blank=True)
    weld_monitoring = models.BooleanField(null=True, blank=True)

class ScopeOfSurvey(models.Model):
    platform = models.OneToOneField(
        "Platform",
        on_delete=models.CASCADE,
        related_name="scope_of_survey",
    )

    above_water_visual_method = models.CharField(max_length=100, null=True,blank=True)
    above_water_visual_scope = models.CharField(max_length=100, null=True,blank=True)

    anodes_method = models.CharField(max_length=100, null=True,blank=True)
    anodes_scope = models.CharField(max_length=100, null=True,blank=True)

    appurtenance_survey_method = models.CharField(max_length=100, null=True,blank=True)
    appurtenance_survey_scope = models.CharField(max_length=100, null=True,blank=True)

    caissons_method = models.CharField(max_length=100, null=True,blank=True)
    caissons_scope = models.CharField(max_length=100, null=True,blank=True)

    cathodic_method = models.CharField(max_length=100, null=True,blank=True)
    cathodic_scope = models.CharField(max_length=100, null=True,blank=True)

    coating_method = models.CharField(max_length=100, null=True,blank=True)
    coating_scope = models.CharField(max_length=100, null=True,blank=True)

    conductor_method = models.CharField(max_length=100, null=True,blank=True)
    conductor_scope = models.CharField(max_length=100, null=True,blank=True)

    debris_method = models.CharField(max_length=100, null=True,blank=True)
    debris_scope = models.CharField(max_length=100, null=True,blank=True)

    deck_elevation_method = models.CharField(max_length=100, null=True,blank=True)
    deck_elevation_scope = models.CharField(max_length=100, null=True,blank=True)

    flooded_method = models.CharField(max_length=100, null=True,blank=True)
    flooded_scope = models.CharField(max_length=100, null=True,blank=True)

    general_visual_method = models.CharField(max_length=100, null=True,blank=True)
    general_visual_scope = models.CharField(max_length=100, null=True,blank=True)

    joint_ndt_method = models.CharField(max_length=100, null=True,blank=True)
    joint_ndt_scope = models.CharField(max_length=100, null=True,blank=True)

    jtube_method = models.CharField(max_length=100, null=True,blank=True)
    jtube_scope = models.CharField(max_length=100, null=True,blank=True)

    marine_growth_method = models.CharField(max_length=100, null=True,blank=True)
    marine_growth_scope = models.CharField(max_length=100, null=True,blank=True)

    risers_method = models.CharField(max_length=100, null=True,blank=True)
    risers_scope = models.CharField(max_length=100, null=True,blank=True)

    scour_depth_method = models.CharField(max_length=100, null=True,blank=True)
    scour_depth_scope = models.CharField(max_length=100, null=True,blank=True)

    supplemental_method = models.CharField(max_length=100, null=True,blank=True)
    supplemental_scope = models.CharField(max_length=100, null=True,blank=True)

    underwater_cp_method = models.CharField(max_length=100, null=True,blank=True)
    underwater_cp_scope = models.CharField(max_length=100, null=True,blank=True)

    visual_method = models.CharField(max_length=100, null=True,blank=True)
    visual_scope = models.CharField(max_length=100, null=True,blank=True)

    wallut_method = models.CharField(max_length=100, null=True,blank=True)
    wallut_scope = models.CharField(max_length=100, null=True,blank=True)

    weld_method = models.CharField(max_length=100, null=True,blank=True)    
    weld_scope = models.CharField(max_length=100, null=True,blank=True)


class PlatformQuerySet(models.QuerySet):
    # def with_access_type(self, user: settings.AUTH_USER_MODEL):
    #     platform_ownership = PlatformOwnership.objects.filter(
    #         Q(user=user) & Q(platform=OuterRef("pk"))
    #     )
    #     site_ownership = SiteOwnership.objects.filter(
    #         Q(user=user) & Q(site__platform=OuterRef("pk"))
    #     )
    #     project_ownership = ProjectOwnership.objects.filter(
    #         Q(user=user) & Q(project__site__platform=OuterRef("pk"))
    #     )
    #     return self.annotate(
    #         access_type=Coalesce(
    #             Subquery(platform_ownership.values("access_type")[:1]),
    #             Subquery(site_ownership.values("access_type")[:1]),
    #             Subquery(project_ownership.values("access_type")[:1]),
    #         ),
    #     )

    def has_ownership(self, user: settings.AUTH_USER_MODEL):
        if user.is_superuser:
            return self

        return self.filter(
            Q(users=user) | Q(project__users=user)
        ).distinct()


class Platform(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_platform')

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="PlatformOwnership"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=250)

    description = models.CharField(max_length=500, default="", blank=True)

    field_name = models.CharField(max_length=250, default="", blank=True)

    manned = models.BooleanField(default=False)

    distance_to_shore = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="distance to shore (Km)",
    )

    distance_to_shipping_lane = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="distance to shipping lane (Km)",
    )

    api_seismic_zone = models.CharField(
        max_length=250, default="", blank=True, verbose_name="api seismic zone"
    )

    number_of_bays = models.IntegerField(default=0, verbose_name="number of bays")

    number_of_main_piles = models.IntegerField(
        default=0, verbose_name="number of main piles"
    )

    number_of_skirt_piles = models.IntegerField(
        default=0, verbose_name="number of skirt piles"
    )

    number_of_decks = models.IntegerField(default=0, verbose_name="number of decks")

    deck_weight = models.DecimalField(
        max_digits=10, decimal_places=5, default=0, verbose_name="deck weight (mt)",
    )

    pile_penetration_depth = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0,
        verbose_name="pile penetration depth (m)",
    )

    jacket_repaired = models.BooleanField(default=False, verbose_name="jacket repaired")

    deck_extension = models.BooleanField(default=False, verbose_name="deck extension")

    crane = models.BooleanField(default=False, verbose_name="crane")

    helideck = models.BooleanField(default=False, verbose_name="helideck")

    boatlanding = models.BooleanField(default=False, verbose_name="boatlanding")

    anode_grade = models.IntegerField(default=0, verbose_name="anode grade")

    design_date = models.DateTimeField(
        null=True, blank=True, verbose_name="[ILOF-2] design date"
    )

    platform_installation_date = models.DateTimeField(
        verbose_name="[ILOF-3] platform installation date", default=timezone.now
    )

    number_of_legs_type = models.ForeignKey(
        NumberOfLegsType,
        on_delete=models.DO_NOTHING,
        verbose_name="[ILOF-4] number of legs",
        default=1,
    )

    bracing_type = models.ForeignKey(
        BracingType,
        on_delete=models.DO_NOTHING,
        default=1,
        verbose_name="[ILOF-5] bracing type",
    )

    environmental_consequence_description = models.CharField(max_length=300, null=True, blank=True)
    economic_consequence_description = models.CharField(max_length=300, null=True, blank=True)
    environmental_consequence_category = models.CharField(max_length=10, null=True, blank=True,default='A')
    economic_consequence_category = models.CharField(max_length=10, null=True, blank=True,default='A')
    level_1_last_inspection_date = models.DateField(null=True,blank=True)
    level_2_last_inspection_date = models.DateField(null=True,blank=True)
    level_3_last_inspection_date = models.DateField(null=True,blank=True)

    @property
    def framing_score(self):
        return Decimal(
            NUMBER_OF_LEGS_AND_BRACING_METRICS[self.bracing_type.pk - 1][
                self.number_of_legs_type.pk - 1
                ]
        )

    rbui_assessment_date = models.DateTimeField(
        default=timezone.now, verbose_name="[ILOF-12] rbui assessment date"
    )

    platform_manned_status = models.ForeignKey(
        PlatformMannedStatus,
        default = 5,
        on_delete=models.DO_NOTHING,
        verbose_name="[ILOF-63] platform manned status",null=True,blank=True
    )

    level_1_selected_inspection_interval_for_next_inspection = models.IntegerField(
        default=0,
        verbose_name="[ILOF-76] level 1 selected inspection interval for next inspection",
        null=True,blank=True
    )
    level_2_selected_inspection_interval_for_next_inspection = models.IntegerField(
        default=0,
        verbose_name="[ILOF-76] level 2 selected inspection interval for next inspection",
        null=True,blank=True
    )
    level_3_selected_inspection_interval_for_next_inspection = models.IntegerField(
        default=0,
        verbose_name="[ILOF-76] level 3 selected inspection interval for next inspection",
        null=True,blank=True
    )

    @property
    def rsr_override_score(self):
        if not self.reserve_strength_ratio_score.rsr_override:
            return 0

        value = self.reserve_strength_ratio_score.reserve_strength_ratio

        if value <= 1.0:
            return 680
        elif 1 < value < 1.32:
            return 490
        elif 1.32 <= value < 1.5:
            return 490
        elif 1.5 <= value < 1.9:
            return 120
        else:
            return 60

    objects = PlatformQuerySet.as_manager()

    def __str__(self):
        return self.name

    @transaction.atomic()
    def save(self, **kwargs):
        isnew = False

        if self.pk is None:
            isnew = True

        result = super().save(**kwargs)

        if isnew:
            logger.info("creating new platform")
            ShallowGas.objects.create(platform=self)
            LegPileGrouting.objects.create(platform=self)
            LastInspection.objects.create(platform=self)
            Corrosion.objects.create(platform=self)
            Scour.objects.create(platform=self)
            UnprotectedAppurtenances.objects.create(platform=self)
            DeckLoad.objects.create(platform=self)
            AdditionalAppurtenance.objects.create(platform=self)
            FatigueLoad.objects.create(platform=self)
            ReserveStrengthRatioScore.objects.create(platform=self)
            EnvironmentalConsequence.objects.create(platform=self)
            EconomicImpactConsequence.objects.create(platform=self)
            MechanicalDamage.objects.create(platform=self)
            FloodedMember.objects.create(platform=self)
            DeckElevationWaveInDeck.objects.create(platform=self)
            ScopeOfSurvey.objects.create(platform=self)
            OtherDetail.objects.create(platform=self)

        return result

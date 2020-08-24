import logging
from functools import lru_cache
from typing import Dict

from django.db import transaction
from rest_framework import serializers

from .calculators import (
    PlatformVintageScoreCalculator,
    PlatformLegsAndBracingScoreCalculator,
    ShallowGasScoreCalculator,
    LastInspectionScoreCalculator,
    LegPileGroutingScoreCalculator,
    MechanicalDamageScoreCalculator,
    CorrosionScoreCalculator,
    MarineGrowthScoreCalculator,
    ScourCalculator,
    FloodedMemberScoreCalculator,
    UnprotectedAppurtenancesScoreCalculator,
    DeckLoadScoreCalculator,
    DeckElevationWaveInDeckScoreCalculator,
    AdditionalAppurtenanceScoreCalculator,
    FatigueLoadScoreCalculator,
    EnvironmentalConsequenceCategoryCalculator,
    RiskBasedUnderwaterIntervalScoreCalculator,
    ExposureCategoryLevelCalculator,
    ExposureCategorySurveyLevel1Calculator,
    ExposureCategorySurveyLevel2Calculator,
    ExposureCategorySurveyLevel3Calculator,
    Level1InspectionDateCalculator,
    Level2InspectionDateCalculator,
    Level3InspectionDateCalculator,
    CalculatedEconmicImpactConsequenceCalculator,
    CalculateEconomicImpactRemainingLifeServicesCalculator,
    StructureReplacementDecisionCalculator,
    FinalConsequenceCategoryCalculator,
    RiskRankingCalculator,
)
from .models import (
    User,
    Project,
    Site,
    Platform,
    PlatformType,
    NumberOfLegsType,
    PlatformMannedStatus,
    DeckElevationWaveInDeck,
    ShallowGas,
    LastInspection,
    LegPileGrouting,
    MechanicalDamage,
    Corrosion,
    MarineGrowth,
    Scour,
    FloodedMember,
    UnprotectedAppurtenances,
    DeckLoad,
    AdditionalAppurtenance,
    FatigueLoad,
    ReserveStrengthRatioScore,
    EnvironmentalConsequence,
    EconomicImpactConsequence,
)

logger = logging.getLogger("core.serializers")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = "__all__"


class SiteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Site
        exclude = ("users",)


class PlatformTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PlatformType
        fields = "__all__"


class BracingTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PlatformType
        fields = "__all__"


class NumberOfLegsTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = NumberOfLegsType
        fields = "__all__"


class PlatformMannedStatusSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PlatformMannedStatus
        fields = "__all__"


class LegPileGroutingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = LegPileGrouting
        exclude = ("platform",)


class DeckElevationWaveInDeckSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = DeckElevationWaveInDeck
        exclude = ("platform",)


class ShallowGasSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ShallowGas
        exclude = ("platform",)


class LastInspectionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = LastInspection
        exclude = ("platform",)


class MechanicalDamageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = MechanicalDamage
        exclude = ("platform",)


class CorrosionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Corrosion
        exclude = ("platform",)


class MarineGrowthSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = MarineGrowth
        exclude = ()


class ScourSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Scour
        exclude = ("platform",)


class FloodedMemberSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = FloodedMember
        exclude = ("platform",)


class UnprotectedAppurtenancesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UnprotectedAppurtenances
        exclude = ("platform",)


class DeckLoadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = DeckLoad
        exclude = ("platform",)


class AdditionalAppurtenanceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = AdditionalAppurtenance
        exclude = ("platform",)


class FatigueLoadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = FatigueLoad
        exclude = ("platform",)


class ReserveStrengthRatioScoreSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ReserveStrengthRatioScore
        exclude = ("platform",)


class EnvironmentalConsequenceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    platform_type = PlatformTypeSerializer(read_only=True)

    platform_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EnvironmentalConsequence
        exclude = ("platform",)


class EconomicImpactConsequenceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = EconomicImpactConsequence
        exclude = ("platform",)


class PlatformSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    platform_vintage_score = serializers.SerializerMethodField(read_only=True)

    access_type = serializers.SerializerMethodField(read_only=True)

    platform_legs_and_bracing_score = serializers.SerializerMethodField(read_only=True)

    leg_pile_grouting = LegPileGroutingSerializer()

    leg_pile_grouting_score = serializers.SerializerMethodField(read_only=True)

    shallow_gas = ShallowGasSerializer()

    shallow_gas_score = serializers.SerializerMethodField(read_only=True)

    last_inspection = LastInspectionSerializer()

    last_inspection_score = serializers.SerializerMethodField(read_only=True)

    mechanical_damage = MechanicalDamageSerializer()

    mechanical_damage_score = serializers.SerializerMethodField(read_only=True)

    corrosion = CorrosionSerializer()

    corrosion_score = serializers.SerializerMethodField(read_only=True)

    marine_growths = MarineGrowthSerializer(many=True, read_only=True)

    marine_growths_score = serializers.SerializerMethodField(read_only=True)

    scour = ScourSerializer()

    scour_score = serializers.SerializerMethodField(read_only=True)

    flooded_member = FloodedMemberSerializer()

    flooded_member_score = serializers.SerializerMethodField(read_only=True)

    unprotected_appurtenances = UnprotectedAppurtenancesSerializer()

    unprotected_appurtenances_score = serializers.SerializerMethodField(read_only=True)

    deck_load = DeckLoadSerializer()

    deck_load_score = serializers.SerializerMethodField(read_only=True)

    deck_elevation_wave_in_deck = DeckElevationWaveInDeckSerializer()

    deck_elevation_wave_in_deck_score = serializers.SerializerMethodField(
        read_only=True
    )

    additional_appurtenance = AdditionalAppurtenanceSerializer()

    additional_appurtenance_score = serializers.SerializerMethodField(read_only=True)

    fatigue_load = FatigueLoadSerializer()

    fatigue_load_score = serializers.SerializerMethodField(read_only=True)

    reserve_strength_ratio_score = ReserveStrengthRatioScoreSerializer()

    platform_manned_status = PlatformMannedStatusSerializer(read_only=True)

    platform_manned_status_id = serializers.IntegerField(write_only=True)

    environmental_consequence = EnvironmentalConsequenceSerializer()

    economic_impact_consequence = EconomicImpactConsequenceSerializer()

    site = SiteSerializer(read_only=True)

    bracing_type = BracingTypeSerializer(read_only=True)

    bracing_type_id = serializers.IntegerField(write_only=True)

    number_of_legs_type = NumberOfLegsTypeSerializer(read_only=True)

    number_of_legs_type_id = serializers.IntegerField(write_only=True)

    robustness_score = serializers.SerializerMethodField(read_only=True)

    condition_score = serializers.SerializerMethodField(read_only=True)

    loading_score = serializers.SerializerMethodField(read_only=True)

    total_score = serializers.SerializerMethodField(read_only=True)

    rsr_override_score = serializers.ReadOnlyField()

    lof_ranking = serializers.SerializerMethodField(read_only=True)

    calculated_environmental_consequence = serializers.SerializerMethodField(
        read_only=True
    )

    calculated_economic_impact_consequence = serializers.SerializerMethodField(read_only=True)

    calculate_economic_impact_remaining_life_services = serializers.SerializerMethodField(read_only=True)

    risk_based_underwater_inspection_interval = serializers.SerializerMethodField(read_only=True)

    structure_replacement_decision = serializers.SerializerMethodField(read_only=True)

    exposure_category_level = serializers.SerializerMethodField(read_only=True)

    exposure_category_level_1 = serializers.SerializerMethodField(read_only=True)

    exposure_category_level_2 = serializers.SerializerMethodField(read_only=True)

    exposure_category_level_3 = serializers.SerializerMethodField(read_only=True)

    level_1_inspection_date = serializers.SerializerMethodField(read_only=True)

    level_2_inspection_date = serializers.SerializerMethodField(read_only=True)

    level_3_inspection_date = serializers.SerializerMethodField(read_only=True)

    final_consequence_category = serializers.SerializerMethodField(read_only=True)

    risk_ranking = serializers.SerializerMethodField(read_only=True)

    @lru_cache(maxsize=1)
    def get_risk_ranking(self, obj: Platform):
        return RiskRankingCalculator(obj)._calculate()

    @lru_cache(maxsize=1)
    def get_final_consequence_category(self, obj: Platform):
        return FinalConsequenceCategoryCalculator(obj)._calculate()

    @lru_cache(maxsize=1)
    def get_structure_replacement_decision(self, obj: Platform):
        return StructureReplacementDecisionCalculator(obj)._calculate()

    @lru_cache(maxsize=1)
    def get_calculate_economic_impact_remaining_life_services(self, obj: Platform):
        return CalculateEconomicImpactRemainingLifeServicesCalculator(obj)._calculate()

    @lru_cache(maxsize=1)
    def get_calculated_economic_impact_consequence(self, obj: Platform):
        return CalculatedEconmicImpactConsequenceCalculator(obj)._calculate()

    @lru_cache(maxsize=1)
    def get_exposure_category_level(self, obj: Platform):
        return ExposureCategoryLevelCalculator()._calculate()

    @lru_cache(maxsize=1)
    def get_exposure_category_level_1(self, obj: Platform):
        return ExposureCategorySurveyLevel1Calculator()._calculate()

    @lru_cache(maxsize=1)
    def get_exposure_category_level_2(self, obj: Platform):
        return ExposureCategorySurveyLevel2Calculator()._calculate()

    @lru_cache(maxsize=1)
    def get_exposure_category_level_3(self, obj: Platform):
        return ExposureCategorySurveyLevel3Calculator()._calculate()

    @lru_cache(maxsize=1)
    def get_level_1_inspection_date(self, obj: Platform):
        return Level1InspectionDateCalculator()._calculate()

    @lru_cache(maxsize=1)
    def get_level_2_inspection_date(self, obj: Platform):
        return Level2InspectionDateCalculator()._calculate()

    @lru_cache(maxsize=1)
    def get_level_3_inspection_date(self, obj: Platform):
        return Level3InspectionDateCalculator()._calculate()

    @lru_cache(maxsize=1)
    def get_risk_based_underwater_inspection_interval(self, obj: Platform):
        return RiskBasedUnderwaterIntervalScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_platform_vintage_score(self, obj: Platform):
        return PlatformVintageScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_platform_legs_and_bracing_score(self, obj: Platform):
        return PlatformLegsAndBracingScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_leg_pile_grouting_score(self, obj: Platform):
        return LegPileGroutingScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_shallow_gas_score(self, obj: Platform):
        return ShallowGasScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_last_inspection_score(self, obj: Platform):
        return LastInspectionScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_mechanical_damage_score(self, obj: Platform):
        return MechanicalDamageScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_corrosion_score(self, obj: Platform):
        return CorrosionScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_marine_growths_score(self, obj: Platform):
        return MarineGrowthScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_scour_score(self, obj: Platform):
        return ScourCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_flooded_member_score(self, obj: Platform):
        return FloodedMemberScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_unprotected_appurtenances_score(self, obj: Platform):
        return UnprotectedAppurtenancesScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_deck_load_score(self, obj: Platform):
        return DeckLoadScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_deck_elevation_wave_in_deck_score(self, obj: Platform):
        return DeckElevationWaveInDeckScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_additional_appurtenance_score(self, obj: Platform):
        return AdditionalAppurtenanceScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_fatigue_load_score(self, obj: Platform):
        return FatigueLoadScoreCalculator(obj).calculate()

    @lru_cache(maxsize=1)
    def get_access_type(self, obj: Platform):
        request = self.context.get("request")

        if request.user.is_superuser:
            return "M"

        return (
            Platform.objects.filter(pk=obj.id)
            .with_access_type(user=request.user)[0]
            .access_type
        )

    @lru_cache(maxsize=1)
    def get_robustness_score(self, obj: Platform):
        return (
            self.get_platform_vintage_score(obj)
            + self.get_platform_legs_and_bracing_score(obj)
            + self.get_leg_pile_grouting_score(obj)
            + self.get_shallow_gas_score(obj)
        )

    @lru_cache(maxsize=1)
    def get_condition_score(self, obj: Platform):
        return (
            self.get_last_inspection_score(obj)
            + self.get_mechanical_damage_score(obj)
            + self.get_corrosion_score(obj)
            + self.get_marine_growths_score(obj)
            + self.get_scour_score(obj)
            + self.get_flooded_member_score(obj)
            + self.get_unprotected_appurtenances_score(obj)
        )

    @lru_cache(maxsize=1)
    def get_loading_score(self, obj: Platform):
        return (
            self.get_deck_load_score(obj)
            + self.get_deck_elevation_wave_in_deck_score(obj)
            + self.get_additional_appurtenance_score(obj)
            + self.get_fatigue_load_score(obj)
        )

    @lru_cache(maxsize=1)
    def get_total_score(self, obj: Platform):
        return (
            self.get_robustness_score(obj)
            + self.get_condition_score(obj)
            + self.get_loading_score(obj)
            + obj.rsr_override_score
        )

    @lru_cache(maxsize=1)
    def get_lof_ranking(self, obj: Platform):
        score = self.get_total_score(obj)

        if score >= 680:
            return 5
        elif 490 <= score < 680:
            return 4
        elif 310 <= score < 490:
            return 3
        elif 120 <= score < 310:
            return 2
        else:
            return 1

    def get_calculated_environmental_consequence(self, obj: Platform):
        return EnvironmentalConsequenceCategoryCalculator(obj).calculate()

    @transaction.atomic()
    def update(self, instance: Platform, validated_data: Dict):
        print("update ",validated_data)
        shallow_gas = validated_data.pop("shallow_gas")
        ShallowGas.objects.filter(platform=instance).update(**shallow_gas)

        last_inspection = validated_data.pop("last_inspection")
        LastInspection.objects.filter(platform=instance).update(**last_inspection)

        leg_pile_grouting = validated_data.pop("leg_pile_grouting")
        LegPileGrouting.objects.filter(platform=instance).update(**leg_pile_grouting)

        mechanical_damage = validated_data.pop("mechanical_damage")
        MechanicalDamage.objects.filter(platform=instance).update(**mechanical_damage)

        corrosion = validated_data.pop("corrosion")
        Corrosion.objects.filter(platform=instance).update(**corrosion)

        scour = validated_data.pop("scour")
        Scour.objects.filter(platform=instance).update(**scour)

        flooded_member = validated_data.pop("flooded_member")
        FloodedMember.objects.filter(platform=instance).update(**flooded_member)

        unprotected_appurtenances = validated_data.pop("unprotected_appurtenances")
        UnprotectedAppurtenances.objects.filter(platform=instance).update(
            **unprotected_appurtenances
        )

        deck_load = validated_data.pop("deck_load")
        DeckLoad.objects.filter(platform=instance).update(**deck_load)

        deck_elevation_wave_in_deck = validated_data.pop("deck_elevation_wave_in_deck")
        DeckElevationWaveInDeck.objects.filter(platform=instance).update(
            **deck_elevation_wave_in_deck
        )

        additional_appurtenance = validated_data.pop("additional_appurtenance")
        AdditionalAppurtenance.objects.filter(platform=instance).update(
            **additional_appurtenance
        )

        fatigue_load = validated_data.pop("fatigue_load")
        FatigueLoad.objects.filter(platform=instance).update(**fatigue_load)

        reserve_strength_ratio_score = validated_data.pop(
            "reserve_strength_ratio_score"
        )
        ReserveStrengthRatioScore.objects.filter(platform=instance).update(
            **reserve_strength_ratio_score
        )

        environmental_consequence = validated_data.pop("environmental_consequence")
        EnvironmentalConsequence.objects.filter(platform=instance).update(
            **environmental_consequence
        )

        economic_impact_consequence = validated_data.pop("economic_impact_consequence")
        EconomicImpactConsequence.objects.filter(platform=instance).update(
            **economic_impact_consequence
        )

        return super().update(instance, validated_data)

    class Meta:
        model = Platform
        exclude = ("users",)

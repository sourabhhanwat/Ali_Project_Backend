import logging
from decimal import Decimal, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from core.models import Platform

logger = logging.getLogger("core.calculators")


class BaseCalculator:
    override_applied = False

    score_max: Decimal
    score_min: Decimal
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self) -> Decimal:
        pass

    def calculate(self) -> Decimal:
        if self.override_applied:
            if self.instance.reserve_strength_ratio_score.rsr_override:
                return Decimal(0)

        value = self._calculate()

        if type(value) is list:
            return value

        if value > self.score_max:
            return self.score_max

        if value < self.score_min:
            return self.score_min

        return value


class PlatformVintageScoreCalculator(BaseCalculator):
    override_applied = True

    dd_h = Decimal(10)
    dd_m = Decimal(6)
    dd_l = Decimal(4)
    score_max = Decimal(80)
    score_min = Decimal(32)
    w_dd = Decimal(8)

    def _calculate(self):
        try:
            clof_1 = self.instance.design_date.year
        except AttributeError:
            clof_1 = self.instance.platform_installation_date.year - 2

        if clof_1 > 1969:
            if clof_1 > 1979:
                clof_2 = self.dd_l
            else:
                clof_2 = self.dd_m
        else:
            clof_2 = self.dd_h

        clof_3 = self.w_dd

        clof_4 = clof_2 * clof_3

        return clof_4
    
class Level1NextInspectionDateCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        try:
            last_inspection_date = self.instance.level_1_last_inspection_date
            interval = self.instance.level_1_selected_inspection_interval_for_next_inspection

            next_inspection_date = last_inspection_date + relativedelta(years=interval)

            return next_inspection_date
        except:
            return None

class Level2NextInspectionDateCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        try:
            last_inspection_date = self.instance.level_2_last_inspection_date
            interval = self.instance.level_2_selected_inspection_interval_for_next_inspection

            next_inspection_date = last_inspection_date + relativedelta(years=interval)

            return next_inspection_date
        except:
            return None

class Level3NextInspectionDateCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        try:
            last_inspection_date = self.instance.level_3_last_inspection_date
            interval = self.instance.level_3_selected_inspection_interval_for_next_inspection

            next_inspection_date = last_inspection_date + relativedelta(years=interval)

            return next_inspection_date
        except:
            return None

class Next10YearsInspectionPlanCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        
        level_1_inspection_date = self.instance.level_1_last_inspection_date
        level_2_inspection_date = self.instance.level_2_last_inspection_date
        level_3_inspection_date = self.instance.level_3_last_inspection_date
        level_1_interval = self.instance.level_1_selected_inspection_interval_for_next_inspection
        level_2_interval = self.instance.level_2_selected_inspection_interval_for_next_inspection
        level_3_interval = self.instance.level_3_selected_inspection_interval_for_next_inspection

        current_year = datetime.now().year
        if level_1_inspection_date is not None:
            level_1_inspection_date = level_1_inspection_date + relativedelta(years=level_1_interval)
            if level_1_inspection_date.year < current_year:
                for x in range(0,10):
                    level_1_inspection_date = level_1_inspection_date + relativedelta(years=level_1_interval)
                    if level_1_inspection_date.year >= datetime.now().year:
                        break
        else:
            level_1_inspection_date = datetime(1900, 5, 17)

        if level_2_inspection_date is not None:
            level_2_inspection_date = level_2_inspection_date + relativedelta(years=level_2_interval)
            if level_2_inspection_date.year < current_year:
                for x in range(0,10):
                    level_2_inspection_date = level_2_inspection_date + relativedelta(years=level_2_interval)
                    if level_2_inspection_date.year >= datetime.now().year:
                        break
        else:
            level_2_inspection_date = datetime(1900, 5, 17)

        if level_3_inspection_date is not None:
            level_3_inspection_date = level_3_inspection_date + relativedelta(years=level_3_interval)
            if level_3_inspection_date.year < current_year:
                for x in range(0,10):
                    level_3_inspection_date = level_3_inspection_date + relativedelta(years=level_3_interval)
                    if level_3_inspection_date.year >= datetime.now().year:
                        break
        else:
            level_3_inspection_date = datetime(1900, 5, 17)
        
        next_inspection=[]
        level_1_count = 0
        level_2_count = 0
        level_3_count = 0
        try:
            for i in range(0,10):

                next_date = datetime.now().year + i
            
                date_1 = datetime.now().year + 1
                date_10 = datetime.now().year + 9
                if next_date == level_1_inspection_date.year and next_date == level_2_inspection_date.year and next_date == level_3_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 1, Level 2, Level 3"})
                
                elif next_date == level_1_inspection_date.year and next_date == level_2_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 1, Level 2"})

                elif next_date == level_1_inspection_date.year and next_date == level_3_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 1, Level 3"})

                elif next_date == level_2_inspection_date.year and next_date == level_3_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 2, Level 3"})
                
                elif next_date == level_1_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 1"})

                elif next_date == level_2_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 2"})

                elif next_date == level_3_inspection_date.year:
                    next_inspection.append({"year":next_date,
                                            "level":"Level 3"})
                
                else:
                    next_inspection.append({"year":next_date,
                                            "level":"No Inspection"})


                if level_1_inspection_date.year==next_date:
                    level_1_inspection_date = level_1_inspection_date + relativedelta(years=level_1_interval)

                if level_2_inspection_date.year==next_date:
                    level_2_inspection_date = level_2_inspection_date + relativedelta(years=level_2_interval)            

                if level_3_inspection_date.year==next_date:
                    level_3_inspection_date = level_3_inspection_date + relativedelta(years=level_3_interval)
        except:
            next_inspection=[]
            for i in range(0,10):
                next_date = datetime.now().year + i
                next_inspection.append({"year":next_date,
                                        "level":""})

        return next_inspection


class PlatformLegsAndBracingScoreCalculator(BaseCalculator):
    override_applied = True

    w_blg = Decimal(10)
    score_min = Decimal(20)
    score_max = Decimal(100)

    def _calculate(self):
        clof_5 = self.instance.framing_score
        clof_6 = self.w_blg
        clof_7 = clof_5 * clof_6
        return clof_7


class LegPileGroutingScoreCalculator(BaseCalculator):
    override_applied = True

    gr_ll = Decimal(0)
    gr_el = Decimal(4)
    gr_lh = Decimal(4)
    gr_eh = Decimal(10)
    w_gr = Decimal(2)
    score_min = Decimal(0)
    score_max = Decimal(20)

    def _calculate(self):
        leg_pile_grouting = self.instance.leg_pile_grouting

        if leg_pile_grouting.pile_in_leg_installation:
            try:
                clof_8 = self.instance.design_date.year
            except AttributeError:
                clof_8 = self.instance.platform_installation_date.year - 2

            if clof_8 > 1975:
                if leg_pile_grouting.leg_to_pile_annulus_grouted:
                    clof_9 = self.gr_ll
                else:
                    clof_9 = self.gr_lh
            else:
                if leg_pile_grouting.leg_to_pile_annulus_grouted:
                    clof_9 = self.gr_el
                else:
                    clof_9 = self.gr_eh

        else:
            clof_9 = 0

        clof_10 = self.w_gr

        clof_11 = clof_9 * clof_10

        return clof_11


class ShallowGasScoreCalculator(BaseCalculator):
    override_applied = True

    sh_h = Decimal(10)
    sh_m = Decimal(5)
    w_sh = Decimal(2)
    score_max = Decimal(20)
    score_min = Decimal(0)

    def _calculate(self):
        shallow_gas = self.instance.shallow_gas

        if shallow_gas.shallow_gas_effect_detected:
            if shallow_gas.shallow_gas_monitored:
                clof_12 = self.sh_m
            else:
                clof_12 = self.sh_h
        else:
            clof_12 = Decimal(0)

        clof_13 = self.w_sh

        clof_14 = clof_12 * clof_13

        return clof_14


class LastInspectionScoreCalculator(BaseCalculator):
    default_interval = Decimal(5)
    in_l = Decimal(0)
    in_m = Decimal(4)
    in_h = Decimal(10)
    in_vh = Decimal(20)
    score_max = Decimal(200)
    score_min = Decimal(0)
    w_in = Decimal(10)

    def _calculate(self) -> float:
        """
        Check with Ali if this value should be float or int.
        :return:
        """

        last_inspection = self.instance.last_inspection

        try:
            clof_15 = last_inspection.last_underwater_inspection_date.year
        except AttributeError:
            clof_15 = self.instance.platform_installation_date.year

        clof_16 = self.instance.rbui_assessment_date.year - clof_15

        try:
            clof_17 = last_inspection.rbui_inspection_interval
            assert clof_17 is not None
        except (AttributeError, AssertionError):
            clof_17 = self.default_interval

        if clof_16 > clof_17 * 1:
            if clof_16 > clof_17 * 2:
                if clof_16 > clof_17 * 3:
                    clof_18 = self.in_vh
                else:
                    clof_18 = self.in_h
            else:
                clof_18 = self.in_m
        else:
            clof_18 = self.in_l

        clof_19 = self.instance.framing_score

        clof_20 = ((clof_18 * clof_19) / 10).quantize(1, ROUND_HALF_UP)
        clof_21 = self.w_in
        clof_22 = clof_20 * clof_21

        return clof_22


class MechanicalDamageScoreCalculator(BaseCalculator):
    override_applied = True

    dm_h = Decimal(10)
    dm_m = Decimal(7)
    dm_l = Decimal(3)
    dm_nil = Decimal(0)
    dm_unk = Decimal(3)
    w_dm = Decimal(10)
    score_max = Decimal(100)
    score_min = Decimal(0)

    def _calculate(self):
        """
        Ask Ali if this should be float or int
        :return:
        """
        try:

            ilof_16 = self.instance.mechanical_damage.number_of_damaged_members
            assert ilof_16 is not None

            if ilof_16 > 0:
                if ilof_16 > 3:
                    if ilof_16 > 6:
                        clof_23 = self.dm_h
                    else:
                        clof_23 = self.dm_m
                else:
                    clof_23 = self.dm_l
            else:
                clof_23 = self.dm_nil

        except AssertionError:
            clof_23 = self.dm_unk

        clof_24 = self.instance.framing_score

        clof_25 = ((clof_23 * clof_24) / 10).quantize(1, ROUND_HALF_UP)

        clof_26 = self.w_dm

        clof_27 = clof_25 * clof_26

        return clof_27


class CorrosionScoreCalculator(BaseCalculator):
    """
    TODO -
    The value in the document for CLOF-38 is all the same. Report to Ali
    CLOF-32 and CLOF-33 diagram does not makes sense.
    """

    dep_vh = Decimal(10)
    dep_h = Decimal(7)
    dep_m = Decimal(3)
    dep_l = Decimal(0)

    pot_vh = Decimal(10)
    pot_h = Decimal(7)
    pot_m = Decimal(3)
    pot_l = Decimal(0)

    w_cor = Decimal(5)
    score_max = Decimal(50)
    score_min = Decimal(0)

    def _calculate(self) -> float:
        corrosion = self.instance.corrosion

        try:
            clof_28 = corrosion.cp_design_life
            assert clof_28 is not None
        except (AttributeError, AssertionError):
            clof_28 = corrosion.platform_design_life

        try:
            clof_29 = corrosion.anode_retrofit_date
            assert clof_29 is not None
        except (AttributeError, AssertionError):
            clof_29 = corrosion.original_anode_installation_date

        clof_30 = (100 / Decimal(clof_28)).quantize(1, ROUND_HALF_UP)

        if corrosion.anode_survey_inspection_date:
            clof_34 = (
                    relativedelta(corrosion.anode_survey_inspection_date, clof_29).days
                    / Decimal(365)
            ).quantize(1, ROUND_HALF_UP)

            if clof_34 == 0:
                clof_34 = 1

            clof_35 = (
                    corrosion.average_anode_depletion_from_survey / clof_34
            ).quantize(1, ROUND_HALF_UP)

            if clof_35 > clof_30:
                clof_36 = clof_35
            else:
                clof_36 = clof_30

            clof_37 = corrosion.average_anode_depletion_from_survey + (
                    (
                            relativedelta(
                                self.instance.rbui_assessment_date,
                                corrosion.anode_survey_inspection_date,
                            ).days
                            / Decimal(365)
                    ).quantize(1, ROUND_HALF_UP)
                    * clof_36
            )
            if clof_37 > 10:
                if clof_37 > 50:
                    if clof_37 > 75:
                        clof_42 = clof_38 = self.dep_vh
                    else:
                        clof_42 = clof_38 = self.dep_h
                else:
                    clof_42 = clof_38 = self.dep_m
            else:
                clof_42 = clof_38 = self.dep_l

        else:
            clof_31 = (
                    relativedelta(self.instance.rbui_assessment_date, clof_29).days
                    / Decimal(365)
            ).quantize(1, ROUND_HALF_UP)

            if clof_31 < clof_28:
                clof_32 = clof_31 * clof_30
                if clof_32 > 10:
                    if clof_32 > 50:
                        if clof_32 > 75:
                            clof_42 = clof_33 = self.dep_vh
                        else:
                            clof_42 = clof_33 = self.dep_h
                    else:
                        clof_42 = clof_33 = self.dep_m
                else:
                    clof_42 = clof_33 = self.dep_l
            else:
                clof_42 = clof_33 = self.dep_vh

        if corrosion.average_anode_potential_from_survey:
            if corrosion.average_anode_potential_from_survey > -950:
                if corrosion.average_anode_potential_from_survey > -850:
                    if corrosion.average_anode_potential_from_survey > -750:
                        clof_43 = clof_41 = self.pot_vh
                    else:
                        clof_43 = clof_41 = self.pot_h
                else:
                    clof_43 = clof_41 = self.pot_m
            else:
                clof_43 = clof_41 = self.pot_l
        else:
            clof_39 = (
                    relativedelta(
                        self.instance.rbui_assessment_date,
                        self.instance.platform_installation_date,
                    ).days
                    / Decimal(365)
            ).quantize(1, ROUND_HALF_UP)

            if clof_39 > ((75 / Decimal(100)).quantize(1, ROUND_HALF_UP) * clof_28):
                clof_43 = clof_40 = self.pot_vh
            else:
                clof_43 = clof_40 = self.pot_m

        clof_44 = ((Decimal(clof_42) + Decimal(clof_43)) / 2).quantize(1, ROUND_HALF_UP)
        clof_45 = self.w_cor * clof_44

        return clof_45

class MarineGrowthEachElevationCalculator(BaseCalculator):
    override_applied = True
    score_max = Decimal(20)
    score_min = Decimal(0)
    mg_h = Decimal(10)
    mg_m = Decimal(7)
    mg_l = Decimal(3)
    w_mg = Decimal(2)
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        marine_growths = self.instance.marine_growths
        if self.override_applied:
            if self.instance.reserve_strength_ratio_score.rsr_override:
                marine=[]
                return marine
        clof_47 = []
        if marine_growths.count() > 0:

            for marine_growth in marine_growths.all():
                if (
                        marine_growth.marine_growth_inspected_thickness
                        > marine_growth.marine_growth_design_thickness
                ):
                    if (
                            marine_growth.marine_growth_inspected_thickness
                            > marine_growth.marine_growth_design_thickness * Decimal("1.5")
                    ):
                        if (
                                marine_growth.marine_growth_inspected_thickness
                                > marine_growth.marine_growth_design_thickness * Decimal("2")
                        ):
                            clof_47.append(self.mg_h)
                        else:
                            clof_47.append(self.mg_m)
                    else:
                        clof_47.append(self.mg_l)
                else:
                    clof_47.append(0)
        
        return clof_47

class MarineGrowthScoreCalculator(BaseCalculator):
    override_applied = True
    score_max = Decimal(20)
    score_min = Decimal(0)
    mg_h = Decimal(10)
    mg_m = Decimal(7)
    mg_l = Decimal(3)
    w_mg = Decimal(2)

    def _calculate(self):
        marine_growths = self.instance.marine_growths

        if marine_growths.count() > 0:
            clof_47 = []

            for marine_growth in marine_growths.all():
                if (
                        marine_growth.marine_growth_inspected_thickness
                        > marine_growth.marine_growth_design_thickness
                ):
                    if (
                            marine_growth.marine_growth_inspected_thickness
                            > marine_growth.marine_growth_design_thickness * Decimal("1.5")
                    ):
                        if (
                                marine_growth.marine_growth_inspected_thickness
                                > marine_growth.marine_growth_design_thickness * Decimal("2")
                        ):
                            clof_47.append(self.mg_h)
                        else:
                            clof_47.append(self.mg_m)
                    else:
                        clof_47.append(self.mg_l)
                else:
                    clof_47.append(0)

            clof_48 = max(clof_47)
            clof_49 = self.w_mg * clof_48
        else:
            clof_46 = 3
            clof_49 = self.w_mg * clof_46

        return clof_49


class ScourCalculator(BaseCalculator):
    override_applied = True
    score_max = 20
    score_min = 0

    sd_l = 0
    sd_m = 3
    sd_h = 7
    sd_vh = 10
    w_sd = 2

    def _calculate(self):
        scour = self.instance.scour

        if scour.measured_scour_depth_during_inspection:
            if scour.measured_scour_depth_during_inspection > scour.design_scour_depth:
                if (
                        scour.measured_scour_depth_during_inspection * 2
                        > scour.design_scour_depth
                ):
                    if (
                            scour.measured_scour_depth_during_inspection * 3
                            > scour.design_scour_depth
                    ):
                        clof_51 = self.sd_vh
                    else:
                        clof_51 = self.sd_h
                else:
                    clof_51 = self.sd_m
            else:
                clof_51 = self.sd_l

            clof_52 = clof_51 * self.w_sd
        else:
            clof_50 = 3
            clof_52 = clof_50 * self.w_sd

        return clof_52


class FloodedMemberScoreCalculator(BaseCalculator):
    """
    CLOF-54, CLOF-57 should the unit be years?
    """

    override_applied = True

    score_max = Decimal(100)
    score_min = Decimal(0)

    fm_h = Decimal(10)
    fm_m = Decimal(7)
    fm_l = Decimal(3)
    w_fm = Decimal(10)

    def _calculate(self):
        flooded_member = self.instance.flooded_member

        if flooded_member.number_of_flooded_members_in_last_inspection is not None:
            if flooded_member.number_of_flooded_members_in_last_inspection > 0:
                clof_54 = Decimal(
                    relativedelta(
                        flooded_member.flooded_members_last_inspection_date,
                        flooded_member.previous_flooded_members_inspection_date,
                    ).years
                )

                clof_55 = Decimal(
                    flooded_member.number_of_flooded_members_in_last_inspection
                    - flooded_member.number_of_previous_inspection_flooded_members
                )

                clof_56 = (clof_55 / clof_54).quantize(1, ROUND_HALF_UP)

                clof_57 = relativedelta(
                    self.instance.rbui_assessment_date,
                    flooded_member.flooded_members_last_inspection_date,
                ).years

                clof_58 = (
                        flooded_member.number_of_flooded_members_in_last_inspection
                        + (clof_56 * clof_57 * Decimal("1.5"))
                )

                if clof_58 > 3:
                    if clof_58 > 9:
                        clof_60 = clof_59 = self.fm_h
                    else:
                        clof_60 = clof_59 = self.fm_m
                else:
                    clof_60 = clof_59 = self.fm_l

            else:
                clof_60 = clof_59 = Decimal(0)
        else:
            clof_60 = clof_53 = Decimal(3)

        clof_61 = self.instance.framing_score

        clof_62 = ((clof_60 * clof_61) / Decimal(10)).quantize(1, ROUND_HALF_UP)

        clof_63 = self.w_fm * clof_62

        return clof_63


class UnprotectedAppurtenancesScoreCalculator(BaseCalculator):
    tu_hr = Decimal(8)
    tu_hc = Decimal(6)
    w_upa = Decimal(5)

    score_max = Decimal(70)
    score_min = Decimal(0)

    def _calculate(self):
        unprotected_appurtenances = self.instance.unprotected_appurtenances
        if unprotected_appurtenances.number_of_unprotected_gas_riser is not None:
            if unprotected_appurtenances.number_of_unprotected_gas_riser > 0:
                clof_64 = self.tu_hr
            else:
                clof_64 = 0
        else:
            clof_64 = 0

        if unprotected_appurtenances.number_of_unprotected_conductor is not None:
            if unprotected_appurtenances.number_of_unprotected_conductor > 0:
                clof_65 = self.tu_hc
            else:
                clof_65 = 0
        else:
            clof_65 = 0

        clof_66 = clof_65 + clof_64

        clof_67 = clof_66 * self.w_upa

        return clof_67


class DeckLoadScoreCalculator(BaseCalculator):
    override_applied = True
    score_max = Decimal(20)
    score_min = Decimal(0)

    dl_kh = Decimal(8)
    dl_km = Decimal(4)
    dl_kl = Decimal(2)

    dl_uh = Decimal(10)
    dl_um = Decimal(8)
    dl_ul = Decimal(4)

    w_dl = Decimal(2)

    def _calculate(self):
        deck_load = self.instance.deck_load

        if (
                deck_load.original_topsides_design_load_known
                and deck_load.increase_in_topsides_load is not None
        ):
            if deck_load.increase_in_topsides_load > 0:
                if deck_load.increase_in_topsides_load > 10:
                    if deck_load.increase_in_topsides_load > 20:
                        clof_69 = self.dl_kh
                    else:
                        clof_69 = self.dl_km
                else:
                    clof_69 = self.dl_kl
            else:
                clof_69 = 0
        else:
            clof_68 = relativedelta(
                self.instance.rbui_assessment_date,
                self.instance.platform_installation_date,
            ).years

            if clof_68 > 10:
                if clof_68 > 20:
                    clof_69 = self.dl_uh
                else:
                    clof_69 = self.dl_um
            else:
                clof_69 = self.dl_ul

        clof_70 = clof_69 * self.w_dl

        return clof_70


class DeckElevationWaveInDeckScoreCalculator(BaseCalculator):
    override_applied = True
    score_max = Decimal(20)
    score_min = Decimal(0)

    wid_h = Decimal(10)
    wid_m = Decimal(5)
    wid_l = Decimal(2)
    w_wid = Decimal(2)

    def _calculate(self):
        deck_elevation_wave_in_deck = self.instance.deck_elevation_wave_in_deck

        if deck_elevation_wave_in_deck.cellar_deck_height is not None:
            clof_71 = (
                    deck_elevation_wave_in_deck.cellar_deck_height
                    - (
                            deck_elevation_wave_in_deck.maximum_wave_height_10_years
                            * deck_elevation_wave_in_deck.crest_height_factor
                    )
                    - deck_elevation_wave_in_deck.storm_surge_10_years
                    - deck_elevation_wave_in_deck.highest_astronomical_tide
            )
            clof_72 = (
                    deck_elevation_wave_in_deck.cellar_deck_height
                    - (
                            deck_elevation_wave_in_deck.maximum_wave_height_100_years
                            * deck_elevation_wave_in_deck.crest_height_factor
                    )
                    - deck_elevation_wave_in_deck.storm_surge_100_years
                    - deck_elevation_wave_in_deck.highest_astronomical_tide
            )
            clof_73 = (
                    deck_elevation_wave_in_deck.cellar_deck_height
                    - (
                            deck_elevation_wave_in_deck.maximum_wave_height_10000_years
                            * deck_elevation_wave_in_deck.crest_height_factor
                    )
                    - deck_elevation_wave_in_deck.storm_surge_10000_years
                    - deck_elevation_wave_in_deck.highest_astronomical_tide
            )

            if clof_71 >= 0:
                if clof_72 >= 0:
                    if clof_73 >= 0:
                        clof_74 = self.wid_l
                    else:
                        clof_74 = 0
                else:
                    clof_74 = self.wid_m
            else:
                clof_74 = self.wid_h

        else:
            clof_74 = 5

        clof_75 = self.instance.framing_score

        clof_76 = ((clof_74 * clof_75) / Decimal(10)).quantize(1, ROUND_HALF_UP)

        clof_77 = clof_76 * self.w_wid

        return clof_77


class AdditionalAppurtenanceScoreCalculator(BaseCalculator):
    override_applied = True
    score_max = Decimal(50)
    score_min = Decimal(0)

    aa_h = Decimal(0)

    aa_lvl = Decimal(2)
    aa_mvl = Decimal(0)
    aa_hvl = Decimal(0)

    aa_ll = Decimal(4)
    aa_ml = Decimal(0)
    aa_hl = Decimal(0)

    aa_lm = Decimal(6)
    aa_mm = Decimal(0)
    aa_hm = Decimal(0)

    aa_lh = Decimal(8)
    aa_mh = Decimal(0)
    aa_hh = Decimal(0)

    aa_lvh = Decimal(10)
    aa_mvh = Decimal(0)
    aa_hvh = Decimal(0)

    w_aa = Decimal(5)

    def _calculate(self):
        additional_appurtenance = self.instance.additional_appurtenance

        clof_78 = (
                additional_appurtenance.number_of_additional_risers
                + additional_appurtenance.number_of_additional_caissons
                + additional_appurtenance.number_of_additional_conductors
        )

        clof_79 = (
                additional_appurtenance.number_of_design_risers
                + additional_appurtenance.number_of_design_caissons
                + additional_appurtenance.number_of_design_conductors
        )

        if clof_78 > 0:
            if clof_79 > 10:
                if clof_79 > 20:
                    if clof_78 < 3:
                        clof_80 = self.aa_hvl
                    elif clof_78 < 5:
                        clof_80 = self.aa_hl
                    elif clof_78 < 7:
                        clof_80 = self.aa_hm
                    elif clof_78 < 9:
                        clof_80 = self.aa_hh
                    else:
                        clof_80 = self.aa_hvh
                else:
                    if clof_78 < 3:
                        clof_80 = self.aa_mvl
                    elif clof_78 < 5:
                        clof_80 = self.aa_ml
                    elif clof_78 < 7:
                        clof_80 = self.aa_mm
                    elif clof_78 < 9:
                        clof_80 = self.aa_mh
                    else:
                        clof_80 = self.aa_mvh
            else:
                if clof_78 < 3:
                    clof_80 = self.aa_lvl
                elif clof_78 < 5:
                    clof_80 = self.aa_ll
                elif clof_78 < 7:
                    clof_80 = self.aa_lm
                elif clof_78 < 9:
                    clof_80 = self.aa_lh
                else:
                    clof_80 = self.aa_lvh

        else:
            clof_80 = self.aa_h

        clof_81 = clof_80 * self.w_aa

        return clof_81


class FatigueLoadScoreCalculator(BaseCalculator):
    score_min = Decimal(0)
    score_max = Decimal(10)

    w_ft = Decimal(1)

    ft_ehh = Decimal(10)
    ft_ehl = Decimal(6)
    ft_mhh = Decimal(4)
    ft_mhl = Decimal(2)

    ft_elh = Decimal(6)
    ft_ell = Decimal(4)
    ft_mlh = Decimal(2)
    ft_mll = Decimal(1)

    def _calculate(self):
        try:
            clof_82 = self.instance.design_date.year
        except AttributeError:
            clof_82 = self.instance.platform_installation_date.year - 2

        fatigue_load = self.instance.fatigue_load

        if clof_82 < 1979:
            if clof_82 < 1972:
                if fatigue_load.water_depth > 30:
                    if fatigue_load.platform_with_conductor_guide_frame:
                        clof_83 = self.ft_ehh
                    else:
                        clof_83 = self.ft_elh
                else:
                    if fatigue_load.platform_with_conductor_guide_frame:
                        clof_83 = self.ft_ehl
                    else:
                        clof_83 = self.ft_ell
            else:
                if fatigue_load.water_depth > 30:
                    if fatigue_load.platform_with_conductor_guide_frame:
                        clof_83 = self.ft_mhh
                    else:
                        clof_83 = self.ft_mlh
                else:
                    if fatigue_load.platform_with_conductor_guide_frame:
                        clof_83 = self.ft_mhl
                    else:
                        clof_83 = self.ft_mll

        else:
            clof_83 = 0

        clof_84 = clof_83 * self.w_ft

        return clof_84


class EnvironmentalConsequenceCategoryCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def calculate(self):
        environmental_consequence = self.instance.environmental_consequence

        if environmental_consequence.daily_oil_production == 0:
            return

        if (environmental_consequence.oil_price or 0) == 0:
            return

        clof_91 = (
                environmental_consequence.estimated_fraction_of_oil_production_loss_due_to_leakage
                * environmental_consequence.daily_oil_production
        )

        clof_92 = environmental_consequence.fixed_cost_for_spill_cleanup + (
                environmental_consequence.variable_cost_for_spill_cleanup * clof_91
        )
        return Decimal(clof_92) / environmental_consequence.oil_price
        # return Decimal(3)

class CalculatedEconmicImpactConsequenceCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        economic_impact_consequence = self.instance.economic_impact_consequence
        environmental_consequence = self.instance.environmental_consequence
        corrosion = self.instance.corrosion
        
        ilof_74 = economic_impact_consequence.platform_replacement_cost
        ilof_75 = economic_impact_consequence.platform_replacement_time
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        ilof_65=0
        if environmental_consequence.daily_oil_production:
            ilof_65 = environmental_consequence.daily_oil_production
        
        ilof_69=0
        if environmental_consequence.oil_price:
            ilof_69 = environmental_consequence.oil_price

        ilof_70=0
        if economic_impact_consequence.daily_gas_production:
            ilof_70 = economic_impact_consequence.daily_gas_production

        ilof_71=0 
        if economic_impact_consequence.gas_price:
            ilof_71 = economic_impact_consequence.gas_price

        clof_95 = Decimal(((ilof_65 * ilof_69 ) + (ilof_70 * ilof_71)))

        clof_95 = round(clof_95,2)
        
        clof_100 = ilof_74 + (clof_95 * ilof_73 * ilof_75)
        clof_100 = round(clof_100, 3)

        ilof_12 = self.instance.rbui_assessment_date.year
        ilof_3 = self.instance.platform_installation_date.year

        clof_96 = ilof_12-ilof_3

        ilof_17 = corrosion.platform_design_life

        clof_97 = int(ilof_17 - clof_96)
        ilof_72 = economic_impact_consequence.discount_date_for_interrupted_production
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        clof_98 = clof_95 * 365 * (1/(1+ilof_72))

        clof_99 = clof_98 * ilof_73
        clof_99 = round(clof_99,2)


        if clof_99 > clof_100:
            clof_101 = clof_100/1000000
        else:
            clof_101 = clof_100/1000000

        return clof_101

class CalculateEconomicImpactRemainingLifeServicesCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        economic_impact_consequence = self.instance.economic_impact_consequence
        environmental_consequence = self.instance.environmental_consequence
        corrosion = self.instance.corrosion
        
        ilof_74 = economic_impact_consequence.platform_replacement_cost
        ilof_75 = economic_impact_consequence.platform_replacement_time
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        ilof_65=0
        if environmental_consequence.daily_oil_production:
            ilof_65 = environmental_consequence.daily_oil_production
        
        ilof_69=0
        if environmental_consequence.oil_price:
            ilof_69 = environmental_consequence.oil_price

        ilof_70=0
        if economic_impact_consequence.daily_gas_production:
            ilof_70 = economic_impact_consequence.daily_gas_production

        ilof_71=0 
        if economic_impact_consequence.gas_price:
            ilof_71 = economic_impact_consequence.gas_price

        clof_95 = Decimal(((ilof_65 * ilof_69 ) + (ilof_70 * ilof_71)))

        clof_95 = round(clof_95,2)
        
        clof_100 = ilof_74 + (clof_95 * ilof_73 * ilof_75)
        clof_100 = round(clof_100, 3)

        ilof_12 = self.instance.rbui_assessment_date.year
        ilof_3 = self.instance.platform_installation_date.year

        clof_96 = ilof_12-ilof_3

        ilof_17 = corrosion.platform_design_life

        clof_97 = int(ilof_17 - clof_96)
        ilof_72 = economic_impact_consequence.discount_date_for_interrupted_production
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        clof_98 = clof_95 * 365 * (1/(1+ilof_72))

        clof_99 = clof_98 * ilof_73
        clof_99 = round(clof_99,2)


        if clof_99 > clof_100:
            clof_101 = clof_100/1000000
        else:
            clof_101 = clof_100/1000000

        if clof_97 <= 0:
            clof_102 = 0
        else:
            clof_102 = clof_101
        
        return clof_102

class StructureReplacementDecisionCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        economic_impact_consequence = self.instance.economic_impact_consequence
        environmental_consequence = self.instance.environmental_consequence
        corrosion = self.instance.corrosion
        
        ilof_74 = economic_impact_consequence.platform_replacement_cost
        ilof_75 = economic_impact_consequence.platform_replacement_time
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        ilof_65=0
        if environmental_consequence.daily_oil_production:
            ilof_65 = environmental_consequence.daily_oil_production
        
        ilof_69=0
        if environmental_consequence.oil_price:
            ilof_69 = environmental_consequence.oil_price

        ilof_70=0
        if economic_impact_consequence.daily_gas_production:
            ilof_70 = economic_impact_consequence.daily_gas_production

        ilof_71=0 
        if economic_impact_consequence.gas_price:
            ilof_71 = economic_impact_consequence.gas_price

        clof_95 = Decimal(((ilof_65 * ilof_69 ) + (ilof_70 * ilof_71)))

        clof_95 = round(clof_95,2)
        
        clof_100 = ilof_74 + (clof_95 * ilof_73 * ilof_75)
        clof_100 = round(clof_100, 3)

        ilof_12 = self.instance.rbui_assessment_date.year
        ilof_3 = self.instance.platform_installation_date.year

        clof_96 = ilof_12-ilof_3

        ilof_17 = corrosion.platform_design_life

        clof_97 = int(ilof_17 - clof_96)
        ilof_72 = economic_impact_consequence.discount_date_for_interrupted_production
        ilof_73 = economic_impact_consequence.fraction_of_remaining_production_loss

        clof_98 = clof_95 * 365 * (1/(1+ilof_72))

        clof_99 = clof_98 * ilof_73
        clof_99 = round(clof_99,2)

        if clof_99 > clof_100:
            return True
        else:
            return False

class FinalConsequenceCategoryCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        try:
            clof_90 = self.instance.platform_manned_status.ranking
        except:
            return None

        clof_94 = self.instance.environmental_consequence_category
        clof_104 = self.instance.economic_consequence_category
        if clof_90 is None and clof_94 is None and clof_104 is None:
            return

        if clof_90 is None:
            clof_90 = 'A'
        if clof_94 is None:
            clof_94 = 'A'
        if clof_104 is None:
            clof_104 = 'A'

        #clof_105
        if clof_104 > clof_90 and clof_104 > clof_94:
            return clof_104
        elif clof_94 > clof_90:
            return clof_94
        else:
            return clof_90

class ExposureCategoryLevelCalculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        clof_105 = FinalConsequenceCategoryCalculator(self.instance)._calculate()
        try:
            clof_90 = self.instance.platform_manned_status.ranking
        except:
            return None
        clof_108=None
        if clof_90 == 'E' or clof_90 == 'D':
            clof_108 = 'L-1'
        elif clof_90 == 'C':
            if clof_105 == 'E' or clof_105 == 'D':
                clof_108 = 'L-1'
            else:
                clof_108 = 'L-2'
        elif clof_90 == 'A' or clof_90 == 'B':
            if clof_105 == 'E' or clof_105 == 'D':
                clof_108 = 'L-1'
            elif clof_105 == 'C':
                clof_108 = 'L-2'
            elif clof_105 == 'B' or clof_105 == 'A':
                clof_108 = 'L-3'

        return clof_108

class ExposureCategorySurveyLevel1Calculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        clof_108 = ExposureCategoryLevelCalculator(self.instance)._calculate()
        clof_109 = '1'
        return clof_109

class ExposureCategorySurveyLevel2Calculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        clof_108 = ExposureCategoryLevelCalculator(self.instance)._calculate()
        clof_109=None
        if clof_108 == 'L-1':
            clof_109 = '3-5'
        elif clof_108 == 'L-2':
            clof_109 = '5-10'
        elif clof_108 == 'L-3':
            clof_109 = '5-10'
        return clof_109

class ExposureCategorySurveyLevel3Calculator:
    instance: Platform

    def __init__(self, instance: Platform):
        self.instance = instance

    def _calculate(self):
        clof_108 = ExposureCategoryLevelCalculator(self.instance)._calculate()
        clof_109=None
        if clof_108 == 'L-1':
            clof_109 = '6-10'
        elif clof_108 == 'L-2':
            clof_109 = '11-15'
        elif clof_108 == 'L-3':
            clof_109 = '11-15'
        return clof_109

# class RiskRankingCalculator:
#     instance: Platform

#     def __init__(self, instance: Platform):
#         self.instance = instance

#     def _calculate(self):
#         clof_88 = RiskBasedUnderwaterIntervalScoreCalculator(self.instance)._calculate()
#         clof_105 = FinalConsequenceCategoryCalculator(self.instance)._calculate()

#         if clof_105 == "A":
#             if clof_88 == 1 or clof_88 == 2:
#                 clof_106 = 'VL'
#             elif clof_88 == 3 or clof_88 == 4:
#                 clof_106 = 'L'
#             elif clof_88 == 5:
#                 clof_106 = 'M'
        
#         elif clof_105 == "B":
#             if clof_88 == 1:
#                 clof_106 = 'VL'
#             elif clof_88 == 2 or clof_88 == 3:
#                 clof_106 = 'L'
#             elif clof_88 == 4:
#                 clof_106 = 'M'
#             elif clof_88 == 5:
#                 clof_106 = 'H'
        
#         elif clof_105 == "C":
#             if clof_88 == 1 or clof_88 == 2:
#                 clof_106 = 'L'
#             elif clof_88 == 3:
#                 clof_106 = 'M'
#             elif clof_88 == 4 or clof_88 == 5:
#                 clof_106 = 'H'
        
#         elif clof_105 == "D":
#             if clof_88 == 1:
#                 clof_106 = 'L'
#             elif clof_88 == 2:
#                 clof_106 = 'M'
#             elif clof_88 == 3 or clof_88 == 4:
#                 clof_106 = 'H'
#             elif clof_88 == 5:
#                 clof_106 = 'VH'
        
#         elif clof_105 == "E":
#             if clof_88 == 1:
#                 clof_106 = 'M'
#             elif clof_88 == 2 or clof_88 == 3:
#                 clof_106 = 'H'
#             elif clof_88 == 4 or clof_88 == 5:
#                 clof_106 = 'VH'

#         return clof_106

# class RiskBasedUnderwaterIntervalScoreCalculator:
#     instance: Platform

#     def __init__(self, instance: Platform):
#         self.instance = instance

#     def _calculate(self):
#         # clof_106 = RiskRankingCalculator(self.instance)._calculate()

#         # if clof_106 == 'VL':
#         #     clof_107 = 12
#         # if clof_106 == 'L':
#         #     clof_107 = 10
#         # if clof_106 == 'M':
#         #     clof_107 = 7
#         # if clof_106 == 'H':
#         #     clof_107 = 5
#         # if clof_106 == 'VH':
#         #     clof_107 = 3
#         return Decimal(3)


import importlib

import calliope
import calliope_pathways
import plotly.express as px

# Set Variables
calliope.set_log_verbosity("INFO", include_solver_output=False)
modelurl = (
    importlib.resources.files("calliope_pathways")
    / "model_configs"
    / "roi_wind_focus"
    / "model.yaml"
)

"""
    "scenario_I_planned_development",
    "scenario_II-I_default_lw",
    "scenario_II-II_default_mw",
    "scenario_II-III_default_hw",
    "scenario_III-I_carbon_budget_lw",
    "scenario_III-II_carbon_budget_mw",
    "scenario_III-III_carbon_budget_hw",
    "scenario_IV-I_enhanced_bio_lw",
    "scenario_IV-II_enhanced_bio_mw",
    "scenario_IV-III_enhanced_bio_hw",
    "scenario_V-I_novel_techs_lw",
    "scenario_V-II_novel_techs_mw",
    "scenario_V-III_novel_techs_hw",
    "scenario_VI-I_inc_demand_lw",
    "scenario_VI-II_inc_demand_mw",
    "scenario_VI-III_inc_demand_hw",
    "scenario_VII-I_no_more_storage_lw",
    "scenario_VII-II_no_more_storage_mw",
    "scenario_VII-III_no_more_storage_hw",
    "sensitivity_I-I_CAPEX_lw",
    "sensitivity_I-II_CAPEX_mw",
    "sensitivity_I-III_CAPEX_hw",
    "sensitivity_II-I_offshore_wind_adv_lw",
    "sensitivity_II-II_offshore_wind_adv_mw",
    "sensitivity_II-III_offshore_wind_adv_hw",
    "sensitivity_III-I_offshore_wind_disadv_lw",
    "sensitivity_III-II_offshore_wind_disadv_mw",
    "sensitivity_III-III_offshore_wind_disadv_hw"


    "scenario_I_planned_development",
    "scenario_V-I_novel_techs_lw",
    "scenario_V-II_novel_techs_mw",
    "scenario_V-III_novel_techs_hw",
    "scenario_VII-I_no_more_storage_lw",
    "scenario_VII-II_no_more_storage_mw",
    "scenario_VII-III_no_more_storage_hw",
    "sensitivity_I-I_CAPEX_lw",
    "sensitivity_I-II_CAPEX_mw",
    "sensitivity_I-III_CAPEX_hw"
    """
scenario_list = [
    "scenario_IV-I_enhanced_bio_lw",
    "scenario_IV-II_enhanced_bio_mw",
    "scenario_IV-III_enhanced_bio_hw",
    "scenario_V-I_novel_techs_lw",
    "scenario_V-II_novel_techs_mw",
    "scenario_V-III_novel_techs_hw",
    "scenario_VI-I_inc_demand_lw",
    "scenario_VI-II_inc_demand_mw",
    "scenario_VI-III_inc_demand_hw",
    "scenario_VII-I_no_more_storage_lw",
    "scenario_VII-II_no_more_storage_mw",
    "scenario_VII-III_no_more_storage_hw",
    "sensitivity_I-I_CAPEX_lw",
    "sensitivity_I-II_CAPEX_mw",
    "sensitivity_I-III_CAPEX_hw",
    "sensitivity_II-I_offshore_wind_adv_lw",
    "sensitivity_II-II_offshore_wind_adv_mw",
    "sensitivity_II-III_offshore_wind_adv_hw",
    "sensitivity_III-I_offshore_wind_disadv_lw",
    "sensitivity_III-II_offshore_wind_disadv_mw",
    "sensitivity_III-III_offshore_wind_disadv_hw"
    ]

# Run Model
for scenario in scenario_list:
    model = calliope_pathways.models.load(modelurl,scenario=scenario)
    fname = scenario + "_3h.nc"
    resultsurl = (
        importlib.resources.files("calliope_pathways")
        / "model_configs"
        / "roi_wind_focus"
        / "model_results_III"
        / fname
    ) 
    model.build()
    model.solve()
    model.to_netcdf(resultsurl)
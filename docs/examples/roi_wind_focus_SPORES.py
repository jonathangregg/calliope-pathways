"""
Date: 06/08/2024
Author: Jonathan Gregg
Description: SPORES setup for RoI model (heavily based on fl SPORES for italy)
"""

import calliope
import calliope_pathways
import plotly.express as px
import xarray as xr

spores_dict = {}  # dictionary to collect SPORES designs as they get generated
#modelurl = "C:/Users/jdg57/calliope-pathways/src/calliope_pathways/model_configs/national_scale_SPORES/model.yaml"
modelurl = "C:/Users/jdg57/calliope-pathways/src/calliope_pathways/model_configs/roi_wind_focus/model.yaml"
#scenario = "new_spores"
scenario = "spores"
# Loading model files and building the model
calliope.set_log_verbosity("INFO", include_solver_output=False)
model = calliope_pathways.models.load(modelurl,scenario=scenario)
model.build()

# Solving
model.solve()

# Extracting SPORES-relevant data
least_feasible_cost = model.results.cost.loc[{"costs": "monetary"}].sum().sum()

# Storing model results for subsequent iterations
spores_dict[0] = model.results

# %%
# INITIALISING the SPORES mode:
# 1) Updating the slack cost constraint with an actual value
# 2) Change problem objective
# 3) Selection/definition of a scoring method
##

## STEP 1
# Check out the current slack cost constraint in the model (should be .inf in the first iteration)
model.backend.get_constraint(
    "total_system_cost_max", as_backend_objs=False
)  # .to_series().dropna()

# Update the backend parameter accordingly
model.backend.update_parameter("spores_cost_max", least_feasible_cost)

# Check again the backend model to see whether the slack cost constraint's upper bound changed as expected
model.backend.get_constraint(
    "total_system_cost_max", as_backend_objs=False
)  # .to_series().dropna()

## STEP 2
# Check out the current objective weights (should be 'monetary': 1 and 'spores_score': 0, initially)
model.backend.get_parameter(
    "objective_cost_weights", as_backend_objs=False
)  # .to_series().dropna()


# Update the objective_cost_weights
model.backend.update_parameter(
    "objective_cost_weights", model.inputs.spores_objective_cost_weights
)

# Check again the objective weights (should be 'monetary': 0 and 'spores_score': 1)
model.backend.get_parameter(
    "objective_cost_weights", as_backend_objs=False
)  # .to_series().dropna()

## STEP 3
# Definition of a scoring method to use


def scoring_integer(results, backend):
    spores_techs = backend.inputs["spores_tracker"].notnull()
    previous_cap = results.flow_cap
    min_relevant_size = 0.5 * previous_cap.where(spores_techs).max(
        ["nodes", "carriers"]
    )
    new_score = previous_cap.copy()
    new_score = new_score.where(spores_techs, other=0)
    new_score = new_score.where(new_score > min_relevant_size, other=0)
    new_score = new_score.where(new_score == 0, other=1000)
    new_score.rename("cost_flow_cap")
    new_score = new_score.expand_dims(costs=["spores_score"])
    # TODO: work out how to handle multiple carriers (e.g. having a CHP facility that has a cost associated with both heat and electricity capacity)
    # For now I'll just sum it as we know there's only one value
    new_score = new_score.sum("carriers")
    all_costs = backend.get_parameter("cost_flow_cap", as_backend_objs=False)
    new_all_costs = all_costs + new_score.fillna(0)

    return new_all_costs


# %%
# SPORES run
###

spores = []
scores = []
previous_spore_counter = 0

for i in range(previous_spore_counter, previous_spore_counter + 5):
    # Calculate weights based on a scoring method
    spores_score = scoring_integer(model.results, model.backend)
    # Check out the current SPORES score in the model (should be 0 in the first iteration)
    model.backend.get_parameter(
        "cost_flow_cap", as_backend_objs=False
    ).to_series().dropna()

    # Assign new score based on the calculated weights
    model.backend.update_parameter(
        "cost_flow_cap", spores_score.reindex_like(model.inputs.cost_flow_cap)
    )

    # # Check again the backend model to see whether the SPORES score has changed as expected
    model.backend.verbose_strings()
    model.backend.to_lp(f"{i}.txt")
    model.solve(force=True)
    spores.append(model.results.expand_dims(spores=[i]))
    scores.append(
        model.backend.get_parameter("cost_flow_cap", as_backend_objs=False)
        .sel(costs="spores_score")
        .expand_dims(spores=[i])
    )

    previous_spore_counter += 1
spore_ds = xr.concat(spores, dim="spores")
score_da = xr.concat(scores, dim="spores")
# %%
# Post-processing of results
###

print(spore_ds.flow_cap.diff("spores").to_series().dropna().unstack("spores"))
print(score_da.to_series().dropna())

# %%
import matplotlib.pyplot as plt
#
ax = plt.subplot(111)
#
spore_ds.flow_cap.sel(spores=498, carriers="electricity",investsteps="2050",nodes="LEI").where(
    model.inputs.spores_tracker
).dropna("techs").to_pandas().fillna(0).plot.bar(
    ax=ax, ylabel="Capacity (kW)", ylim=[0, 2000000]
)
plt.show()

#spores_dict[1].flow_cap.sel(carriers='power', techs=cool_techs).to_pandas().fillna(0).plot.bar(ax=ax, xticks=[k -0.5 for k in # xticks])

import importlib

import calliope
import plotly.express as px

# Set Variables
modelurl = (
    importlib.resources.files("calliope_pathways")
    / "model_configs"
    / "roi_wind_focus"
    / "model.yaml"
)


scenario = "scenario_II-II_default_mw"

fname = scenario + "_3h.nc"
resultsurl = (
    importlib.resources.files("calliope_pathways")
    / "model_configs"
    / "roi_wind_focus"
    / "model_results_Final"
    / fname
)

# Set up model
calliope.set_log_verbosity("INFO", include_solver_output=False)
model = calliope.read_netcdf(resultsurl)
#mone = model.results.costs.sel(costs='monetary')
#sum = mone.count()
#print(sum)
#x = sum(mone.values())


filter1 = model.results.techs != "demand_electricity" 
filter2 = model.results.techs != "demand_electrified_transport" 
filter3 = model.results.techs != "demand_electrified_heat"

df_capacity = (
    model.results.storage_cap.sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("Storage capacity (kWh)")
    .reset_index()
)

fig = px.bar(
    df_capacity,
    x="investsteps",
    y="Storage capacity (kWh)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
    barmode='stack'
)

# Plot Figure


fig.update_layout(
    xaxis_title={'text': 'Investsteps', 'font': {'size': 26}},
    yaxis_title={'text': 'Storage Capacity (kWh)', 'font': {'size': 26}},
    xaxis={'tickfont': {'size': 18}},
    yaxis={'tickfont': {'size': 18}},
    legend={'font': {'size': 26}}
)
#fig.update_layout(margin=dict(l=0, r=0, t=20, b=20))
fig.show()

"""
df_outflow = (
    (model.results.flow_out.fillna(0) - model.results.flow_in.fillna(0))
    .sel(carriers="electricity")
    .sum(["nodes", "timesteps"], min_count=1)
    .to_series()
    .where(lambda x: x > 1)
    .dropna()
    .to_frame("Annual outflow (kWh)")
    .reset_index()
)

fig = px.bar(
    df_outflow,
    x="investsteps",
    y="Annual outflow (kWh)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
    barmode='stack'
)
filter1 = model.results.techs != "demand_electricity" 
filter2 = model.results.techs != "demand_electrified_transport" 
filter3 = model.results.techs != "demand_electrified_heat"
# Plot Figure

# Plot Figure
df_capacity = (
    model.results.flow_cap_new.where(filter1 & filter2 & filter3)
    .sel(carriers="electricity")
    .sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("New flow capacity (kW)")
    .reset_index()
)

fig = px.bar(
    df_capacity,
    x="vintagesteps",
    y="New flow capacity (kW)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
    barmode='stack'
)
fig.update_layout(bargap=0,width=800)
fig.update_layout(margin=dict(l=0, r=0, t=20, b=20))
fig.show()

df_capacity = (
    model.results.flow_cap.where(filter1 & filter2 & filter3)
    .sel(carriers="electricity")
    .sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("Flow capacity (kW)")
    .reset_index()
)

print(df_capacity.head())

fig = px.bar(
    df_capacity,
    x="investsteps",
    y="Flow capacity (kW)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
    barmode='stack'
)
fig.update_layout(bargap=0.05,width=800)
fig.update_layout(margin=dict(l=0, r=0, t=20, b=20))
fig.show()

df_capacity = (
    model.results.storage_cap.sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("Storage capacity (kWh)")
    .reset_index()
)

print(df_capacity.head())

fig = px.bar(
    df_capacity,
    x="investsteps",
    y="Storage capacity (kWh)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
    barmode='stack'
)
fig.update_layout(bargap=0,width=800)
fig.update_layout(margin=dict(l=0, r=0, t=20, b=20))
fig.show()

df_electricity = (
    (model.results.flow_out.fillna(0) - model.results.flow_in.fillna(0))
    .sel(carriers="electricity")
    .sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("Flow in/out (kWh)")
    .reset_index()
)
df_electricity_demand = df_electricity[df_electricity.techs == "demand_electricity"]
df_electricity_other = df_electricity[df_electricity.techs != "demand_electricity"]

invest_order = sorted(df_electricity.investsteps.unique())

fig = px.bar(
    df_electricity_other,
    x="timesteps",
    y="Flow in/out (kWh)",
    facet_row="investsteps",
    color="techs",
    height=1000,
    category_orders={"investsteps": invest_order},
    color_discrete_map=model.inputs.color.to_series().to_dict(),
)

showlegend = True
# we reverse the investment year order (`[::-1]`) because the rows are numbered from bottom to top.
for row, year in enumerate(invest_order[::-1]):
    demand_ = df_electricity_demand.loc[(df_electricity_demand.investsteps == year)]
    fig.add_scatter(
        x=demand_["timesteps"],
        y=-1 * demand_["Flow in/out (kWh)"],
        row=row + 1,
        col="all",
        marker_color="black",
        name="Demand",
        legendgroup="demand",
        showlegend=showlegend,
    )
    showlegend = False
fig.update_yaxes(matches=None)
fig.show()

"""
import importlib

import calliope
import calliope_pathways
import plotly.express as px

# Set Variables
modelurl = (
    importlib.resources.files("calliope_pathways")
    / "model_configs"
    / "roi_wind_focus"
    / "model.yaml"
)

# Set up model
calliope.set_log_verbosity("INFO", include_solver_output=False)
model = calliope_pathways.models.load(modelurl)

# Run Model
model.build()
model.solve()

# Plot Figure
df_capacity = (
    model.results.flow_cap_new.where(model.results.techs != "demand_electricity")
    .sel(carriers="electricity")
    .sum("nodes")
    .to_series()
    .where(lambda x: x != 0)
    .dropna()
    .to_frame("New flow capacity (kW)")
    .reset_index()
)

print(df_capacity.head())

fig = px.bar(
    df_capacity,
    x="vintagesteps",
    y="New flow capacity (kW)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
)
fig.show()

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

print(df_capacity.head())

fig = px.bar(
    df_outflow,
    x="investsteps",
    y="Annual outflow (kWh)",
    color="techs",
    color_discrete_map=model.inputs.color.to_series().to_dict(),
)
df_demand = (
    model.results.flow_in.sel(techs="demand_electricity", carriers="electricity")
    .sum(["nodes", "timesteps"])
    .to_series()
    .reset_index()
)
fig.add_scatter(
    x=df_demand.investsteps, y=df_demand.flow_in, line={"color": "black"}, name="Demand"
)
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

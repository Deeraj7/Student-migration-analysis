import altair as alt
import pandas as pd

# Read in your data table as a pandas dataframe
df = pd.read_csv("https://gist.githubusercontent.com/karthikRachamalli1995/b6f1caac97e22f0d4328443f24c8f393/raw/6ff1bdbaf5dadc975726d3fe9cc3bc5e7033175a/gdp_inflation_loss.csv")

brush = alt.selection_interval(resolve='global')

# Create a gdp scatter plot with Altair
gdp = alt.Chart(df).mark_circle().encode(
    x=alt.X('current_gdp', axis=alt.Axis(
        title='Current GDP in USD', labelAngle=0)),
    y=alt.Y('projected_gdp:Q', title='Projected GDP in USD'),
    color=alt.condition(brush, 'country', alt.ColorValue('gray')),
    tooltip=['country', alt.Tooltip('current_gdp', title="Current GDP"), alt.Tooltip(
        'projected_gdp', title="Projected GDP")]
).add_params(
    brush
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        'Current vs Projected GDP of Countries', anchor='middle')
)

# Create a inflation scatter plot with Altair
inflation = alt.Chart(df).mark_circle().encode(
    x=alt.X('current_inflation', axis=alt.Axis(
        title='Current Inflation', labelAngle=0)),
    y=alt.Y('projected_inflation:Q', title='Projected Inflation'),
    color=alt.condition(brush, 'country', alt.ColorValue('gray')),
    tooltip=['country', alt.Tooltip('current_inflation', title="Current Inflation"), alt.Tooltip(
        'projected_inflation', title="Projected Inflation")]
).add_params(
    brush
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        'Current and Projected Inflation of Countries', anchor='middle')
)

chart = gdp & inflation

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('inflation.json', 'w') as f:
    f.write(chart_json)

import altair as alt
import pandas as pd

# Read in your data table as a pandas dataframe
migration_dataset = pd.read_csv(
    "https://gist.githubusercontent.com/karthikRachamalli1995/1eda9a6b78a79224ed6824798094f14f/raw/d7c60ef4433cede71bc318885c57e4e7d2048089/Student_migration_INC_2.csv")

# define the selection
country_selection = alt.selection_point(fields=['country'])

# Create a bar graph with Altiar
country = alt.Chart(migration_dataset).mark_bar().encode(
    x=alt.X('country', axis=alt.Axis(title='Country', labelAngle=0)),
    y=alt.Y('sum(gdp\:salary):Q', title='Loss of GDP in USD'),
    color=alt.condition(country_selection, 'country', alt.value('lightgray')),
    tooltip=['country', alt.Tooltip('gdp\:occupation', title="Occupation"), alt.Tooltip(
        'sum(gdp\:salary)', title="Salary")]
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        'Loss in GDP of various countries due to migration', anchor='middle')
).add_params(
    country_selection
)


# Create a stacked bar graph with Altiar
occupationChart = alt.Chart(migration_dataset).mark_bar().encode(
    x=alt.X('gdp\:occupation:N', axis=alt.Axis(
        title='Occupation', labelAngle=0)),
    y=alt.Y('sum(gdp\:salary)',
            title='Total Earned Money in Foriegn countries in USD'),
    color=alt.condition(country_selection, 'country', alt.value('lightgray')),
    tooltip=['country', alt.Tooltip('gdp\:occupation', title="Occupation"), alt.Tooltip(
        'sum(gdp\:salary)', title="Salary")]
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        'Money earned in various occupations by migrated students', anchor='middle')
).add_params(
    country_selection
)

# Combining the charts
chart = (country & occupationChart).configure_title(
    fontSize=25
)

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('gdp_loss.json', 'w') as f:
    f.write(chart_json)

import altair as alt
import pandas as pd

# Read in your data table as a pandas dataframe
migration_dataset = pd.read_csv(
    "https://gist.githubusercontent.com/karthikRachamalli1995/1eda9a6b78a79224ed6824798094f14f/raw/d7c60ef4433cede71bc318885c57e4e7d2048089/Student_migration_INC_2.csv")


# Create a bar graph with Altiar
chart = alt.Chart(migration_dataset).mark_bar().encode(
    x=alt.X('country', axis=alt.Axis(title='Country', labelAngle=0)),
    y=alt.Y('sum(willingness)', title='Willingness'),
    color='Education Level:N',
    tooltip=['Education Level:N', alt.Tooltip(
        'sum(willingness)', title="Willingness")]
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        'Students willing to move back to home country if all expectations are met', anchor='middle')
)

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('willingness.json', 'w') as f:
    f.write(chart_json)

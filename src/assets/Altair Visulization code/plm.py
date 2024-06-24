import altair as alt
import pandas as pd

# Read the Student migration dataset from csv format to dataframe
migration_dataset = pd.read_csv(
    "https://gist.githubusercontent.com/karthikRachamalli1995/f1e073a489ad98120c9f63cc0eb2e9bc/raw/cf495f3204325a4cde627040de5768f4d16b744f/student_migration_dataset.csv")

# Selecting the problems leading migration columns that starts with "plm:"
problem_leading_migration_columns = [
    col for col in migration_dataset.columns if col.startswith('plm:')]
# As it is a stacked bar graph, color stack of the bar is taken on country attribute.
color_column = 'country'

# Grouping the dataset based on country and summing the values of problems leading migration columns using Pivoting technique.
pivoted_data = pd.pivot_table(
    migration_dataset, values=problem_leading_migration_columns, index=color_column, aggfunc=sum).reset_index()

# Melt the data to get a long format
melted_data = pd.melt(pivoted_data, id_vars=color_column,
                      value_vars=problem_leading_migration_columns, var_name='plm', value_name='value')

# The below code, make the non-selected countries to light grey using selection_point API of Altair
country_selection = alt.selection_point(fields=['country'], bind='legend')
color = alt.condition(
    country_selection,
    alt.Color('country:N'),
    alt.value('lightgray')
)

# The below code will create a Stacked Bar Graph visulization which has:
# 'problems' on x-axis.
# 'intensity' on y-axis.
#  color to 'country' attribute with selection.
# mark_bar is the method used to generate Stacked Bar Graph visulization
chart = alt.Chart(melted_data).transform_calculate(plm='replace(datum.plm, "plm:", "")').mark_bar(size=70).encode(
    x=alt.X('plm:N', axis=alt.Axis(
        title='problems leading migration', labelAngle=0)),
    y=alt.Y('value:Q', axis=alt.Axis(title='Intensity')),
    color=color,
    # The below property tooltip generates the tooltip when user hovers on a point with repsective problem, intensity, and country attributes.
    tooltip=[alt.Tooltip('plm', title="problem"), alt.Tooltip(
        'value', title="Intensity"), 'country']
).properties(
    height=400,
    width=900,
    title='Problems Leading Migration of Students'
).add_params(
    country_selection  # adding country selection param
)

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('plm.json', 'w') as f:
    f.write(chart_json)

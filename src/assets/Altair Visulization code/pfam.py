import pandas as pd
import altair as alt

# Read the Student migration dataset from csv format to dataframe
migration_dataset = pd.read_csv(
    "https://gist.githubusercontent.com/karthikRachamalli1995/f1e073a489ad98120c9f63cc0eb2e9bc/raw/cf495f3204325a4cde627040de5768f4d16b744f/student_migration_dataset.csv")

# Selecting the problems leading migration columns that starts with "pfam:"
problem_faced_after_migration_columns = [
    col for col in migration_dataset.columns if col.startswith('pfam:')]
color_column = 'country'

# Grouping the dataset based on country and summing the values of problems faced after migration columns using Pivoting technique.
pivoted_data = pd.pivot_table(
    migration_dataset, values=problem_faced_after_migration_columns, index=color_column, aggfunc=sum).reset_index()

# Melt the data to get a long format
melted_data = pd.melt(pivoted_data, id_vars=color_column,
                      value_vars=problem_faced_after_migration_columns, var_name='pfam', value_name='value')

# create selection dropdown for country
country_select = alt.selection_point(
    name='Select', fields=['country'], bind=alt.binding_select(options=melted_data['country'].unique().tolist()), value='India'
)

# Added new attribute that trims the "pfam:" as prefix
melted_data['problem'] = melted_data['pfam'].apply(lambda x: x.split(":")[1])

# The below code will create a base chart with the encoding values.
base = alt.Chart(melted_data).encode(
    alt.Theta("value:Q", title="Intensity").stack(True),
    alt.Radius("value", title="Intensity").scale(
        type="sqrt", zero=True, rangeMin=20),
    color=alt.Color("problem:N", legend=alt.Legend(title="Problems")),
    tooltip=['problem', 'value', 'country']
).add_params(
    country_select
).transform_filter(
    country_select  # Filtering the radial chart based on country selection.
)

# The below code generates the chart.
c1 = base.mark_arc(innerRadius=5, stroke="#fff").encode(
    text=alt.Text("pfam:N")
)

# The below code generates the lables on the radial chart
c2 = base.mark_text(radiusOffset=50).encode(text="problem:N")

# The below code combine the radial chart and labels.
chart = (c1 + c2).configure_legend(
    orient='top-right',
    offset=-150,
    titleAlign='left',
    labelAlign='left'
).properties(
    title="Problems faced by Students after migration"
)

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('pfam.json', 'w') as f:
    f.write(chart_json)

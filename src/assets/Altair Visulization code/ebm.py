import altair as alt
import pandas as pd

# Read in your data table as a pandas dataframe
migration_dataset = pd.read_csv(
    "https://gist.githubusercontent.com/karthikRachamalli1995/f1e073a489ad98120c9f63cc0eb2e9bc/raw/bda0fc143c3a53ef8fa736b4d6f8f86ac7554b59/student_migration_dataset.csv")

# Selecting the problems leading migration columns that starts with "ebm:"
problem_faced_after_migration_columns = [
    col for col in migration_dataset.columns if col.startswith('ebm:')]
color_column = 'country'

# Grouping the dataset based on country and summing the values of expectations by migrators columns using Pivoting technique.
pivoted_data = pd.pivot_table(migration_dataset, values=problem_faced_after_migration_columns, index=[
                              color_column, 'gender', 'Education Level'], aggfunc=sum).reset_index()


# Melt the data to get a long format
melted_data = pd.melt(pivoted_data, id_vars=[color_column, 'gender', 'Education Level'],
                      value_vars=problem_faced_after_migration_columns, var_name='ebm', value_name='value')

# dividing the dataset into female and male datasets
female_data = melted_data.query('gender == "Female"')
male_data = melted_data.query('gender == "Male"')

# create selection dropdown for country
country_select_dropdown = alt.selection_point(
    name='Select', fields=['country'], bind=alt.binding_select(options=melted_data['country'].unique().tolist())
)

# The below code will generate the a grouped stacked bar graph for female students
female_chart = alt.Chart(female_data).transform_calculate(ebm='replace(datum.ebm, "ebm:", "")'
                                                          ).mark_bar().encode(
    x=alt.X('Education Level:N', axis=alt.Axis(title='Edu Level', labelAngle=-20)),
    y=alt.Y('value:Q', axis=alt.Axis(title='Intensity')),
    color='country',
    tooltip=[alt.Tooltip('ebm', title="Expectation"), alt.Tooltip('value', title="Intensity"), 'country', 'gender', 'Education Level'],
    column=alt.Column("ebm:N", title="Expectations")
).properties(
    width=100,
    title=alt.TitleParams(
        'Expectations by Female Students after Migration', anchor='middle')
).add_params(
    country_select_dropdown
).transform_filter(
    country_select_dropdown
)

# The below code will generate the a grouped stacked bar graph for male students
male_chart = alt.Chart(male_data).transform_calculate(ebm='replace(datum.ebm, "ebm:", "")'
                                                      ).mark_bar().encode(
    x=alt.X('Education Level:N', axis=alt.Axis(
        title='Edu Level', labelAngle=-20)),
    y=alt.Y('value:Q', axis=alt.Axis(title='Intensity')),
    color='country',
    tooltip=[alt.Tooltip('ebm', title="Expectation"), alt.Tooltip(
        'value', title="Intensity"), 'country', 'gender', 'Education Level'],
    column=alt.Column("ebm:N", title="Expectations")
).properties(
    width=100,
    title=alt.TitleParams(
        'Expectations by Male Students after Migration', anchor='middle')
).add_params(
    country_select_dropdown
).transform_filter(
    country_select_dropdown
)

#The below code will make the charts one after the other.
chart = (female_chart & male_chart).configure_title(
    fontSize=25
).interactive()

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('ebm.json', 'w') as f:
    f.write(chart_json)

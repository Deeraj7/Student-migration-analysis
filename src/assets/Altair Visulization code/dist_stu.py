import altair as alt
import pandas as pd

# Read the Student migration dataset from csv format to dataframe
data = pd.read_csv(
    'https://gist.githubusercontent.com/karthikRachamalli1995/892698eca918365a2dac1bff3ce6644f/raw/062a1c63d6959adbfd4e9f48a7c4e74a29fd4441/indian_student.csv')

# The below code generates a horizontal bar graph
chart = alt.Chart(data).mark_bar().encode(
    y=alt.Y('Country:O', sort='-x'),
    x=alt.X('No of Indian Students:Q'),
    tooltip=['Country', 'No of Indian Students']
).properties(
    title='Number of Indian Students in Different Countries'
)

# To convert the chart to JSON to host the chart in Angular App
chart_json = chart.to_json()

# The below code will write the above JSON to file.
with open('dist_stu.json', 'w') as f:
    f.write(chart_json)

import pandas as pd
from event_calplot import create_calendar_heatmap

# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', '2024-12-31'),
    'value': range(366)
})

# Create heatmap
fig = create_calendar_heatmap(
    data=df,
    date_col='date',
    value_col='value',
    year=2024
)
fig.write_image("quick_start.svg")

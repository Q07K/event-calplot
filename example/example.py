import numpy as np
import pandas as pd

from event_calplot import create_calendar_heatmap

# Create sample data
df = pd.DataFrame(
    data={
        "date": pd.date_range(start="2024-01-01", end="2024-12-31"),
        "value": np.random.randint(0, 100, size=366),
    }
)

# Event dates
event_dates = pd.to_datetime(
    arg=[
        "2024-01-01",
        "2024-02-14",
        "2024-03-01",
        "2024-10-03",
        "2024-10-09",
        "2024-12-25",
    ]
)

# Create heatmap
fig = create_calendar_heatmap(
    data=df,
    date_col="date",
    value_col="value",
    year=2024,
    min_color="#eff2f5",
    max_color="#116329",
    line_color="#cccccc",
    event_dates=event_dates,
    event_color="#b64f17",
)
fig.write_image("example.svg")
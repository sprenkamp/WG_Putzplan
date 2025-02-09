from datetime import date, timedelta
import streamlit as st
import pandas as pd
import numpy as np


# Utils
def get_future_date(dayname):
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    start_date = date.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_until = 35 + day_num + day_num_target

    return start_date + timedelta(days=days_until)


def highlight_current(styler, date):
    if styler.Start == date:
        return ["background-color: #8c4ce8"] * len(styler)
    else:
        return ["background-color: black"] * len(styler)


# Page setup
st.title("Grande Terrazza")
st.subheader("Putzplan")

# Parameter
start = pd.date_range(start="2025-02-02", end=get_future_date("Monday"), freq="W-MON")
end = pd.date_range(start="2025-02-09", end=get_future_date("Sunday"), freq="W")
people = ["Fabian", "Morley", "Melissa", "Kilian", "Jonny"]
cycles = len(end)
people_array = np.tile(people, 1000)[:cycles]

# Table contruction
overview = pd.DataFrame({"Start": start, "End": end, "Verantwortlich": people_array})
overview = overview.sort_values(by="Start", ascending=False).reset_index(drop=True)

# Table styling
today = pd.to_datetime(date.today())
this_week = overview.loc[
    (overview.Start <= today) & (overview.End >= today)
].Start.dt.date.values

overview = overview.assign(Start=overview.Start.dt.date, End=overview.End.dt.date)

st.dataframe(
    overview.style.apply(lambda x: highlight_current(x, this_week), axis=1)
)

from TaxiFareModel.data import get_data, clean_df
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 14
plt.figure(figsize=(12,5))
palette = sns.color_palette('Paired', 10)

def df_ny_box():
    df = get_data(nrows=10000)
    df = clean_df(df)
    #setting boundries
    df = df[df["pickup_latitude"].between(left = 40, right = 42 )]
    df = df[df["pickup_longitude"].between(left = -74.3, right = -72.9 )]
    df = df[df["dropoff_latitude"].between(left = 40, right = 42 )]
    df = df[df["dropoff_longitude"].between(left = -74, right = -72.9 )]
    return df

def folium_heat():
    df = df_ny_box()
    heatmap_data = df.head(10000)[['pickup_latitude', 'pickup_longitude', 'passenger_count']].groupby(['pickup_latitude', 'pickup_longitude']).sum().reset_index().values.tolist()

    center_location = [40.758896, -73.985130]
    m = folium.Map(location=center_location, control_scale=True, zoom_start=11)
    gradient = {0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}
    HeatMap(data=heatmap_data, radius=5, gradient=gradient, max_zoom=13).add_to(m)

    return m

def folium_moving():
    df = df_ny_box()
    timezone_name = 'America/New_York'
    time_column = "pickup_datetime"
    df.index = pd.to_datetime(df[time_column])
    df.index = df.index.tz_convert(timezone_name)
    df["dow"] = df.index.weekday
    df["hour"] = df.index.hour
    df["month"] = df.index.month
    df["year"] = df.index.year
    df.reset_index(drop=True)
    gradient = {0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}


    heatmap_data_by_hour = []
    __df__ = df.copy()
    for hour in df.hour.sort_values().unique():
        _df = __df__[__df__.hour == hour][['pickup_latitude', 'pickup_longitude', 'passenger_count']].groupby(['pickup_latitude', 'pickup_longitude']).sum().reset_index().values.tolist()
        heatmap_data_by_hour.append(_df)

    center_location = [40.758896, -73.985130]
    m2 = folium.Map(location=center_location, control_scale=True, zoom_start=11)
    HeatMapWithTime(heatmap_data_by_hour, radius=5,
                    gradient=gradient,
                    min_opacity=0.5, max_opacity=0.8,
                    use_local_extrema=False).add_to(m2)
    return m2


def fare_bins():
    df = df_ny_box()
    df['fare-bin'] = pd.cut(df['fare_amount'], bins = list(range(0, 50, 5))).astype(str)

    # Uppermost bin
    df.loc[df['fare-bin'] == 'nan', 'fare-bin'] = '[45+]'

    # Adjust bin so the sorting is correct
    df.loc[df['fare-bin'] == '(5, 10]', 'fare-bin'] = '(05, 10]'


    fig = sns.catplot(x="fare-bin", kind="count", palette=palette, data=df, height=5, aspect=3);
    sns.despine()
    return fig

def hour():
    df = df_ny_box()
    timezone_name = 'America/New_York'
    time_column = "pickup_datetime"
    df.index = pd.to_datetime(df[time_column])
    df.index = df.index.tz_convert(timezone_name)
    df["dow"] = df.index.weekday
    df["hour"] = df.index.hour
    df["month"] = df.index.month
    df["year"] = df.index.year
    df.reset_index(drop=True)

    fig = sns.catplot(x="hour", kind="count", palette=palette, data=df, height=5, aspect=3);
    sns.despine()
    plt.title('Hour of Day')

    return fig

def monthly_fare():
    df = df_ny_box()
    date_df = df.copy()

    date_df['pickup_datetime'] = pd.to_datetime(date_df['pickup_datetime'])
    date_df.set_index('pickup_datetime', inplace=True)
    monthly = date_df[["fare_amount"]].resample('M').mean()
    monthly["date"] = monthly.index
    

    fig = alt.Chart(monthly).mark_area(
        color="lightblue",
        interpolate='step-after',
        line=True
    ).encode(alt.Y('fare_amount', scale=alt.Scale(domain=(6, 15))),
        x='date',
    ).properties(width=630, height=400)
    return fig

if __name__ == "__main__":
    #df = read_data() 
    df = df_ny_box()


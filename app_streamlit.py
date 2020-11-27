from datetime import datetime
import joblib
import pandas as pd
import pytz
import streamlit as st
from TaxiFareModel.data import get_data
from TaxiFareModel.utils import geocoder_here
from TaxiFareModel.dataviz import folium_heat, folium_moving, fare_bins, monthly_fare, hour
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

COLS = ['key',
        'pickup_datetime',
        'pickup_longitude',
        'pickup_latitude',
        'dropoff_longitude',
        'dropoff_latitude',
        'passenger_count']


st.markdown("# ML Project")
st.markdown("**Taxifare data explorer**")

@st.cache
def read_data(n_rows=10000):
    df = get_data(n_rows=n_rows, local=False)
    return df


def format_input(pickup, dropoff, passengers=1):
    pickup_datetime = datetime.utcnow().replace(tzinfo=pytz.timezone('America/New_York'))
    formated_input = {
        "pickup_latitude": pickup["lat"],
        "pickup_longitude": pickup["lon"],
        "dropoff_latitude": dropoff["lat"],
        "dropoff_longitude": dropoff["lon"],
        "passenger_count": passengers,
        "pickup_datetime": str(pickup_datetime),
        "key": str(pickup_datetime)}

    return formated_input


def main():
    analysis = st.sidebar.selectbox("chose restitution", ["prediction", "Dataviz"])
    if analysis == "Dataviz":
        st.header("TaxiFare Basic Data Visualisation")
        m = folium_heat()
        m_move = folium_moving()

        st.subheader("Static view of number of taxirides in manhattan")
        folium_static(m)

        st.subheader("24hours of taxi rides in manhattan")
        folium_static(m_move)

        st.subheader("Average number of Taxi rides per hour of the day")
        st.pyplot(hour())

        st.subheader("Binned Fare amount count")
        st.pyplot(fare_bins())

        st.subheader("Monthly fare average from 2011 to 2017")
        st.write(monthly_fare())
     

    if analysis == "prediction":
        pipeline = joblib.load('data/model.joblib')
        st.header("TaxiFare Model predictions")
        # inputs from user
        pickup_adress = st.text_input("pickup adress", "251 Church St, New York, NY 10013")
        dropoff_adress = st.text_input("dropoff adress", "434 6th Ave, New York, NY 10011")
        # Get coords from input adresses usung HERE geocoder
        pickup_coords = geocoder_here(pickup_adress)
        dropoff_coords = geocoder_here(dropoff_adress)
        # inputs from user
        passenger_counts = st.selectbox("# passengers", [1, 2, 3, 4, 5, 6], 1)
        data = pd.DataFrame([pickup_coords, dropoff_coords])
        to_predict = [format_input(pickup=pickup_coords, dropoff=dropoff_coords, passengers=passenger_counts)]
        X = pd.DataFrame(to_predict)
        res = pipeline.predict(X[COLS])
        st.write("💸 taxi fare", res[0])
        st.map(data=data)


# print(colored(proc.sf_query, "blue"))
# proc.test_execute()
if __name__ == "__main__":
    #df = read_data()
    main()

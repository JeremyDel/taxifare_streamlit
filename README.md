# Streamlit

Very Simple setup with streamlit for the kaggle New-York dataset. You can find a nicer interface on my Github (Taxifare interface)

I included very simple visualisations made with folium, altair and seaborn.

# Introduction
For information on the dataset you can find it here on [Kaggle](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction)

# About the Taxifare model

Model running on the google cloud platform and with ML flow. Go check TaxiFareModel to check set the set up

## Setup
Before everything let us install the requirements provided inside `requirements.txt`
```bash
pip install -r requirements.txt
```
```bash
make install
```
Now run:
```bash
streamlit run app_streamlit.py
```
# Deploy on Heroku

There's a ProcFile included in order to deplot this simple app on Heroku.

# Useful links

- [Altair](https://altair-viz.github.io/gallery/)

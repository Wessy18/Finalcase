#!/usr/bin/env python
# coding: utf-8

# # Insight into American flights

# ## **Nikhil, Oskay, Wesley**

# # 1. Setup

# In[1]:


pip install streamlit


# In[ ]:


#These are all the packages we will be using for this project
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from IPython.display import display
import sklearn
from sklearn.linear_model import LinearRegression


# In[ ]:





# # 2. Data setup

# In[3]:


alldata = pd.read_csv('Airports2.csv')


# In[4]:


alldata.tail()


# In[5]:


alldata.info()


# In[6]:


alldata.describe()


# In[7]:


alldata.isna().sum()


# In[8]:


alldata.count()


# Visualisatie
# - kaart met daarop aantal vluchten die binnenkomen en weggaan (dmv een dropdown hoeveel vliegtuigen er komen en weggaan)
# 
# 

# In[9]:


#Changing Fly_date to a datatype
alldata['Fly_date'] = pd.to_datetime(alldata['Fly_date'])

# We only want the last 10 years of data
start_date = pd.to_datetime('1999-01-01')
end_date = pd.to_datetime('2009-12-31')

alldata['Fly_date'] = alldata['Fly_date'].dt.floor('D')

# Filtering the rows between te start and end date and assigning it to a new df
airportnew = alldata[(alldata['Fly_date'] >= start_date) & (alldata['Fly_date'] <= end_date)]



# In[10]:


airportnew.head()


# In[11]:


airportnew.isna().sum()


# In[16]:


# Assuming 'airportnew' is your DataFrame
airportnew.dropna(inplace=True)

# Create a new DataFrame without NaN values
airportnew = airportnew.dropna()


# In[17]:


#Dropping all the values where the Origin_airport is the same as Destination_airport
airportnew = airportnew[airportnew['Origin_airport'] != airportnew['Destination_airport']]


# In[18]:


#creating a new column loadfactor, this can be used to visualise how full a plane is
airportnew['Loadfactor'] = (airportnew['Passengers'] / airportnew['Seats'])


# In[19]:


#Dropping all records where the loadfactor is bigger than 1
airportnew = airportnew[airportnew['Loadfactor'] <= 1]


# In[ ]:


airportnew.tail()


# In[20]:


airportnew['Origin_airport'].nunique()


# In[21]:


unique_airports = airportnew['Origin_airport'].unique()

# Maak een lege lijst om de resultaten op te slaan
results = []

# Itereer over de unieke luchthavens en haal de breedtegraad en lengtegraad op
for airport in unique_airports:
    airport_data = airportnew.loc[airportnew['Origin_airport'] == airport].iloc[0]  # We nemen de gegevens van de eerste rij voor elke luchthaven
    latitude = airport_data['Org_airport_lat']
    longitude = airport_data['Org_airport_long']
    results.append({'Origin_airport': airport, 'Latitude': latitude, 'Longitude': longitude})

# Converteer de resultaten naar een DataFrame
airport_location_df = pd.DataFrame(results)

# Toon het aantal unieke luchthavens en de bijbehorende breedtegraad en lengtegraad
print("Aantal unieke luchthavens:", len(unique_airports))
print(airport_location_df)


# In[ ]:





# In[22]:


airportnew.head()


# # 3. Visualisations

# In[23]:


# Eerst, groepeer de gegevens op basis van het oorsprongsvliegveld (Origin_airport) en bereken de totale passagiers per vliegveld.
airportnew_grouped = airportnew.groupby('Origin_airport')['Passengers'].sum().reset_index()

# Sorteer de gegevens in aflopende volgorde op basis van het totale aantal passagiers en selecteer de top 5 vliegvelden.
top_5_airports = airportnew_grouped.sort_values(by='Passengers', ascending=False).head(5)

print(top_5_airports)


# In[ ]:





# In[24]:


import streamlit as st
import plotly.express as px

# Definieer de dataframe
airportnew = pd.read_csv('airportnew.csv')

# Filter de dataframe om alleen de gegevens voor de gewenste origin airports te behouden
selected_airports = ['ATL', 'ORD', 'DFW', 'LAX', 'PHX']
Airportflights = airportnew[airportnew['Origin_airport'].isin(selected_airports)]
Airportflights = Airportflights[Airportflights['Flights'] < 200]

# Definieer een kleurenkaart voor de gewenste luchthavens
color_map = {
    'PHX': 'red',
    'DFW': 'blue',
    'LAX': 'yellow',
    'ORD': 'green',
    'ATL': 'purple'
}

# Maak een histogram voor de geselecteerde airports met aangepaste kleuren
fig = px.histogram(
    Airportflights,
    x='Flights',
    color='Origin_airport',
    title='Amount of montly flights per Airport',
    color_discrete_map=color_map
)
fig.update_xaxes(rangeslider_visible=True, rangemode='tozero')

# Toon het histogram in Streamlit
st.plotly_chart(fig)


# In[26]:


import streamlit as st
import plotly.express as px

# Definieer de dataframe
airportnew = pd.read_csv('airportnew.csv')

# Filter de data voor de geselecteerde luchthavens
selected_airports = ['ATL', 'ORD', 'DFW', 'LAX', 'PHX']
seat_passenger = airportnew[airportnew['Origin_airport'].isin(selected_airports)]

# Groepeer de gegevens per luchthaven en datum
grouped_data = seat_passenger.groupby(['Origin_airport', 'Fly_date']).sum().reset_index()

# Bereken de gemiddelde loadfactor per vlucht
grouped_data['Grouped_Loadfactor'] = (grouped_data['Passengers'] / grouped_data['Seats']) * 100

# Toon de scatterplot in Streamlit
st.plotly_chart(fig)


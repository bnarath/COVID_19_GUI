#Import packages
import os
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
import math

#Change to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


#Data Retrieval
'''
Timestamp values have a precision in fractional seconds that range 
from 0 to 9. For example, a precision of 0 means that no fractional 
seconds are stored, 3 means that the timestamp stores milliseconds, 
and 9 means a precision of nanoseconds. 0 is the minimum precision, 
and 9 is the maximum.
'''
DF = pd.read_excel('COVID-19-geographic-disbtribution-worldwide-2020-05-29.xlsx', dtype={'DateRep':'datetime64[0]', 'Countries and territories':'str', 'GeoId':'str' })

#Select only the required columns
DF_Sel = DF[['dateRep', 'cases', 'deaths', 'countryterritoryCode']]
#Rename those columns
DF_Sel = DF_Sel.rename(columns={'dateRep':'Date', 'countryterritoryCode':'Country'})
DF_Sel.columns = [col.capitalize() for col in DF_Sel.columns]
#Take off the time from Date
DF_Sel["Date"] = DF_Sel["Date"].map(lambda x: datetime.date(x))

#We need 5 types of graphs
#1. Country Vs Date for Daily Cases
#2. Country Vs Date for deaths
#3. Country Vs Date for Cum Cases
#4. Country Vs Date for Cum deaths

Title = ["Daily Cases", "Daily Deaths", "Cumulative Cases", "Cumulative Deaths"]
for iter in range(1,5):
    if iter==1 or iter==3:
        #Obtain Country Vs Date for Daily Cases
        Cases = pd.pivot_table(DF_Sel,index=["Country"],values=["Cases"],
               columns=["Date"],aggfunc=[np.sum], fill_value=0, margins=False)
    elif iter==2 or iter==4:
        #Obtain Country Vs Date for Daily Deaths
        Cases = pd.pivot_table(DF_Sel,index=["Country"],values=["Deaths"],
               columns=["Date"],aggfunc=[np.sum], fill_value=0, margins=False)

    if iter==3 or iter==4:
        #For Cumulative Cases or Deaths, take cumsum across dates
        Cases = Cases.cumsum(axis=1)
    

    
    
    #Get rid of extra layers of the column names
    Cases.columns = Cases.columns.get_level_values(2)

    #reset index and obtain it as column
    Cases.reset_index(inplace=True)

    #Draw choropleth plots using plotly go
    
    Frames = Cases.columns[1:][15:] #Dates staring from 15th January
    fig = go.Figure(
        data=[go.Choropleth(
        locations=Cases['Country'], # Spatial coordinates
        z = Cases[Frames[0]], # Data to be color-coded
        locationmode = 'ISO-3', 
        colorscale = 'Reds',
        colorbar_title = "Confirmed Cases",)],
        layout=go.Layout(
            title_text=f"COVID-19 {Title[iter-1]} Worldwide from Jan 15 to Mar 29",
            geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
            annotations = [dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Data Source: <a href="https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide">\
                European Centre for Disease Prevention and Control</a>',
                showarrow = True
            )],
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                            method="animate",
                            args=[None])])]
        ),
        frames=[go.Frame(data=[go.Choropleth(
        locations=Cases['Country'], # Spatial coordinates
        z = Cases[Frames[i]], # Data to be color-coded
        locationmode = 'ISO-3',
        #colorscale = 'Reds',
        colorscale= [
            [0, 'rgb(255, 255, 255)'],        
            [1, 'rgb(255, 0, 0)']], 
        colorbar_title = f"Title{iter}",),]) for i in range(1, len(Frames))]
    )

    pio.write_html(fig, file=f"{Title[iter-1]}.html", auto_open=True)
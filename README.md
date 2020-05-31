# Plotly Illustration of COVID-19 Data

We had seen enough this year, through COVID - 19 times.
In the mid of January, it was just in Wuhan and the world was not prepared to deal with it.
Looking back, today the epicentre has been moving from one to the other.

In this project, we would see an illustration of COVID-19 impact and how it changed it's epicentre from January 15 Till May 29th 2020 (The day, I am putting this up)

Python <a href=https://plotly.com/python/>plotly.py</a> is a graphing library makes interactive, publication-quality graphs.
Plotly is an open-source, interactive data visualization library for Python. Plotly graphs can be viewed in Jupyter notebooks, standalone HTML files, or hosted online using <a href="https://chart-studio.plotly.com/">Chart Studio Cloud</a>

## Data Source
For the purpose of illustration, we can download the data from <a href="https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide">the website of European Centre for Disease Prevention and Control</a>. It appears to me that they publish this data on a daily basis

<a href="COVID-19-geographic-disbtribution-worldwide-2020-05-29.xlsx">Downloaded Data File in excel format</a>
## Data Retrieval

```python
DF = pd.read_excel('COVID-19-geographic-disbtribution-worldwide-2020-05-29.xlsx', dtype={'DateRep':'datetime64[0]', 'Countries and territories':'str', 'GeoId':'str' })

DF.head()

0	2020-05-29	29	5	2020	580	8	Afghanistan	AF	AFG	37172386.0	Asia
1	2020-05-28	28	5	2020	625	7	Afghanistan	AF	AFG	37172386.0	Asia
2	2020-05-27	27	5	2020	658	1	Afghanistan	AF	AFG	37172386.0	Asia
3	2020-05-26	26	5	2020	591	1	Afghanistan	AF	AFG	37172386.0	Asia
4	2020-05-25	25	5	2020	584	2	Afghanistan	AF	AFG	37172386.0	Asia
```

## Data Preprocessing

```python
#Select only the required columns
DF_Sel = DF[['dateRep', 'cases', 'deaths', 'countryterritoryCode', 'popData2018']]
DF_Sel = DF_Sel.rename(columns={'dateRep':'Date', 'countryterritoryCode':'Country', 'popData2018':'Population'})
DF_Sel.columns = [col.capitalize() for col in DF_Sel.columns]

#Take off the time from date
DF_Sel["Date"] = DF_Sel["Date"].map(lambda x: datetime.date(x))
```

## Data Manipulation

Obtain the summary using pandas pivot function
```python
#Obtain Country Vs Date for Daily Cases
Daily_Cases = pd.pivot_table(DF_Sel,index=['Country'],values=["Cases"],
               columns=["Date"],aggfunc=[np.sum], fill_value=0, margins=False)
               
#Get rid of extra layers of the column names
Daily_Cases.columns = Daily_Cases.columns.get_level_values(2)

#reset index and obtain it as column
Daily_Cases.reset_index(inplace=True)

Daily_Cases.head()

```
The DataFrame we obtained looks like this
<img src="Summary_DF" alt="Summary DF">

## Choropleth Map in Plotly

A Choropleth Map is a map composed of colored polygons. It is used to represent spatial variations of a quantity. go.Choropleth graph objects (like many other plotly objects) have a go.layout.Geo object which can be used to control the appearance of the base map onto which data is plotted

We can plot a choropleth map in plotly go as follows:

### Key points
- Here we give 'Country' column as the spacial coordinates, as it is in the format (3 letter code) the function expects.
- A frame is a  column corresponds to the confirmed cases across all countries
- We have frames corresponds to each date of interest Jan 15 to Mar 29

```python

Frames = Daily_Cases.columns[1:][15:]
fig = go.Figure(
    data=[go.Choropleth(
    locations=Daily_Cases['Country'], # Spatial coordinates
    z = Daily_Cases[Frames[0]], # Data to be color-coded
    locationmode = 'ISO-3', 
    colorscale = 'Reds',
    colorbar_title = "Confirmed Cases",)],
    layout=go.Layout(
        title_text='COVID-19 Daily Cases Worldwide from Jan 15 to Mar 29',
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
    locations=Daily_Cases['Country'], # Spatial coordinates
    z = Daily_Cases[Frames[i]], # Data to be color-coded
    locationmode = 'ISO-3',
    #colorscale = 'Reds',
    colorscale= [
        [0, 'rgb(255, 255, 255)'],        
        [1, 'rgb(255, 0, 0)']], 
    colorbar_title = "Confirmed Cases",),]) for i in range(1, len(Frames))]
)

fig.show()

```
Finally we can write plotly figure into an html file

```python
pio.write_html(fig, file='index.html', auto_open=True)
```

## Jupyter Notebook is <a href="COVID-19-geographic-disbtribution-worldwide-2020-05-29.xlsx">here</a>
## Full deployment file <a href="covid19_illustration.py">here</a>

Here, 4 graphs are generated
- Country Vs Date for Daily Cases
- Country Vs Date for deaths
- Country Vs Date for Cumulative Cases
- Country Vs Date for Cumulative deaths

## Featured
Graph illustrating Daily Cases worldwide is hosted on <a href="https://bnarath.github.io/COVID_19_GUI/"> github pages</a>

It is shocking to see the epicenter being shifted over time

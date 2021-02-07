import pandas as pd
import pandasql
import plotly.express as px
import boto3
from io import BytesIO

import chart_studio.plotly as py
import chart_studio.tools as tls

def generateWeatherData():
    storm_details = pd.DataFrame()
    s3 = boto3.resource('s3')
    obj = s3.Object('stormdetailsfile', 'details/stormDetails.csv')
    a = BytesIO(obj.get()['Body'].read())

    with BytesIO(obj.get()['Body'].read()) as bio:
        storm_details = pd.read_csv('s3://stormdetailsfile/details/stormDetails.csv')
    
    numberOfEventsPerMonthPriorYears = pandasql.sqldf("SELECT MONTH_NAME, YEAR , COUNT(EVENT_ID) as MaxNumberOfEvents  FROM storm_details where YEAR <>2018 group by MONTH_NAME, YEAR")
    numberOfEvents = pandasql.sqldf("SELECT MONTH_NAME, YEAR , COUNT(EVENT_ID) as MaxNumberOfEvents  FROM storm_details where YEAR = 2018 group by MONTH_NAME, YEAR")
    fig = px.box(numberOfEventsPerMonthPriorYears, x=numberOfEventsPerMonthPriorYears['MONTH_NAME'], y=numberOfEventsPerMonthPriorYears['MaxNumberOfEvents'])
    fig.update_traces(x =numberOfEventsPerMonthPriorYears['MONTH_NAME'],y=numberOfEventsPerMonthPriorYears['MaxNumberOfEvents'],name = "Data Distribution for years prior 2018",showlegend= True )
    fig.add_scatter(x = numberOfEvents['MONTH_NAME'],
        y = numberOfEvents['MaxNumberOfEvents'],
        mode = "markers",marker = dict(size=15, color="LightSeaGreen"),
        name = "2018 Max Number Events",
        showlegend= True)
    
    #Logic to upload the graph to plotly cloud so that it can be accessed by the from end
    #using the embed source
    plotly_username = 'meanusingh'
    plotly_key = 'WPfbzXKMHCr8BeW4i6Yr'
    py.sign_in(plotly_username, plotly_key)
    
    plotUrl = py.plot(fig,'stromsGraph')
    plotEmbed = tls.get_embed(plotUrl)
    plotEmbedURL = plotUrl+'.embed'
    return plotEmbedURL

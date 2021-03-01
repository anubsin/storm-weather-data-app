import boto3
from io import StringIO
import requests
import re
from bs4 import BeautifulSoup
import ssl
import pandasql
import pandas as pd

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
r = requests.get('https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/')
soup = BeautifulSoup(r.text, "html.parser")
storm_details = pd.DataFrame()
storm_fatalities =  pd.DataFrame()
storm_locations =  pd.DataFrame()
years = []
files = []

s3_resource = boto3.resource('s3')
first_bucket = s3_resource.Bucket(name='stormdetailsfile')
first_object = s3_resource.Object(
bucket_name= 'stormdetailsfile', key='details')

for link in soup.findAll('a'):
    a = (link.get('href'))
    if re.findall('d201[0-8]{1}' , a):
         c = 'https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/%s' %a
         if ((re.search('StormEvents_details',c))):
             df = pd.read_csv(c)
             sd =  pandasql.sqldf("SELECT * FROM df WHERE (state ='KENTUCKY' )")
             storm_details = pd.concat([storm_details, sd], axis = 0)
            # check = pandasql.sqldf("SELECT DISTINCT(EVENT_ID) FROM storm_details")
         elif re.findall('d2018' , a):
            c = 'https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/%s' % a
            if ((re.search('StormEvents_fatalities',c))and (re.findall('d2018',a))):
                sf = pd.read_csv(c)
                #  fatality = pandasql.sqldf("SELECT * FROM fatality")
                storm_fatalities=pd.concat([storm_fatalities, sf], axis =0)
            if ((re.search('StormEvents_locations', c)) and (re.findall('d2018',a))):
                sl = pd.read_csv(c)
           # location = pandasql.sqldf("SELECT * FROM df2")
                storm_locations = pd.concat([storm_locations, sl], axis=0)
csv_buffer = StringIO()
storm_details.to_csv(csv_buffer)
Body = csv_buffer.getvalue()
s3_resource = boto3.resource('s3')
s3_resource.Object('stormdetailsfile', 'details/stormDetails.csv').put(Body=csv_buffer.getvalue())
#s3_resource.Object('stormdetailsfile', 'details/fatalities.csv').put(Body=csv_buffer.getvalue())

csv_buffer1 = StringIO()
storm_fatalities.to_csv(csv_buffer1)
Body = csv_buffer1.getvalue()
s3_resource = boto3.resource('s3')
s3_resource.Object('stormdetailsfile', 'details/fatalities.csv').put(Body=csv_buffer.getvalue())

csv_buffer2 = StringIO()
storm_locations.to_csv(csv_buffer2)
Body = csv_buffer2.getvalue()
s3_resource = boto3.resource('s3')
s3_resource.Object('stormdetailsfile', 'details/storm_locations').put(Body=csv_buffer.getvalue())

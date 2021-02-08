import json
from weatherData import generateWeatherData

def handler(event, context):
  
  weathwerData = json.loads(generateWeatherData())
  description = "As seen on grpah, anomaly is detected for the month of September."
  title = "Events per month data distribution for 2018 relative to prior years."

  body = {
    'year': 2018,
    'totalEvents': weathwerData["eventsCount"],
    'totalDeaths': weathwerData["deathsCount"],
    'state': 'KY',
    'graph_encoded': weathwerData["graphURL"],
    'description': description,
    'title': title
  }

  response = {
    'statusCode': 200,
    'body': json.dumps(body),
    'headers': {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  }
  return response

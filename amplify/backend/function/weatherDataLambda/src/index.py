import json
from weatherData import generateWeatherData

def handler(event, context):
  
  weathwerData = json.loads(generateWeatherData())

  body = {
    'year': 2018,
    'totalEvents': weathwerData["eventsCount"],
    'totalDeaths': weathwerData["deathsCount"],
    'state': 'KY',
    'graph_encoded': weathwerData["graphURL"]
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

import json
from weatherData import generateWeatherData

def handler(event, context):
  
  plot_graph_embed_frame = generateWeatherData()

  body = {
    'year': 2018,
    'totalEvents': 115,
    'state': 'KY',
    'graph_encoded': plot_graph_embed_frame
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

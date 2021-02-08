import './App.css';
import React, {useEffect, useReducer} from 'react'
import {AmplifySignOut, withAuthenticator} from '@aws-amplify/ui-react'
import { API, Auth} from 'aws-amplify'
import Iframe from './iFrame.js';

function App() {

  function reducer(state, action){
    switch (action.type){
      case 'setweatherdata':
        return {...state, weatherData: {
                            ...state.weatherData,
                            year: action.payload.year,
                            province: action.payload.province,
                            totalEvents: action.payload.totalEvents,
                            totalDeaths: action.payload.totalDeaths,
                            graph_encoded: action.payload.graph_encoded,
                            title: action.payload.title,
                            description: action.payload.description
                          }

                }
      default:
        return {...state,initialState}
    }
  } 

  const initialState = {
    weatherData: {
      province: 'KY',
      year:'2018',
      totalEvents: 'loading...',
      totalDeaths: 'loading...',
      graph_encoded: '',
      title: '',
      description: ''
    }
  }

  const [state, dispatch] = useReducer(reducer, initialState)
 // const [weatherData, setWeatherData] = useState({year: 'year', totalEvents: 'totalEvents', state: 'state', graph_encoded: 'graph_encoded'})
  
  //Function to call the weather API after making sure the user is authenticated
  async function callWeatherApi() {
    const user = await Auth.currentAuthenticatedUser()
    const token = user.signInUserSession.idToken.jwtToken
    const requestInfo = {
      headers: {
        Authorization: token
      }
    }
    const apiData = await API.get('weatherApi', '/stormdata', requestInfo) 
   
   dispatch({type: 'setweatherdata', payload: {year: apiData.year, province: apiData.state, totalEvents: apiData.totalEvents, 
    totalDeaths: apiData.totalDeaths, graph_encoded: apiData.graph_encoded, title: apiData.title, description: apiData.description}})
  }
 
  useEffect(() => {
    callWeatherApi();
  }, [])

  return (
    <div className="App"> 
      <header className="App-header">
        <AmplifySignOut />
        <h1>Weather Data Summary for {state.weatherData.year} for {state.weatherData.province}</h1>
      </header>
      <div className='container'>
        <div className='block'>Total events: {state.weatherData.totalEvents}</div>
        <div className='block'>Total fatalities: {state.weatherData.totalDeaths}</div>
      </div>
      <div className='container' min-height='100vh'>
        <h3>{state.weatherData.title}</h3>
        <Iframe source={state.weatherData.graph_encoded} /> 
        <p>{state.weatherData.description}</p>
      </div>
      <footer>
        <div className='footer'>
          Built with{' '}
          <span role='img' aria-label='love'>
            💚
          </span>{' '}
          by Anu Singh
        </div>
      </footer>
    </div>
  );
}

export default withAuthenticator(App);

import React, { useState } from 'react';
import { View, Alert, Text, Button } from 'react-native';
import { from, of, Observable } from 'rxjs';
import { map, tap, catchError, switchMap } from 'rxjs/operators';
//import Constants from 'expo-constants';
import { connect } from 'react-redux';

//import AppRedux from '../../store/AppRedux';
import Geolocation from '@react-native-community/geolocation';
//import BackgroundService from 'react-native-background-actions';
import BackgroundTimer from 'react-native-background-timer';


//const DEVICE_ID = Constants.installationId;
const DEVICE_ID = 'C2044035-EA0B-4A9C-9D12-FC4A7A3DB170' //TODO: generate and store this
// const API_KEY = Constants.manifest.extra.API_KEY;
const API_KEY = "4b6bff10-760e-11ea-bcd4-03a854e8623c"

interface IOptionButtonProps {
  icon: string;
  label: string;
  onPress: any;
  isLastOption?: boolean;
}

export const MapScreen = () => {
  /*const locationConfig = {
    skipPermissionRequests: false,
    authorizationLevel: "always"
  }

  Geolocation.setRNConfiguration(locationConfig);*/
  Geolocation.requestAuthorization(); //TODO: move to initial onboarding flow
  
  function encryptLocation(gpsObj: any){
    fetch('https://safetraceapi.herokuapp.com/api/encryption', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': API_KEY,
        //'device_key': 'cb94a1442fc90ee43d17a4284ea26675a432fc4c7a1d6d0905c23ce5eaa0f391'
        'device_key': '3d99ffd9b5c0b9b95e1b97a5334bce3918dec4bc541ab4fac25a71f5437c4e31',
        //'device_key': private_key TODO: fix this, add from memory
      },
      body: JSON.stringify({
        //TODO: make device id, row type, infection status dynamic
        "device_id": DEVICE_ID,       
        "row_type": 0,      
        "latitude": gpsObj.coords.latitude,
        "longitude": gpsObj.coords.longitude,
      }),
    }).then((response) => response.json())
    .then((json) => {
      console.log('Submitted gps test'); //TODO: remove
      console.log(json)
      submitLocation(json.encrypted_body);
      //return json.encrypted_body;
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }

  function submitLocation(gps_json: JSON){
    fetch('https://safetraceapi.herokuapp.com/api/events', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': API_KEY,
        //'device_key': 'cb94a1442fc90ee43d17a4284ea26675a432fc4c7a1d6d0905c23ce5eaa0f391'
        'device_key': '250765803750a51bed76023b5491c71c992e8d42f28afecc15f12411c7eb9ecc',
        //'device_key': private_key TODO: fix this, add from memory
      },
      body: JSON.stringify(gps_json),
    }).then((response) => response.json())
    .then((json) => {
      console.log('submitted encrypted GPS data'); //TODO: remove
      console.log(json)
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }

  //TODO: gather+store location data during the whole hour, more ios testing, android testing,

  function getGPS(){
    BackgroundTimer.runBackgroundTimer(() => {
      var min = new Date().getMinutes()
      var sec = new Date().getSeconds(); 
      console.log(min);
      console.log(sec);
      if (min < 1 && min >= 0 && sec < 10 && sec >=0) { //less than wahtever our update interval
        console.log('time');
        Geolocation.getCurrentPosition(info => encryptLocation(info));
      }
      }, 
      10000);
  }  


  return (
    <View>
      <View>
        <Button title="GPS Test" onPress = {getGPS}/>
        <Button title="Stop GPS Test" onPress = {() => {
          BackgroundTimer.stopBackgroundTimer();
        }}/>
      </View>
    </View>
  );
}

export default MapScreen;
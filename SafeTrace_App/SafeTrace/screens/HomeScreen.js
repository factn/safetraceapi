import * as WebBrowser from 'expo-web-browser';
//import * as React from 'react';
import React, {useEffect, useState, Component} from 'react';
import { ActivityIndicator, FlatList, Text, View, Button, TextInput, Image, Platform, StyleSheet, TouchableOpacity, Vibration, Alert, AsyncStorage} from 'react-native';
import Constants from 'expo-constants';
import { Notifications } from 'expo';
//import * as Permissions from 'expo-permissions';
//import * as SecureStore from 'expo-secure-store';
//import RNSecureStorage, { ACCESSIBLE } from 'rn-secure-storage'
//import { ScrollView } from 'react-native-gesture-handler';
//import { MonoText } from '../components/StyledText';

//You need to get one of these for yourself and put it in the app.json file
const deviceID = Constants.installationId // An identifier that is unique to this particular device and installation of the Expo client.

export default function HomeScreen() {

  //let uniqueId = DeviceInfo.getUniqueId();

  const [enteredSymptoms, setEnteredSymptoms] = useState('');
  //const [symptoms, setSymptoms] = useState([]);

  const symptomsInputHandler = (enteredText) => {
    setEnteredSymptoms(enteredText);
  }

  const value = ''

  /*export const setObjectForKey = async ({key, object, ttl = undefined }) => {

    if (!key) throw new Error('Cannot set an object without a key');

    if (!object) throw new Error('Cannot set a key without an object');

    let expiresAt = undefined;
    if (ttl) {
        expiresAt = new Date().getTime() + ttl;
    }
    let wrappedObj = {
        object,
        expiresAt,
    };
    let stringedWrapper = JSON.stringify(wrappedObj);

    return await AsyncStorage.setItem(key,stringedWrapper)
  };

  export const removeObjectForKey = async (key) => {
      return await AsyncStorage.removeItem(key)
  };


export const getObjectForKey = async (key) => {
    let now = new Date().getTime();
    let stringedWrapper = await AsyncStorage.getItem(key);

    if (!stringedWrapper) throw new Error('No key found for object');

    let wrapper = JSON.parse(stringedWrapper);
    if (wrapper.expiresAt < now) {
        // Object expired
        AsyncStorage.removeItem(key);
        throw new Error('Object expired');
    } else {
        return wrapper.object;
    }
};*/



  //store and get the user's private key

  function encryptSymptomEntry () {
    //console.log(enteredSymptoms);
    fetch('https://safetraceapi.herokuapp.com/api/encryption', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': Constants.manifest.extra.API_KEY,
        //'device_key': 'cb94a1442fc90ee43d17a4284ea26675a432fc4c7a1d6d0905c23ce5eaa0f391'
        'device_key': '250765803750a51bed76023b5491c71c992e8d42f28afecc15f12411c7eb9ecc',
        //'device_key': private_key TODO: fix this, add from memory
      },
      body: JSON.stringify({
        //TODO: make device id, row type, infection status dynamic
        'device_id' : deviceID,
        'row_type' : 2,
        'symptoms' : enteredSymptoms,
        //'symptoms' : 'cough,fever',
        'infection_status' : 1,
      }),
    }).then((response) => response.json())
    .then((json) => {
      console.log('Submitted Symptoms for encryption'); //TODO: remove
      console.log(json);
      console.log(json.encrypted_body);
      submitSymptomEntry(json.encrypted_body);
      //return json.encrypted_body;
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }

  function submitSymptomEntry (symptom_json){
    //const symptom_json = encryptSymptomEntry();
    
    console.log(symptom_json);
    fetch('https://safetraceapi.herokuapp.com/api/events', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': Constants.manifest.extra.API_KEY,
      },
      //body: symptom_json,
      body:{
        device_id: symptom_json.device_id,
        infection_status: symptom_json.infection_status,
        row_type: symptom_json.row_type,
        symptoms: symptom_json.symptoms,
      }
    }).then((response) => response.json())
    .then((json) => {
      console.log('Submitted Encrypted Symptoms'); //TODO: remove
      console.log(json);
      console.log(json.event_id);
      return json.event_id;
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }

  function handleSignupPress () {
    fetch('https://safetraceapi.herokuapp.com/api/devices', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': Constants.manifest.extra.API_KEY
      },
      body: JSON.stringify({
        'device_id': deviceID,
      }),
    }).then((response) => response.json())
    .then((json) => {
      console.log('signup request sent');
      //console.log(json)
      console.log(json.message);
      console.log(json.device_key)
      //console.log(json.device_key);
      if (typeof json.error != 'undefined'){
        console.log(json.error)
        Alert.alert(
          'Device Already Registered Error',
          json.error,
          [
            { text: 'OK', onPress: () => console.log('OK Pressed') },
          ],
          { cancelable: false }
        );
      }
      else{
        console.log(json.device_key)
        /*const saveKey = async value => {
          try{
            await AsyncStorage.setItem('private_key', value);
          }catch (error){
            console.log(error.message);
          }
        }*/
        //storeData(JSON.stringify(json.device_key));
        //hideKey("priv_key", JSON.stringify(json.device_key))
        return json.device_key;
        //TODO: store the key
      }
      
    })
    .catch((error) => {
      console.error(error);
    });
  }


  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        <TextInput placeholder="Enter Symptoms" style={styles.input} onChangeText={symptomsInputHandler} value={enteredSymptoms}/>
        <Button title="Submit Symptoms" onPress = {encryptSymptomEntry}/>
      </View>
      <View>
        <Button title="Sign Up" onPress = {handleSignupPress}/>
      </View>
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};

function DevelopmentModeNotice() {
  if (__DEV__) {
    const learnMoreButton = (
      <Text onPress={handleLearnMorePress} style={styles.helpLinkText}>
        Learn more
      </Text>
    );

    return (
      <Text style={styles.developmentModeText}>
        Development mode is enabled: your app will be slower but you can use useful development
        tools. {learnMoreButton}
      </Text>
    );
  } else {
    return (
      <Text style={styles.developmentModeText}>
        You are not in development mode: your app will run at full speed.
      </Text>
    );
  }
}

function handleLearnMorePress() {
  WebBrowser.openBrowserAsync('https://docs.expo.io/versions/latest/workflow/development-mode/');
}

function handleHelpPress() {
  WebBrowser.openBrowserAsync(
    'https://docs.expo.io/versions/latest/get-started/create-a-new-app/#making-your-first-change'
  );
}

const styles = StyleSheet.create({
  screen: {
    padding: 50
  },
  inputContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 15
  },
  input: {
    width: '50%',
    borderBottomColor: 'black',
    borderBottomWidth: 1
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 50,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: 'rgba(96,100,109, 0.8)',
  },
  codeHighlightContainer: {
    backgroundColor: 'rgba(0,0,0,0.05)',
    borderRadius: 3,
    paddingHorizontal: 4,
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  tabBarInfoContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { width: 0, height: -3 },
        shadowOpacity: 0.1,
        shadowRadius: 3,
      },
      android: {
        elevation: 20,
      },
    }),
    alignItems: 'center',
    backgroundColor: '#fbfbfb',
    paddingVertical: 20,
  },
  tabBarInfoText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    textAlign: 'center',
  },
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});

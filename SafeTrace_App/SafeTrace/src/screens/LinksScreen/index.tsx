import React from 'react';
import { View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { WebBrowser } from 'expo';

import {
  BaseLayout,
  OptionButtonContainer,
  OptionIconContainer,
  OptionLabelContainer,
  OptionLabel
} from './styles';

interface IOptionButtonProps {
  icon: string;
  label: string;
  onPress: any;
  isLastOption?: boolean;
}

const OptionButton = ({ icon, label, onPress, isLastOption }: IOptionButtonProps) => {
  return (
    <OptionButtonContainer lastOption={isLastOption} onPress={onPress}>
      <View style={{ flexDirection: 'row' }}>
        <OptionIconContainer>
          <Ionicons name={icon} size={22} color="rgba(0,0,0,0.35)" />
        </OptionIconContainer>
        <OptionLabelContainer>
          <OptionLabel>{label}</OptionLabel>
        </OptionLabelContainer>
      </View>
    </OptionButtonContainer>
  );
}

export const MapScreen = () => {

  function encryptGPS(){
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
        "device_id": deviceID,       
        "row_type": 0,      
        "latitude": 45,
        "longitude": 155,
      }),
    }).then((response) => response.json())
    .then((json) => {
      console.log('Submitted gps test'); //TODO: remove
      console.log(json)
      //console.log(json);
      //console.log(json.encrypted_body);
      submitGPS(json.encrypted_body);
      //return json.encrypted_body;
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }

  function submitGPS(gps_json){
    fetch('https://safetraceapi.herokuapp.com/api/events', {
      method: 'POST',
      headers : {
        'Content-Type': 'application/json',
        'api_key': Constants.manifest.extra.API_KEY,
        //'device_key': 'cb94a1442fc90ee43d17a4284ea26675a432fc4c7a1d6d0905c23ce5eaa0f391'
        'device_key': '250765803750a51bed76023b5491c71c992e8d42f28afecc15f12411c7eb9ecc',
        //'device_key': private_key TODO: fix this, add from memory
      },
      body: JSON.stringify(gps_json),
      /*body: JSON.stringify({
        'device_id': gps_json.device_id,
        'latitude': gps_json.latitude,
        'longitude': gps_json.longitude,
        'row_type': gps_json.row_type
      }),*/
      /*body: JSON.stringify({
        //TODO: make device id, row type, infection status dynamic
        "device_id": deviceID,       
        "row_type": 0,      
        "latitude": 45,
        "longitude": 155,
      }),*/
    }).then((response) => response.json())
    .then((json) => {
      console.log('submitted encrypted GPS data'); //TODO: remove
      console.log(json)
      //console.log(json);
      //console.log(json.encrypted_body);
      //submitSymptomEntry(json.encrypted_body);
      //return json.encrypted_body;
    })
    .catch((error) => {
      console.error(error);
      return error;
    });
  }


  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        
      </View>
      <View>
        <Button title="Sign Up" onPress = {handleSignupPress}/>
      </View>
      <View>
        <Button title="GPS Test" onPress = {encryptGPS}/>
      </View>
    </View>
  );
}

  return (
    <BaseLayout
      contentContainerStyle={{ paddingTop: 15 }}
    >
      <OptionButton
        icon="md-school"
        label="Read the Expo documentation"
        onPress={() => WebBrowser.openBrowserAsync('https://safetraceapi.org')}
      />

      <OptionButton
        icon="md-compass"
        label="Read the React Navigation documentation"
        onPress={() =>
          WebBrowser.openBrowserAsync('https://reactnavigation.org')
        }
      />

      <OptionButton
        icon="ios-chatboxes"
        label="Ask a question on the forums"
        onPress={() => WebBrowser.openBrowserAsync('https://forums.expo.io')}
        isLastOption={true}
      />
    </BaseLayout>
  );
};

LinksScreen.navigationOptions = {
  header: null,
};

export default LinksScreen;
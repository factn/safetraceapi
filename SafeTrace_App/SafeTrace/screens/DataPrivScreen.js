import { Ionicons } from '@expo/vector-icons';
import * as WebBrowser from 'expo-web-browser';
import * as React from 'react';
import { StyleSheet, Text, View, Alert, Button } from 'react-native';
import { RectButton, ScrollView } from 'react-native-gesture-handler';
import Constants from 'expo-constants';

export default function DataPrivScreen() {

  const deviceID = Constants.installationId

  function removeDevice () {
    fetch('https://safetraceapi.herokuapp.com/api/devices', {
      method: 'DELETE',
      headers : {
        'Content-Type': 'application/json',
        api_key: Constants.manifest.extra.API_KEY
      },
      body: JSON.stringify({
        //TODO: make device id, row type, infection status dynamic
        'device_id' : deviceID,
      }),
    }).then((response) => response.json())
    .then((json) => {
      console.log('Submitted Symptoms'); //TODO: remove
      console.log(json);
      console.log(json.message);
      if (typeof json.error != 'undefined'){
        console.log(json.error)
        Alert.alert(
          'Account Deletion Error',
          json.error,
          [
            { text: 'OK', onPress: () => console.log('OK Pressed') },
          ],
          { cancelable: false }
        );
      }
      else{
        Alert.alert(
          'Successfully Removed Your Device',
          json.message,
          [
            { text: 'OK', onPress: () => console.log('OK Pressed') },
          ],
          { cancelable: false }
        );
        return json.message;
      }
      
    })
    .catch((error) => {
      console.error(error);
    });
  }

  return (
    <View style={styles.container}>
        <Button title="Remove Device" onPress = {removeDevice}/>
    </View>
  );
}

function OptionButton({ icon, label, onPress, isLastOption }) {
  return (
    <RectButton style={[styles.option, isLastOption && styles.lastOption]} onPress={onPress}>
      <View style={{ flexDirection: 'row' }}>
        <View style={styles.optionIconContainer}>
          <Ionicons name={icon} size={22} color="rgba(0,0,0,0.35)" />
        </View>
        <View style={styles.optionTextContainer}>
          <Text style={styles.optionText}>{label}</Text>
        </View>
      </View>
    </RectButton>
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
  container: {
    flex: 1,
    backgroundColor: '#fafafa',
  },
  contentContainer: {
    paddingTop: 15,
  },
  optionIconContainer: {
    marginRight: 12,
  },
  option: {
    backgroundColor: '#fdfdfd',
    paddingHorizontal: 15,
    paddingVertical: 15,
    borderWidth: StyleSheet.hairlineWidth,
    borderBottomWidth: 0,
    borderColor: '#ededed',
  },
  lastOption: {
    borderBottomWidth: StyleSheet.hairlineWidth,
  },
  optionText: {
    fontSize: 15,
    alignSelf: 'flex-start',
    marginTop: 1,
  },
});

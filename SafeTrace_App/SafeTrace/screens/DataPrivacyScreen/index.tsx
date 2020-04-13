import React from 'react';

import { BaseLayout, Button } from './styles';
import { from } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import Constants from 'expo-constants';
import { Alert } from 'react-native';

// function OptionButton({ icon, label, onPress, isLastOption }) {
//   return (
//     <RectButton style={[styles.option, isLastOption && styles.lastOption]} onPress={onPress}>
//       <View style={{ flexDirection: 'row' }}>
//         <View style={styles.optionIconContainer}>
//           <Ionicons name={icon} size={22} color='rgba(0,0,0,0.35)' />
//         </View>
//         <View style={styles.optionTextContainer}>
//           <Text style={styles.optionText}>{label}</Text>
//         </View>
//       </View>
//     </RectButton>
//   );
// }

const DEVICE_ID = Constants.installationId;
// const API_KEY = Constants.manifest.extra.API_KEY;

const DataPrivacyScreen = () => {
  const removeDevice = () => {
    from(
      fetch('https://safetraceapi.herokuapp.com/api/devices', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          // api_key: API_KEY,
        },
        body: JSON.stringify({
          // TODO: make device id, row type, infection status dynamic
          device_id: DEVICE_ID,
        }),
      })
    )
      .pipe(
        map((resp: any) => resp.json()),
        tap((resp) => {
          if (typeof resp.error !== 'undefined') {
            console.log(resp.error);
            Alert.alert(
              'Account Deletion Error',
              resp.error,
              [{ text: 'OK', onPress: () => console.log('OK Pressed') }],
              { cancelable: false }
            );
          } else {
            Alert.alert(
              'Successfully Removed Your Device',
              resp.message,
              [{ text: 'OK', onPress: () => console.log('OK Pressed') }],
              { cancelable: false }
            );
          }
        })
      )
      .subscribe();
  };

  return (
    <BaseLayout>
      <Button title="Remove Device" onPress={removeDevice} />
    </BaseLayout>
  );
};

// const styles = StyleSheet.create({
//   screen: {
//     padding: 50
//   },
//   inputContainer: {
//     flexDirection: 'row',
//     justifyContent: 'space-between',
//     alignItems: 'center',
//     paddingHorizontal: 15
//   },
//   input: {
//     width: '50%',
//     borderBottomColor: 'black',
//     borderBottomWidth: 1
//   },
//   container: {
//     flex: 1,
//     backgroundColor: '#fff',
//   },
//   container: {
//     flex: 1,
//     backgroundColor: '#fafafa',
//   },
//   contentContainer: {
//     paddingTop: 15,
//   },
//   optionIconContainer: {
//     marginRight: 12,
//   },
//   option: {
//     backgroundColor: '#fdfdfd',
//     paddingHorizontal: 15,
//     paddingVertical: 15,
//     borderWidth: StyleSheet.hairlineWidth,
//     borderBottomWidth: 0,
//     borderColor: '#ededed',
//   },
//   lastOption: {
//     borderBottomWidth: StyleSheet.hairlineWidth,
//   },
//   optionText: {
//     fontSize: 15,
//     alignSelf: 'flex-start',
//     marginTop: 1,
//   },
// });

DataPrivacyScreen.navigationOptions = {
  header: null,
};

export default DataPrivacyScreen;

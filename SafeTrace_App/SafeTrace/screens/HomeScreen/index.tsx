import React, { useState } from "react";
import { View, Alert, Text } from "react-native";
import { from, of, Observable } from "rxjs";
import { map, tap, catchError, switchMap } from "rxjs/operators";
import Constants from "expo-constants";
import { connect } from "react-redux";

import AppRedux from "../../store/AppRedux";
import { BaseLayout, InputContainer, Input, Button } from "./styles";

const DEVICE_ID = Constants.installationId;
const API_KEY = Constants.manifest.extra.API_KEY;

interface IProps {
  performTest: any;
  testVal: string;
}

const HomeScreen = (props: IProps) => {
  const [enteredSymptoms, setEnteredSymptoms] = useState("");

  const symptomsInputHandler = (enteredText: string) => {
    setEnteredSymptoms(enteredText);
  };

  const encryptSymptomEntry = () => {
    from(
      fetch("https://safetraceapi.herokuapp.com/api/encryption", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          api_key: Constants.manifest.extra.API_KEY,
          //"device_key": "cb94a1442fc90ee43d17a4284ea26675a432fc4c7a1d6d0905c23ce5eaa0f391"
          device_key:
            "250765803750a51bed76023b5491c71c992e8d42f28afecc15f12411c7eb9ecc",
          //"device_key": private_key TODO: fix this, add from memory
        },
        body: JSON.stringify({
          //TODO: make device id, row type, infection status dynamic
          device_id: DEVICE_ID,
          row_type: 2,
          symptoms: enteredSymptoms,
          //"symptoms" : "cough,fever",
          infection_status: 1,
        }),
      })
    )
      .pipe(
        map((resp: any) => resp.json()),
        switchMap((resp) => submitSymptomEntry(resp.encrypted_body)),
        tap((resp) => console.info("Submitted Response: ", resp))
      )
      .subscribe();
  };

  const submitSymptomEntry = (payload: any): Observable<any> => {
    return from(
      fetch("https://safetraceapi.herokuapp.com/api/events", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          api_key: Constants.manifest.extra.API_KEY,
        },
        body: {
          device_id: payload.device_id,
          infection_status: payload.infection_status,
          row_type: payload.row_type,
          symptoms: payload.symptoms,
        },
      })
    );
  };

  const handleSignupPress = () => {
    from(
      fetch("https://safetraceapi.herokuapp.com/api/devices", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          api_key: API_KEY,
        },
        body: JSON.stringify({
          device_id: DEVICE_ID,
        }),
      })
    )
      .pipe(
        map((resp) => resp.json()),
        tap((resp: any) => console.info(`Signup Request Response: `, res)),
        tap((resp) => {
          if (typeof resp.error !== "undefined") {
            Alert.alert(
              "Device Already Registered Error",
              resp.error,
              [{ text: "OK", onPress: () => console.log("OK Pressed") }],
              { cancelable: false }
            );
          } else {
            console.log(resp.device_key);
          }
        }),
        catchError((err) => {
          console.error("Caught error while submitting signup form. ", err);

          return of(err);
        })
      )
      .subscribe();
  };

  return (
    <BaseLayout>
      <InputContainer>
        <Input
          placeholder="Enter Symptoms"
          onChangeText={symptomsInputHandler}
          value={enteredSymptoms}
        />
        <Button title="Sign Up" onPress={handleSignupPress} />
      </InputContainer>
      <View>
        <Button title="Press me!" onPress={() => {
          props.performTest('Hello World');
          console.info(props.performTest);
        }} />
        <Text>Output from store: {props.testVal}</Text>
      </View>
    </BaseLayout>
  );
};

HomeScreen.navigationOptions = {
  header: null,
};

const mapStateToProps = (state: any) => {
  return {
    testVal: state.app.val,
  };
}

const mapDispatchToProps = (dispatch: any) => {
  return {
    performTest: (val: string) => dispatch(AppRedux.test(val))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomeScreen);
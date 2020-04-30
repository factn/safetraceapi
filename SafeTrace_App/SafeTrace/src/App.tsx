import React, { useState, useEffect, useRef } from 'react';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { ThemeProvider } from 'styled-components/native';
import { Provider } from 'react-redux';
import Config from 'react-native-config';
import * as Permissions from 'expo-permissions';
import * as Location from 'expo-location';

import useLinking from './navigation/useLinking';
import RootNavigator from './navigation/RootNavigator';
import { Theme } from '../Theme';
import { store } from './store';
import { BaseLayout } from './components';
import {
  setRemoteConfigDefaults,
  fetchRemoteConfigs,
  readRemoteConfigs,
  persistRemoteConfigs,
  Logger,
} from './services';

interface IProps {
  skipLoadingScreen?: any;
}

if (__DEV__) {
  new Logger({ enableLog: true });
  console.log('Environment Variables: ', Config);
}

export default (props: IProps) => {
  const [isLoadingComplete, setLoadingComplete] = useState(false);
  const [initialNavigationState, setInitialNavigationState] = React.useState();
  const containerRef = useRef();
  const { getInitialState } = useLinking(containerRef);

  useEffect(() => {
    // alert(JSON.stringify(NativeModulesProxy.ExpoLocation));

    const loadResourcesAndDataAsync = async () => {
      try {
        // Load our initial navigation state
        setInitialNavigationState((await getInitialState()) as any);
      } catch (e) {
        // We might want to provide this error information to an error reporting service
        console.info(e);
      } finally {
        setLoadingComplete(true);
      }
    };

    const getLocationAsync = async () => {
      // permissions returns only for location permissions on iOS and under certain conditions, see Permissions.LOCATION
      const { status } = await Permissions.askAsync(Permissions.LOCATION);
      if (status === 'granted') {
        return Location.getCurrentPositionAsync({ enableHighAccuracy: true });
      } else {
        throw new Error('Location permission not granted');
      }
    };

    const getNotificationAsync = async () => {
      const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);
      if (status !== 'granted') {
        throw new Error('Notification permission not granted');
      }
    };

    const checkMultiPermissions = async () => {
      const { status } = await Permissions.getAsync(
        Permissions.LOCATION,
        Permissions.NOTIFICATIONS
      );
      if (status !== 'granted') {
        getLocationAsync();
        getNotificationAsync();
      }
    };

    loadResourcesAndDataAsync();
    checkMultiPermissions();
    setRemoteConfigDefaults()
      .then(() => fetchRemoteConfigs())
      .then(() => readRemoteConfigs())
      .then((configs) => {
        persistRemoteConfigs(configs);
      });
  }, []);

  if (!isLoadingComplete && !props.skipLoadingScreen) {
    return (
      <SafeAreaProvider>
        <BaseLayout />
      </SafeAreaProvider>
    );
  } else {
    return (
      <SafeAreaProvider>
        <SafeAreaView style={{ flex: 1 }}>
          <ThemeProvider theme={Theme}>
            <Provider store={store}>
              <RootNavigator
                containerRef={containerRef}
                initialState={initialNavigationState}
              />
            </Provider>
          </ThemeProvider>
        </SafeAreaView>
      </SafeAreaProvider>
    );
  }
};

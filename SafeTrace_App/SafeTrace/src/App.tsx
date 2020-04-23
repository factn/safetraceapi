import React, { useState, useEffect, useRef } from 'react';
import { SafeAreaView } from 'react-native';
import { ThemeProvider } from 'styled-components/native';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import Config from 'react-native-config';

import useLinking from './navigation/useLinking';
import RootNavigator from './navigation/RootNavigator';
import { Theme } from '../Theme';
import { configureStore } from './store';
import { BaseLayout } from './components';
import { setRemoteConfigDefaults, fetchRemoteConfigs, readRemoteConfigs, persistRemoteConfigs, Logger } from './services';

interface IProps {
  skipLoadingScreen?: any;
}

export default (props: IProps) => {
  const [isLoadingComplete, setLoadingComplete] = useState(false);
  const [initialNavigationState, setInitialNavigationState] = React.useState();
  const containerRef = useRef();
  const { getInitialState } = useLinking(containerRef);
  const storeRef = configureStore();

  if (__DEV__) {
    Logger();
    console.log('Environment Variables: ', Config);
  }

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

    loadResourcesAndDataAsync();
    setRemoteConfigDefaults()
      .then(() => fetchRemoteConfigs())
      .then(() => readRemoteConfigs())
      .then((configs) => {
        persistRemoteConfigs(configs);
      });
  }, []);

  if (!isLoadingComplete && !props.skipLoadingScreen) {
    return (
      <SafeAreaView>
        <BaseLayout />
      </SafeAreaView>
    );
  } else {
    return (
      <SafeAreaView style={{ flex: 1 }}>
        <BaseLayout>
          <ThemeProvider theme={Theme}>
            <Provider store={storeRef.store}>
              <PersistGate loading={null} persistor={storeRef.persistor}>
                <RootNavigator
                  containerRef={containerRef}
                  initialState={initialNavigationState}
                />
              </PersistGate>
            </Provider>
          </ThemeProvider>
        </BaseLayout>
      </SafeAreaView>
    );
  }
};

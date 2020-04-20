import React, { useState, useEffect, useRef } from 'react';
import { SafeAreaView } from 'react-native';
import { ThemeProvider } from 'styled-components/native';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';

import useLinking from './navigation/useLinking';
import RootNavigator from './navigation/RootNavigator';
import { Theme } from '../Theme';
import { configureStore } from './store';
import { BaseLayout } from './components';

interface IProps {
  skipLoadingScreen?: any;
}

export default (props: IProps) => {
  const [isLoadingComplete, setLoadingComplete] = useState(false);
  const [initialNavigationState, setInitialNavigationState] = React.useState();
  const containerRef = useRef();
  const { getInitialState } = useLinking(containerRef);
  const storeRef = configureStore();

  useEffect(() => {
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

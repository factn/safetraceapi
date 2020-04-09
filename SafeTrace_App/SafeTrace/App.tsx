import React, { useState, useEffect, useRef } from "react";
import { Platform, StatusBar } from "react-native";
import { SplashScreen } from "expo";
import * as Font from "expo-font";
import { Ionicons } from "@expo/vector-icons";
import { ThemeProvider } from "styled-components/native";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";

import { BaseLayout } from "./styles";
import useLinking from "./navigation/useLinking";
import RootNavigator from "./navigation/RootNavigator";
import { Theme } from "./Theme";
import { configureStore } from "./store";

interface IProps {
  skipLoadingScreen: any;
}

export default function App(props: IProps) {
  const [isLoadingComplete, setLoadingComplete] = useState(false);
  const [initialNavigationState, setInitialNavigationState] = React.useState();
  const containerRef = useRef();
  const { getInitialState } = useLinking(containerRef);
  const storeRef = configureStore();

  const StatusBarNode = Platform.OS === "ios" && (
    <StatusBar barStyle="default" />
  );

  useEffect(() => {
    const loadResourcesAndDataAsync = async () => {
      try {
        SplashScreen.preventAutoHide();

        // Load our initial navigation state
        setInitialNavigationState((await getInitialState()) as any);

        // Load fonts
        await Font.loadAsync({
          ...Ionicons.font,
          "space-mono": require("./assets/fonts/SpaceMono-Regular.ttf"),
        });
      } catch (e) {
        // We might want to provide this error information to an error reporting service
        console.warn(e);
      } finally {
        setLoadingComplete(true);
        SplashScreen.hide();
      }
    };

    loadResourcesAndDataAsync();
  }, []);

  if (!isLoadingComplete && !props.skipLoadingScreen) {
    return <BaseLayout></BaseLayout>;
  } else {
    return (
      <BaseLayout>
        {StatusBarNode}
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
    );
  }
}

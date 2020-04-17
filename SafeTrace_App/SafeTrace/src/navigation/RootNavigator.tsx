import React, { useRef, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import BottomTabNavigator from './BottomTabNavigator';
import { SplashScreen } from '../screens/SplashScreen';
import { HomeScreen } from '../screens/HomeScreen';
import { MapScreen } from '../screens/MapScreen';

const Stack = createStackNavigator();

interface IProps {
  containerRef: any;
  initialState: any;
}

export default (props: IProps) => {
  const { containerRef, initialState } = props;
  return (
    <NavigationContainer
      ref={containerRef}
      initialState={initialState}
    >
      <Stack.Navigator headerMode="none">
        {/* <Stack.Screen name="Root" component={BottomTabNavigator} /> */}
        {/*<Stack.Screen
          name="Splash"
          component={SplashScreen}
        />
        <Stack.Screen
          name="home"
          component={HomeScreen}
        />*/}
        <Stack.Screen
          name="location"
          component={MapScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

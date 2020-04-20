import React, { useRef, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import BottomTabNavigator from './BottomTabNavigator';
import { SplashScreen } from '../screens/SplashScreen';
import { TestScreen } from '../screens/TestScreen';

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
      <Stack.Navigator headerMode="none" initialRouteName="Test">
        {/* <Stack.Screen name="Root" component={BottomTabNavigator} /> */}
        <Stack.Screen
          name="Splash"
          component={SplashScreen}
        />
        <Stack.Screen
          name="Test"
          component={TestScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

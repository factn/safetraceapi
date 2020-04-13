import React, { useRef, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import BottomTabNavigator from './BottomTabNavigator';
import { SplashScreen } from '../screens/SplashScreen';

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
      <Stack.Navigator>
        {/* <Stack.Screen name="Root" component={BottomTabNavigator} /> */}
        <Stack.Screen name="Splash" component={SplashScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

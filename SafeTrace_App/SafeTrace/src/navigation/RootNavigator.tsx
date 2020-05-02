import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import BottomTabNavigator from './BottomTabNavigator';
import { SplashScreen } from '../screens/SplashScreen';
import TestBottomTabNav from '../screens/TestScreen';
import { OnboardScreen } from '../screens/OnboardScreen';
import { StatusUpdateScreen } from '../screens/StatusUpdateScreen';
import { StatusSubmitScreen } from '../screens/StatusSubmitScreen';
import { HeatmapScreen } from '../screens/HeatmapScreen';
import { AccountScreen } from '../screens/AccountScreen';

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
      <Stack.Navigator headerMode="none" initialRouteName="TestBottomTabNav">
        {/* <Stack.Screen name="Root" component={BottomTabNavigator} /> */}
        <Stack.Screen
          name="Test"
          component={TestBottomTabNav}
        />
        <Stack.Screen
          name="Splash"
          component={SplashScreen}
        />
        <Stack.Screen
          name="Onboard"
          component={OnboardScreen}
        />
        <Stack.Screen
          name="UpdateStatus"
          component={StatusUpdateScreen}
        />
        <Stack.Screen
          name="SubmitStatus"
          component={StatusSubmitScreen}
        />
        <Stack.Screen
          name="Heatmap"
          component={HeatmapScreen}
        />
        <Stack.Screen
          name="Account"
          component={AccountScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

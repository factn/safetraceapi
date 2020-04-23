import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import * as React from 'react';

import { LocationScreen } from '../TestScreen/LocationScreen';
import { MPCScreen } from '../TestScreen/MPCScreen';
import TabBarIcon from '../../components/TabBarIcon';
// TODO: update this

interface ITabNavProps {
  navigation: any;
  route: any;
}

const BottomTab = createBottomTabNavigator();
const INITIAL_ROUTE_NAME = 'MPC';

export default function BottomTabNavigator({
  navigation,
  route,
}: ITabNavProps) {
  // Set the header title on the parent stack navigator depending on the
  // currently active tab. Learn more in the documentation:
  // https://reactnavigation.org/docs/en/screen-options-resolution.html
  navigation.setOptions({ headerTitle: getHeaderTitle(route) });

  return (
    <BottomTab.Navigator initialRouteName={INITIAL_ROUTE_NAME}>
      <BottomTab.Screen
        name="MPC"
        component={MPCScreen}
        options={{
          title: 'MPC Test',
          tabBarIcon: ({ focused }) => (
            <TabBarIcon focused={focused} name="md-code-working" />
          ),
        }}
      />
      <BottomTab.Screen
        name="Location"
        component={LocationScreen}
        options={{
          title: 'Location Test',
          tabBarIcon: ({ focused }) => (
            <TabBarIcon focused={focused} name="md-book" />
          ),
        }}
      />
    </BottomTab.Navigator>
  );
}

function getHeaderTitle(route: any) {
  const routeName =
    route.state?.routes[route.state.index]?.name ?? INITIAL_ROUTE_NAME;

  switch (routeName) {
    case 'Home':
      return 'SafeTrace';
    case 'Links':
      return 'Links to learn more';
    // TODO: update for privacy, etc. tabs
  }
}

import * as React from 'react';

import { Colors } from '../constants';

interface IProps {
  name: string;
  focused: boolean;
}

export default function TabBarIcon(props: IProps) {
  // return (
  //   <Ionicons
  //     name={props.name}
  //     size={30}
  //     style={{ marginBottom: -3 }}
  //     color={props.focused ? Colors.tabIconSelected : Colors.tabIconDefault}
  //   />
  // );
  return null;
}

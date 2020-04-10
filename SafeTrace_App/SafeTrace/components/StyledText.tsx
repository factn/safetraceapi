import * as React from 'react';
import { Text } from 'react-native';

interface IProps {
  style: any;
}

export const MonoText = (props: IProps) => {
  return <Text {...props} style={[props.style, { fontFamily: 'space-mono' }]} />;
}

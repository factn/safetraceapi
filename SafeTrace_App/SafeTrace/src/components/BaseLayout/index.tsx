import React, { ReactNode } from 'react';
import { StatusBar } from 'react-native';

import { RootContainer } from './styles';

interface IProps {
  children?: ReactNode;
}

export const BaseLayout = (props: IProps) => {
  const { children } = props;
  return (
    <RootContainer {...props}>
      <StatusBar barStyle="default" backgroundColor="#FFFFFF" />
      {children}
    </RootContainer>
  );
};

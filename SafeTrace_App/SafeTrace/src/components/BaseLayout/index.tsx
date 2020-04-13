import React, { ReactNode } from 'react';

import {
  RootContainer
} from './styles';

interface IProps {
  children?: ReactNode;
}

export const BaseLayout = (props: IProps) => {
  const { children } = props;
  return (
    <RootContainer>
      {children}
    </RootContainer>
  );
}
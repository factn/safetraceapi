import React from 'react';

import {
  ButtonContainer,
  ButtonLabel
} from './style';

interface IProps {
  label: string;
  onPress: any;
  style?: any;
  disabled?: boolean;
  inverted?: boolean;
}

export const Button = (props: IProps) => {
  const { label, onPress, style, disabled, inverted } = props;
  return (
    <ButtonContainer onPress={onPress} activeOpacity={0.7} style={style} disabled={disabled} inverted={inverted}>
      <ButtonLabel inverted={inverted}>
        {label}
      </ButtonLabel>
    </ButtonContainer>
  );
}
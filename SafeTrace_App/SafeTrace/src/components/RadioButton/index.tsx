import React from 'react';

import {
  RadioButtonWrapper,
  SelectedRadio,
  Label,
  RadioCircle,
  LabelWrapper,
} from './style';

interface IProps {
  id: string | number;
  label: string;
  onPress: any;
  value: string;
}

export const RadioButton = (props: IProps) => {
  const { id, label, onPress, value } = props;

  return (
    <RadioButtonWrapper key={id} onPress={() => onPress(id)} activeOpacity={0.8}>
      <RadioCircle onPress={() => onPress(id)} activeOpacity={0.6}>
        {value === id && <SelectedRadio />}
      </RadioCircle>
      <LabelWrapper>
        <Label>{label}</Label>
      </LabelWrapper>
    </RadioButtonWrapper>
  );
};

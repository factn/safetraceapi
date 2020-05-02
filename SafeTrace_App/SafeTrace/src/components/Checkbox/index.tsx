import React from 'react';

import {
  CheckboxWrapper,
  SelectedCheckbox,
  Label,
  Checkbox as CheckboxElem,
  LabelWrapper,
} from './style';

interface IProps {
  id: string | number;
  label: string;
  onPress: any;
  isActive: boolean;
}

export const Checkbox = (props: IProps) => {
  const { id, label, onPress, isActive } = props;

  return (
    <CheckboxWrapper key={id} onPress={() => onPress(id)} activeOpacity={0.8}>
      <CheckboxElem onPress={() => onPress(id)} activeOpacity={0.6}>
        {isActive && <SelectedCheckbox />}
      </CheckboxElem>
      <LabelWrapper>
        <Label>{label}</Label>
      </LabelWrapper>
    </CheckboxWrapper>
  );
};

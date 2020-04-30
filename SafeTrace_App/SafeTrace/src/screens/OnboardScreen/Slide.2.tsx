import React from 'react';

import {
  SlideContainer,
  Icon,
  IconWrapper,
  SafeTraceLogoText,
  SlideDescription
} from './styles';
import { Button } from '../../components';

interface IProps {
  getSwiper?: any;
}

export const Slide2 = (props: IProps) => {
  const { getSwiper } = props;
  return (
    <SlideContainer>
      <IconWrapper>
        <Icon name="plus-square" size={80} />
      </IconWrapper>
      <SafeTraceLogoText>SafeTrace</SafeTraceLogoText>
      <SlideDescription>Update your status and symptoms in the app to help track the spread of COVID-19</SlideDescription>
      <Button label="Next" style={{ marginTop: 16 }} onPress={() => {
        if (!!getSwiper) {
          getSwiper().scrollBy(1);
        }
      }} />
    </SlideContainer>
  );
}
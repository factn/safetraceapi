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

export const Slide1 = (props: IProps) => {
  const { getSwiper } = props;
  return (
    <SlideContainer>
      <IconWrapper>
        <Icon name="users" size={80} />
      </IconWrapper>
      <SafeTraceLogoText>SafeTrace</SafeTraceLogoText>
      <SlideDescription>Get alerted when you might have come into contact with someone with COVID-19</SlideDescription>
      <Button label="Next" style={{ marginTop: 16 }} onPress={() => {
        if (!!getSwiper) {
          getSwiper().scrollBy(1);
        }
      }} />
    </SlideContainer>
  );
}
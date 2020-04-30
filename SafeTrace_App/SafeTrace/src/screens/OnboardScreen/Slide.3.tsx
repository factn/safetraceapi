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
  getNavigation?: any;
}

export const Slide3 = (props: IProps) => {
  const { getSwiper, getNavigation } = props;
  return (
    <SlideContainer>
      <IconWrapper>
        <Icon name="chart-line" size={80} />
      </IconWrapper>
      <SafeTraceLogoText>SafeTrace</SafeTraceLogoText>
      <SlideDescription>Help research organisations by anonymously sharing your data (opt-in only).</SlideDescription>
      <Button label="Get Started" style={{ marginTop: 16 }} onPress={() => {
        if (!!getNavigation) {
          getNavigation().navigate('UpdateStatus');
        }
      }} />
    </SlideContainer>
  );
}
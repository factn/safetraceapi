import React from 'react';
import Swiper from 'react-native-swiper';
import { View, Image, Text } from 'react-native';

import { RootContainer } from './styles';
import { BaseLayout } from '../../components';
import { Slide1 } from './Slide.1';
import { Slide2 } from './Slide.2';
import { Slide3 } from './Slide.3';

interface IProps {
  navigation?: any;
}

export const OnboardScreen = (props: IProps) => {
  const { navigation } = props;

  let swiperRef: any;

  return (
    <BaseLayout>
      <RootContainer>
        <Swiper showsButtons={true} loop={false} ref={_ref => swiperRef = _ref}>
          <Slide1 getSwiper={() => swiperRef} />
          <Slide2 getSwiper={() => swiperRef} />
          <Slide3 getSwiper={() => swiperRef} getNavigation={() => navigation} />
        </Swiper>
      </RootContainer>
    </BaseLayout>
  );
};

import React, { useEffect } from 'react';
import { Text } from 'react-native';

import {
  SplashScreenBackgroundCover,
  SafeTraceLogo,
  SafeTraceLogoText,
  SafeTraceLogoContainer,
  Loader,
} from './styles';
import { BaseLayout } from '../../components';

export const SplashScreen = () => {
  let animation: any;

  useEffect(() => {
    animation.play();
  });

  return (
    <BaseLayout>
      <SplashScreenBackgroundCover
        source={require('../../media/backgrounds/4.jpg')}
      >
        <SafeTraceLogoContainer>
          <SafeTraceLogo source={require('../../media/safetrace-logo.png')} />
          <SafeTraceLogoText>SafeTrace</SafeTraceLogoText>
          <Loader
            ref={anim => animation = anim}
            source={require('../../media/animations/ecg.json')}
          />
        </SafeTraceLogoContainer>
      </SplashScreenBackgroundCover>
    </BaseLayout>
  );
};

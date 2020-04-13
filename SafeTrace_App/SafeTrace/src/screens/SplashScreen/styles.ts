import styled from 'styled-components/native';
import LottieView from 'lottie-react-native';

export const SplashScreenBackgroundCover = styled.ImageBackground`
  flex: 1;
  align-items: center;
  justify-content: center;
`;

export const SafeTraceLogoContainer = styled.View`
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
`;

export const SafeTraceLogo = styled.Image`
  transform: scale(0.5);
`;

export const SafeTraceLogoText = styled.Text`
  margin-top: -40px;
  margin-bottom: 70px;
  font-size: 30px;
  letter-spacing: 3px;
  font-family: ${props => props.theme.fonts.bold};
`;

export const Loader = styled(LottieView)`
  width: 200px;
`;
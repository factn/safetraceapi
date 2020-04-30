import styled from 'styled-components/native';
import Ico from 'react-native-vector-icons/FontAwesome5';
import { ITheme } from 'react-native';

import { BaseLayout } from '../../components';

export const RootContainer = styled(BaseLayout)``;


export const SlideContainer = styled.View<{
  theme?: ITheme;
}>`
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.theme.colors.whiteColor};
  padding: 32px;
`;

export const IconWrapper = styled.View`
  width: 250px;
  height: 250px;
  border-radius: 250px;
  background-color: #eaf4ff;
  align-items: center;
  justify-content: center;
`;

export const Icon = styled(Ico)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const SafeTraceLogoText = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.bold};
  font-size: 30px;
  color: ${props => props.theme.colors.primaryColor};
  margin-top: 16px;
`;

export const SlideDescription = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.regular};
  font-size: 18px;
  color: ${props => props.theme.colors.primaryColor};
  margin-top: 16px;
  text-align: center;
  margin-bottom: 16px;
`;
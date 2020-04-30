import styled from 'styled-components/native';
import { ITheme } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

export const NotificationBannerContainer = styled.View<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.whiteColor};
  padding: 16px;
  border-radius: 10px;
  flex-direction: row;
  align-items: flex-start;
`;

export const NotificationIconWrapper = styled.View`
  width: 80px;
  height: 80px;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: #eaf4ff;
  border-radius: 80px;
`;

export const NotificationIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const NotificationInfo = styled.View`
  flex-direction: column;
  padding: 0 16px;
`;

export const NotificationTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.bold};
  color: ${props => props.theme.colors.primaryColor};
  font-size: 20px;
`;

export const NotificationTime = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.bold};
  color: ${props => props.theme.colors.primaryColor};
  text-transform: uppercase;
  margin: 8px 0;
`;

export const NotificationDesc = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.regular};
  color: ${props => props.theme.colors.primaryColor};
  font-size: 14px;
`;
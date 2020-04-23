import styled from 'styled-components/native';
import { StatusBar, ITheme, Platform } from 'react-native';

export const RootContainer = styled.View<{
  theme?: ITheme;
}>`
  flex: 1;
  ${props => Platform.OS === 'android' && `padding-top: ${StatusBar.currentHeight}`};
`;

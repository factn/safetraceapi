import styled from 'styled-components/native';
import { ITheme } from 'react-native';

export const ButtonContainer = styled.TouchableOpacity<{
  theme?: ITheme;
  disabled?: boolean;
  inverted?: boolean;
}>`
  width: 100%;
  height: 45px;
  background-color: ${props => !props.disabled ? (props.inverted ? props.theme.colors.whiteColor : props.theme.colors.primaryColor) : props.theme.colors.silverColor};
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  ${props => props.inverted && `
    border-color: ${props.theme.colors.primaryColor};
    border-width: 2px;
  `}
`;

export const ButtonLabel = styled.Text<{
  theme?: ITheme;
  inverted?: boolean;
}>`
  color: ${props => props.inverted ? props.theme.colors.primaryColor : props.theme.colors.whiteColor};
  font-size: 16px;
`;
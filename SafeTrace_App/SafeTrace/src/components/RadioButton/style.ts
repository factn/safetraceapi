import styled from 'styled-components/native';
import { ITheme } from 'react-native';

export const CheckboxContainer = styled.View`
  flex-direction: column;
`;

export const RadioButtonWrapper = styled.TouchableOpacity`
  flex-direction: row;
  align-items: center;
  padding: 8px 0;
  margin: 4px 0;
`;

export const SelectedRadio = styled.View<{
  theme?: ITheme;
}>`
  width: 12.5px;
  height: 12.5px;
  border-radius: 50px;
  background-color: ${props => props.theme.colors.primaryColor};
`;

export const RadioCircle = styled.TouchableOpacity<{
  theme?: ITheme;
}>`
  height: 25px;
  width: 25px;
  border-radius: 100px;
  border-color: ${props => props.theme.colors.primaryColor};
  border-width: 2px;
  align-items: center;
  justify-content: center;
`;

export const LabelWrapper = styled.Text<{
  theme?: ITheme;
}>`
  margin-left: 16px;
`;

export const Label = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 18px;
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.semiBold};
`;
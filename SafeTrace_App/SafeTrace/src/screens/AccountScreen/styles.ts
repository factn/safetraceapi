import styled from 'styled-components/native';
import { ITheme } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

export const RootContainer = styled.ScrollView`
  
`;

export const AccountHeader = styled.View<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.whiteColor};
  padding: 16px;
  margin: 16px 0;
  border-radius: 10px;
`;

export const AccountTitle = styled.Text<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
  font-size: 20px;
  font-family: ${props => props.theme.fonts.bold};
`;

export const AccountCard = styled.View<{
  theme?: ITheme;
}>`
  padding: 16px;
  background-color: ${props => props.theme.colors.whiteColor};
  border-radius: 10px;
`;

export const AccountCardHeader = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.bold};
  font-size: 20px;
  color: ${props => props.theme.colors.primaryColor};
`;

export const AccountCardDesc = styled.Text<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.regular};
  font-size: 15px;
  margin: 8px 0;
`;

export const ModalContainer = styled.View<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.whiteColor};
  padding: 16px;
`;

export const AvatarWrapper = styled.View`
  background-color: #eaf4ff;
  width: 100px;
  height: 100px;
  border-radius: 10px;
  align-items: center;
  justify-content: center;
  align-self: center;
`;

export const AvatarIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const DeleteTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 20px;
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.bold};
  align-self: center;
  margin: 16px;
`;

export const DeleteConfirmation = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 16px;
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.regular};
  align-self: center;
  margin-bottom: 8px;
`;

export const DeleteInfo = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 16px;
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.regular};
  align-self: center;
`;
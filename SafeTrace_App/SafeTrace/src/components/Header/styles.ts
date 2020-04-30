import styled from 'styled-components/native';
import { ITheme } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

export const HeaderContainer = styled.View<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.whiteColor};
  flex-direction: column;
  padding: 16px;
`;

export const HeaderNavigation = styled.View`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

export const HeaderTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 30px;
  color: ${props => props.theme.colors.primaryColor};
  font-family: ${props => props.theme.fonts.bold};
  font-weight: bold;
`;

export const AccountButton = styled.TouchableOpacity``;

export const AccountIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const EmptyFillView = styled.View`
  flex: 1;
`;

export const BackButton = styled.TouchableOpacity``;

export const BackIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;
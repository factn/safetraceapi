import styled from 'styled-components/native';
import Icon from 'react-native-vector-icons/FontAwesome5';

import { BaseLayout } from '../../components';
import { ITheme } from 'react-native';

export const RootContainer = styled.ScrollView<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.primaryBackground};
`;

export const PromptCardContainer = styled.View<{
  theme?: ITheme;
}>`
  margin: 16px 0;
  background-color: ${props => props.theme.colors.whiteColor};
  border-radius: 10px;
  padding: 16px;
  flex-direction: column;
`;

export const PromptHeader = styled.View`
  flex-direction: column;
  margin-bottom: 16px;
`;

export const PromptTitleWrapper = styled.View`
  flex-direction: row;
  align-items: center;
`;

export const PromptHeaderTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 18px;
  font-weight: bold;
  font-family: ${props => props.theme.fonts.bold};
  color: ${props => props.theme.colors.primaryColor};
`;

export const PromptHeaderSubtitle = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 15px;
  font-family: ${props => props.theme.fonts.regular};
  color: ${props => props.theme.colors.primaryColor};
  margin: 8px 0;
`;

export const HeaderIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
  margin-right: 16px;
`;
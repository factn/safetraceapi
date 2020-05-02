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

export const StatusSubmittedContainer = styled.View<{
  theme?: ITheme;
}>`
  background-color: ${props => props.theme.colors.whiteColor};
  padding: 16px;
  flex-direction: column;
`;

export const StatusListItem = styled.View`
  flex-direction: row;
  align-items: center;
  margin-bottom: 16px;
`;

export const StatusListItemIconWrapper = styled.View<{
  theme?: ITheme;
}>`
  width: 80px;
  height: 80px;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: #eaf4ff;
  border-radius: 80px;
`;

export const StatusListItemIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const StatusListItemInfo = styled.View`
  padding: 0 16px;
`;

export const StatusListItemTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.bold};
  font-size: 20px;
  color: ${props => props.theme.colors.primaryColor};
  letter-spacing: 0.5px;
`;

export const StatusListItemLabel = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.regular};
  font-size: 15px;
  color: ${props => props.theme.colors.primaryColor};
  margin: 8px 0;
  letter-spacing: 0.5px;
`;

export const StatusListItemSymptoms = styled.View`
  flex-direction: column;
  margin-top: 8px;
`;

export const SymptomLabel = styled.Text<{
  theme?: ITheme;
}>`
  font-family: ${props => props.theme.fonts.regular};
  font-size: 15px;
  color: ${props => props.theme.colors.primaryColor};
  letter-spacing: 0.5px;
`;
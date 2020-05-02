import styled from 'styled-components/native';
import { ITheme } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';

export const HeatmapContainer = styled.View<{
  theme?: ITheme;
}>`
  margin: 16px 0;
  background-color: ${props => props.theme.colors.whiteColor};
  border-radius: 10px;
  padding: 16px;
  flex-direction: column;
`;

export const HeatmapPlaceholder = styled.Image``;

export const HeatmapHeader = styled.View`
  flex-direction: row;
  align-items: center;
  margin-bottom: 16px;
  justify-content: space-between;
`;

export const HeatmapHeaderTitleWrapper = styled.View`
  position: relative;
  padding: 0;
  margin: 0;
`;

export const HeatmapHeaderTitle = styled.Text<{
  theme?: ITheme;
}>`
  font-size: 18px;
  font-weight: bold;
  font-family: ${props => props.theme.fonts.bold};
  color: ${props => props.theme.colors.primaryColor};
`;

export const HeatmapMoreButton = styled.TouchableOpacity``;

export const HeatmapMoreIcon = styled(Icon)<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.primaryColor};
`;

export const HeatmapNotificaitonBadge = styled.View`
  position: absolute;
  top: -15px;
  right: -25px;
  padding: 4px;
  border-radius: 25px;
  background-color: #3ad477;
  width: 25px;
  height: 25px;
  align-items: center;
  justify-content: center;
`;

export const HeatmapNotificationBadgeLabel = styled.Text<{
  theme?: ITheme;
}>`
  color: ${props => props.theme.colors.whiteColor};
`;
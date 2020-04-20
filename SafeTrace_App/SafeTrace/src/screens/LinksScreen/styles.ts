import styled from 'styled-components/native';
import { StyleSheet } from 'react-native';
import { ScrollView, RectButton } from 'react-native-gesture-handler';

export const BaseLayout = styled(ScrollView)`
  flex: 1;
  background-color: #fafafa;
`;

export const OptionButtonContainer = styled(RectButton)<{
  lastOption?: boolean;
}>`
  background-color: #fdfdfd;
  padding-vertical: 15px;
  border-width: ${StyleSheet.hairlineWidth};
  border-bottom-width: ${props => props.lastOption ? StyleSheet.hairlineWidth : 0}px;
  border-color: #ededed;
`;

export const OptionIconContainer = styled.View`
  margin-right: 15px;
`;

export const OptionLabelContainer = styled.View`

`;

export const OptionLabel = styled.Text`
  font-size: 15px;
  align-self: flex-start;
  margin-top: 1px;
`;
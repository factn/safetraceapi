import styled from 'styled-components/native';
import { ITheme } from 'react-native';

/********* Location List Styles *********/
export const LocationListViewContainer = styled.View`
  flex: 1;
  flex-direction: column;
  background-color: #FFFFFF;
  padding: 16px 0;
`;

export const LocationListViewItem = styled.View`
  flex-direction: row;
  height: 50px;
  align-items: center;
  background-color: #FFFFFF;
  border-bottom-color: rgba(0, 0, 0, 0.1);
  border-bottom-width: 1px;
`;

export const LocationListViewLabel = styled.Text<{
  theme?: ITheme
}>`
  flex: 0.75;
  padding-left: 16px;
  font-size: 17px;
  font-weight: bold;
  font-family: ${props => props.theme.fonts.semiBold};
`;

export const LocationListViewValue = styled.Text<{
  theme?: ITheme
}>`
  flex: 1;
  font-size: 15px;
  font-family: ${props => props.theme.fonts.regular};
`;
/********* Location List Styles *********/

/********* MPC Styles *********/
export const MPCDetailsScrollView = styled.ScrollView`
  flex: 1;
  padding: 16px;
`;

export const ShareSplitInput = styled.Text<{
  theme?: ITheme
}>`
    font-family: ${props => props.theme.fonts.regular};
    font-size: 15px;
`;

export const ShareSplitOutput = styled.Text<{
  theme?: ITheme
}>`
    font-family: ${props => props.theme.fonts.regular};
    font-size: 15px;
`;

export const ShareJoinInput = styled.Text<{
  theme?: ITheme
}>`
    font-family: ${props => props.theme.fonts.regular};
    font-size: 15px;
    margin-top: 20px;
`;

export const ShareJoinOutput = styled.Text<{
  theme?: ITheme
}>`
    font-family: ${props => props.theme.fonts.regular};
    font-size: 15px;
    padding-bottom: 50px;
`;
/********* MPC Styles *********/
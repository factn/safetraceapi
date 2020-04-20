import styled from 'styled-components/native';
import { StatusBar } from 'react-native';

export const RootContainer = styled.View`
  flex: 1;
  padding-top: ${StatusBar.currentHeight}%;
`;
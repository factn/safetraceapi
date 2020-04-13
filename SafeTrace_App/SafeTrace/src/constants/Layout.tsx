import { Dimensions, IThemeLayout } from 'react-native';

const width = Dimensions.get('window').width;
const height = Dimensions.get('window').height;

export const Layout: IThemeLayout = {
  window: {
    width,
    height,
  },
  isSmallDevice: width < 375,
};

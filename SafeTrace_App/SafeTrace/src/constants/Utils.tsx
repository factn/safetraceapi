import { Platform, IThemeUtils } from 'react-native';

export const Utils: IThemeUtils = {
  isIOS: Platform.OS === 'ios',
  isAndroid: Platform.OS === 'android',
};
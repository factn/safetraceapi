import 'react-native';

declare module 'react-native' {
  export interface IThemeFonts {
    bold: string;
    italic: string;
    light: string;
    regular: string;
    semiBold: string;
  }
  
  export interface IThemeLayout {
    window: {
      width: number;
      height: number;
    }
    isSmallDevice: boolean;
  }
  
  export interface IThemeColors {
    tintColor: string;
    primaryColor: string;
    primaryColor2: string;
    primaryBackground: string;
    tabIconDefault: string;
    tabIconSelected: string;
    tabBar: string;
    errorBackground: string;
    errorText: string;
    warningBackground: string;
    warningText: string;
    noticeBackground: string;
    noticeText: string;
    whiteColor: string;
    silverColor: string;
  }

  export interface IThemeUtils {
    isIOS: boolean;
    isAndroid: boolean;
  }
  
  export interface ITheme {
    fonts: IThemeFonts;
    colors: IThemeColors;
    layout: IThemeLayout;
    utils: IThemeUtils;
  }
}
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
    tabIconDefault: string;
    tabIconSelected: string;
    tabBar: string;
    errorBackground: string;
    errorText: string;
    warningBackground: string;
    warningText: string;
    noticeBackground: string;
    noticeText: string;
  }
  
  export interface ITheme {
    fonts: IThemeFonts;
    colors: IThemeColors;
    layout: IThemeLayout;
  }
}
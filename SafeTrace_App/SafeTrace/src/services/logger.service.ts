import Reactotron from 'reactotron-react-native';
import AsyncStorage from '@react-native-community/async-storage';
import Config from 'react-native-config';

export const Logger = () => {
  if (Reactotron !== undefined) {
    (Reactotron as any)
      .setAsyncStorageHandler(AsyncStorage)
      .configure({
        name: 'SafeTrace App',
        host: Config.LOG_HOST,
      })
      .useReactNative({
        asyncStorage: false,
        networking: {
          ignoreUrls: /symbolicate/,
        },
        editor: false,
        errors: {veto: (_stackFrame: any) => false},
        overlay: false,
      })
      .connect();
  }
};

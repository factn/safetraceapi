import Reactotron from 'reactotron-react-native';
import AsyncStorage from '@react-native-community/async-storage';
import Config from 'react-native-config';

export class Logger {
  private isLogEnabled: boolean = false;
  constructor(options: any = {}) {
    this.isLogEnabled = options.enableLog ? options.enableLog : false;

    if (!!Config && !!Config.LOG_HOST) {
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
          errors: { veto: (_stackFrame: any) => false },
          overlay: false,
        })
        .connect();

      this.connectConsoleToReactotron();
    }
  }

  enableLog(): void {
    this.isLogEnabled = true;
  }

  disableLog(): void {
    this.isLogEnabled = false;
  }

  logEnabled(): boolean {
    return this.isLogEnabled;
  }

  connectConsoleToReactotron() {
    // console.info = Reactotron.display as any;
    // console.log = Reactotron.display as any;
    // console.warn = Reactotron.display as any;
    // console.error = Reactotron.display as any;
    console.log = this.log;
  }

  log(message: string, ...args: any[]) {
    if (!__DEV__) { return; }
    Reactotron.display({
      name: 'LOG',
      preview: message,
      value: { message, args },
    });
  }

  info(message: string, ...args: any[]) {
    if (!__DEV__) { return; }
    Reactotron.display({
      name: 'INFO',
      preview: message,
      value: { message, args },
    });
  }

  warn(message: string, ...args: any[]) {
    if (!__DEV__) { return; }
    Reactotron.display({
      name: 'WARN',
      preview: message,
      value: { message, args },
      important: true,
    });
  }

  error(message: string, ...args: any[]) {
    if (!__DEV__) { return; }
    Reactotron.display({
      name: 'ERROR',
      preview: message,
      value: { message, args },
      important: true,
    });
  }
}

import remoteConfig from '@react-native-firebase/remote-config';
import AsyncStorage from '@react-native-community/async-storage';

const REMOTE_CONFIG_STORAGE_KEY = 'RemoteConfigStorage';

export const setRemoteConfigDefaults = () => {
  return remoteConfig()
  .setDefaults({
    config_android_analytics_status: 'disabled',
    config_ios_analytics_status: 'disabled',
  })
  .then(() => {
    console.info('Default values for Remote Config is set.');
  });
}

export const fetchRemoteConfigs = () => {
  return remoteConfig()
  .fetchAndActivate()
  .then((activated) => {
    if (activated) {
      console.info('Fetched from Remote Config and Activated.')
    } else {
      console.warn('Fetched from Remote Config and Failed Activation.');
    }
  });
}

export const readRemoteConfigs = () => ({
  configAndroidAnalyticsEnabled: getById('config_android_analytics_status'),
  configIOSAnalyticsEnabled: getById('config_ios_analytics_status'),
});

export const persistRemoteConfigs = (dataToPersist: any) => {
  AsyncStorage.setItem(REMOTE_CONFIG_STORAGE_KEY, JSON.stringify(dataToPersist));
}

export const rehydrateRemoteConfigs = async () => {
  const vals = await AsyncStorage.getItem(REMOTE_CONFIG_STORAGE_KEY);
  const valsToHydrate = !!vals ? vals : '{}';
  return JSON.parse(valsToHydrate);
}

const getById = (id: string) => {
  return remoteConfig().getValue(id);
}
import i18n from 'i18next';
import {initReactI18next} from 'react-i18next';

import * as EN from '../i18n/en.json';
import * as FR from '../i18n/fr.json';

const resources = {
  en: EN,
  fr: FR,
};

i18n.use(initReactI18next).init({
  resources,
  ns: ['common'],
  lng: 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

export {i18n};

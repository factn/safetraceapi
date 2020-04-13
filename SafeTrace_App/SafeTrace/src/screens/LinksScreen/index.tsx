import React from 'react';
import { View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { WebBrowser } from 'expo';

import {
  BaseLayout,
  OptionButtonContainer,
  OptionIconContainer,
  OptionLabelContainer,
  OptionLabel
} from './styles';

interface IOptionButtonProps {
  icon: string;
  label: string;
  onPress: any;
  isLastOption?: boolean;
}

const OptionButton = ({ icon, label, onPress, isLastOption }: IOptionButtonProps) => {
  return (
    <OptionButtonContainer lastOption={isLastOption} onPress={onPress}>
      <View style={{ flexDirection: 'row' }}>
        <OptionIconContainer>
          <Ionicons name={icon} size={22} color="rgba(0,0,0,0.35)" />
        </OptionIconContainer>
        <OptionLabelContainer>
          <OptionLabel>{label}</OptionLabel>
        </OptionLabelContainer>
      </View>
    </OptionButtonContainer>
  );
}

const LinksScreen = () => {
  return (
    <BaseLayout
      contentContainerStyle={{ paddingTop: 15 }}
    >
      <OptionButton
        icon="md-school"
        label="Read the Expo documentation"
        onPress={() => WebBrowser.openBrowserAsync('https://safetraceapi.org')}
      />

      <OptionButton
        icon="md-compass"
        label="Read the React Navigation documentation"
        onPress={() =>
          WebBrowser.openBrowserAsync('https://reactnavigation.org')
        }
      />

      <OptionButton
        icon="ios-chatboxes"
        label="Ask a question on the forums"
        onPress={() => WebBrowser.openBrowserAsync('https://forums.expo.io')}
        isLastOption={true}
      />
    </BaseLayout>
  );
};

LinksScreen.navigationOptions = {
  header: null,
};

export default LinksScreen;
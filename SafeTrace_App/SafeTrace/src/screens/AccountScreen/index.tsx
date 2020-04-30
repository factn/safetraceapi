import React, { useState } from 'react';
import Modal from 'react-native-modal';

import { BaseLayout, Header, Button } from '../../components';
import { RootContainer, AccountHeader, AccountTitle, AccountCard, AccountCardHeader, AccountCardDesc } from './styles';
import { AccountDeletionModal } from './AccountDeletionModal';
import { AccountPrivacyModal } from './AccountPrivacyModal';

interface IProps {
  navigation?: any;
}

export const AccountScreen = (props: IProps) => {
  const { navigation } = props;
  const [deletionModalVisible, setDeletionModalVisible] = useState(false);
  const [privacyModalVisible, setPrivacyModalVisible] = useState(false);

  const _renderAccountDeletionModal = () => {
    return (
      <Modal isVisible={deletionModalVisible} onBackButtonPress={() => setDeletionModalVisible(false)}>
        <AccountDeletionModal onCancel={() => setDeletionModalVisible(false)} />
      </Modal>
    );
  }

  const _renderAccountPrivacyModal = () => {
    return (
      <Modal isVisible={privacyModalVisible} onBackButtonPress={() => setPrivacyModalVisible(false)}>
        <AccountPrivacyModal onCancel={() => setPrivacyModalVisible(false)} />
      </Modal>
    );
  }

  return (
    <BaseLayout>
      <RootContainer>
        <Header hasBackBtn onBackPress={() => navigation.goBack()} hideAccount />
        <AccountHeader>
          <AccountTitle>My account</AccountTitle>
        </AccountHeader>
        <AccountCard>
          <AccountCardHeader>Privacy and data collection</AccountCardHeader>
          <AccountCardDesc>We ensure that your identity remains anonymous and the data that we collect is private.</AccountCardDesc>
          <Button label="Read about how we do this" onPress={() => setPrivacyModalVisible(true)} style={{ marginTop: 16 }} />
        </AccountCard>
        <AccountCard>
          <AccountCardHeader>Account deletion</AccountCardHeader>
          <AccountCardDesc>Deleting your account will erase any information that you've anonymously suppled as well as revoke all data sharing requests that you've approved.</AccountCardDesc>
          <Button label="Yes, please delete my account" onPress={() => setDeletionModalVisible(true)} style={{ marginTop: 16 }} />
        </AccountCard>
      </RootContainer>
      {_renderAccountDeletionModal()}
      {_renderAccountPrivacyModal()}
    </BaseLayout>
  )
}
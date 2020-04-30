import React from 'react';

import {
  ModalContainer,
  AvatarWrapper,
  AvatarIcon,
  DeleteTitle,
  DeleteConfirmation,
  DeleteInfo,
} from './styles';
import { Button } from '../../components';

interface IProps {
  onCancel?: any;
}

export const AccountPrivacyModal = (props: IProps) => {
  const { onCancel } = props;
  return (
    <ModalContainer>
      <AvatarWrapper>
        <AvatarIcon name="shield-alt" size={50} />
      </AvatarWrapper>
      <DeleteTitle>Privacy and data collection</DeleteTitle>
      <DeleteInfo>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</DeleteInfo>
      <Button inverted={true} label="OK, back to account" onPress={onCancel} style={{ marginTop: 16 }} />
    </ModalContainer>
  );
}
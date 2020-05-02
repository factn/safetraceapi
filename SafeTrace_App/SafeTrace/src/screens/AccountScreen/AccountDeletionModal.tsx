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

export const AccountDeletionModal = (props: IProps) => {
  const { onCancel } = props;
  return (
    <ModalContainer>
      <AvatarWrapper>
        <AvatarIcon name="user-circle" size={50} />
      </AvatarWrapper>
      <DeleteTitle>Delete my account</DeleteTitle>
      <DeleteConfirmation>Are you sure?</DeleteConfirmation>
      <DeleteInfo>Deleting your account cannot be undone</DeleteInfo>
      <Button label="Yes, please delete my account" onPress={() => null} style={{ marginTop: 16 }} />
      <Button inverted={true} label="No, I'd like to keep my account open" onPress={onCancel} style={{ marginTop: 16 }} />
    </ModalContainer>
  );
}
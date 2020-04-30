import React from 'react';

import {
  StatusSubmittedContainer,
  StatusListItem,
  StatusListItemIconWrapper,
  StatusListItemIcon,
  StatusListItemInfo,
  StatusListItemTitle,
  StatusListItemLabel,
  StatusListItemSymptoms,
  SymptomLabel
} from './styles';
import { Button } from '../../components';

export const StatusSubmittedCard = () => {
  const handleStatusSubmit = () => {}

  return (
    <StatusSubmittedContainer>
      <StatusListItem>
        <StatusListItemIconWrapper>
          <StatusListItemIcon name="heartbeat" size={30} />
        </StatusListItemIconWrapper>
        <StatusListItemInfo>
          <StatusListItemTitle>Your reported status</StatusListItemTitle>
          <StatusListItemLabel>Negative for COVID-19</StatusListItemLabel>
        </StatusListItemInfo>
      </StatusListItem>
      <StatusListItem>
        <StatusListItemIconWrapper>
          <StatusListItemIcon name="heartbeat" size={30} />
        </StatusListItemIconWrapper>
        <StatusListItemInfo>
          <StatusListItemTitle>Your reported symptoms</StatusListItemTitle>
          <StatusListItemSymptoms>
            <SymptomLabel>Fever</SymptomLabel>
            <SymptomLabel>Shortness of breath</SymptomLabel>
          </StatusListItemSymptoms>
        </StatusListItemInfo>
      </StatusListItem>
      <Button label="Update status or symptoms" onPress={handleStatusSubmit} style={{ marginTop: 16 }} />
    </StatusSubmittedContainer>
  );
}
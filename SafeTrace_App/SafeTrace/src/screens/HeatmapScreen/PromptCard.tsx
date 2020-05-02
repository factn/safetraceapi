import React, { useState } from 'react';

import {
  PromptCardContainer,
  PromptHeader,
  PromptHeaderTitle,
  PromptHeaderSubtitle,
} from './styles';
import { RadioButton, Button } from '../../components';

interface IOption {
  id: string | number;
  label: string;
}

interface IProps {
  navigation?: any;
}

const options: IOption[] = [
  {
    id: 1,
    label: 'I tested positive',
  },
  {
    id: 0,
    label: 'I tested negative',
  },
  {
    id: -1,
    label: 'I haven\'t had a medical test',
  },
];

export const PromptCard = (props: IProps) => {
  const { navigation } = props;
  const [status, setStatus] = useState('');

  const handleStatusSubmit = () => {
    if (!status) {
      return;
    }
  
    alert(`Status: ${status}`);
    navigation.navigate('SubmitStatus');
  }
  
  return (
    <PromptCardContainer>
      <PromptHeader>
        <PromptHeaderTitle>
          Update your status and or symptoms
        </PromptHeaderTitle>
        <PromptHeaderSubtitle>
          Let us know if you tested positive or not for COVID-19 and if you have
          any cold or flu-like symptoms.
        </PromptHeaderSubtitle>
      </PromptHeader>
      {options.map((option) => (
        <RadioButton key={option.id} id={option.id} label={option.label} onPress={(id: string) => setStatus(id)} value={status} />
      ))}
      <Button disabled={!status} label="Continue" onPress={handleStatusSubmit} style={{ marginTop: 16 }} />
    </PromptCardContainer>
  );
};

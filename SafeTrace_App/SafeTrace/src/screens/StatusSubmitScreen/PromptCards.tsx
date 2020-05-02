import React, { useState, Fragment } from 'react';
import * as _ from 'lodash';

import {
  PromptCardContainer,
  PromptHeader,
  PromptHeaderTitle,
  PromptTitleWrapper,
  HeaderIcon,
} from './styles';
import { RadioButton, Button, Checkbox } from '../../components';

interface IOption {
  id: string | number;
  label: string;
}

const statusOptions: IOption[] = [
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

const symptomOptions: IOption[] = [
  {
    id: 1,
    label: 'Fever (measured with thermometer or not)',
  },
  {
    id: 2,
    label: 'Cough (new or worsening)',
  },
  {
    id: 3,
    label: 'Shortness of breath (new or worsening)',
  },
  {
    id: 4,
    label: 'Fatigue (new tiredness doing normal activities)',
  },
  {
    id: 5,
    label: 'Body aches',
  },
  {
    id: 6,
    label: 'Headache',
  },
  {
    id: 7,
    label: 'Diarrhea',
  },
  {
    id: 8,
    label: 'Soar throat',
  },
  {
    id: 9,
    label: 'Loss of sense of smell or taste (new or worsening)',
  },
  {
    id: 10,
    label: 'None of the above',
  },
];

export const PromptCards = () => {
  const [status, setStatus] = useState('');
  const [symptoms, setSymptoms]: any = useState([]);

  const handleStatusAndSymptomsSubmit = () => {
    if (!status && symptoms.length === 0) {
      return;
    }

    alert(`Status: ${status} - ${JSON.stringify(symptoms)}`);
  };

  const _renderStatusPrompt = () => {
    return (
      <PromptCardContainer>
        <PromptHeader>
          <PromptTitleWrapper>
            <HeaderIcon name="heartbeat" size={20} />
            <PromptHeaderTitle>
              Update your status and or symptoms
            </PromptHeaderTitle>
          </PromptTitleWrapper>
        </PromptHeader>
        {statusOptions.map((option) => (
          <RadioButton
            key={option.id}
            id={option.id}
            label={option.label}
            onPress={(id: string) => setStatus(id)}
            value={status}
          />
        ))}
      </PromptCardContainer>
    );
  };

  const _renderSymptomsPrompt = () => {
    const handleSymptomPress = (id: string | number) => {
      if (!!id) {
        const symptomsClone = _.clone(symptoms);
        const containIndex = _.findIndex(symptoms, (o) => o === id);
        console.log(symptomsClone, containIndex);

        if (containIndex === -1) {
          symptomsClone.push(id);
          setSymptoms(symptomsClone);
        } else {
          symptomsClone.splice(containIndex, 1);
          setSymptoms(symptomsClone);
        }
      }
    };

    return (
      <PromptCardContainer>
        <PromptHeader>
          <PromptTitleWrapper>
            <HeaderIcon name="vials" size={20} />
            <PromptHeaderTitle>
              If you have symptoms, what are they?
            </PromptHeaderTitle>
          </PromptTitleWrapper>
        </PromptHeader>
        {symptomOptions.map((option) => {
          return (
            <Checkbox
              key={option.id}
              id={option.id}
              label={option.label}
              onPress={(id: string) => handleSymptomPress(id)}
              isActive={symptoms.indexOf(option.id) > -1}
            />
          );
        })}
        <Button disabled={symptoms.length === 0} label="Submit" onPress={handleStatusAndSymptomsSubmit} style={{ marginTop: 16 }} />
      </PromptCardContainer>
    );
  };

  return (
    <Fragment>
      {_renderStatusPrompt()}
      {_renderSymptomsPrompt()}
    </Fragment>
  );
};

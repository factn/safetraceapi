import React from 'react';

import { RootContainer } from './styles';
import { Header, BaseLayout } from '../../components';
import { PromptCards } from './PromptCards';

interface IProps {
  navigation?: any;
}

export const StatusSubmitScreen = (props: IProps) => {
  const { navigation } = props;

  return (
    <BaseLayout>
      <RootContainer>
        <Header
          hasBackBtn={true}
          onBackPress={() => navigation.goBack()}
          onAccountPress={() => navigation.navigate('Account')}
        />
        <PromptCards />
      </RootContainer>
    </BaseLayout>
  );
};

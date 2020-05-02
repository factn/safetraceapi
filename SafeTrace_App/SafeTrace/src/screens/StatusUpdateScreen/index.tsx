import React from 'react';

import { RootContainer } from './styles';
import { Header, BaseLayout, Heatmap } from '../../components';
import { PromptCard } from './PromptCard';
import { StatusSubmittedCard } from './StatusSubmittedCard';

interface IProps {
  navigation?: any;
}

export const StatusUpdateScreen = (props: IProps) => {
  const { navigation } = props;
  return (
    <BaseLayout>
      <RootContainer>
        <Header onAccountPress={() => navigation.navigate('Account')} />
        <Heatmap showBadge={true} onMorePress={() => navigation.navigate('Heatmap')} />
        <PromptCard navigation={navigation} />
        <StatusSubmittedCard />
      </RootContainer>
    </BaseLayout>
  );
};

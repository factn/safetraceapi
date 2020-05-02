import React from "react";

import {
  HeaderContainer,
  HeaderNavigation,
  HeaderTitle,
  AccountIcon,
  AccountButton,
  EmptyFillView,
  BackButton,
  BackIcon,
} from "./styles";

interface IProps {
  hasBackBtn?: boolean;
  onBackPress?: any;
  hideAccount?: boolean;
  onAccountPress?: any;
}

export const Header = (props: IProps) => {
  const { hasBackBtn, onBackPress, hideAccount, onAccountPress } = props;

  const handleBackPress = () => {
    if (!!onBackPress) {
      onBackPress();
    }
  };

  return (
    <HeaderContainer>
      <HeaderNavigation>
        {hasBackBtn && (
          <BackButton onPress={handleBackPress}>
            <BackIcon name="angle-left" size={30} />
          </BackButton>
        )}
        <EmptyFillView />
        {!hideAccount && (
          <AccountButton onPress={onAccountPress} activeOpacity={0.8}>
            <AccountIcon name="user-circle" size={40} />
          </AccountButton>
        )}
      </HeaderNavigation>
      <HeaderTitle>SafeTrace</HeaderTitle>
    </HeaderContainer>
  );
};

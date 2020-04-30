import React from 'react';

import {
  NotificationBannerContainer,
  NotificationIconWrapper,
  NotificationIcon,
  NotificationInfo,
  NotificationTitle,
  NotificationTime,
  NotificationDesc
} from './styles';

interface IProps {
  iconName?: string;
  label?: string;
  time?: string;
  desc?: string;
}

export const NotificationBanner = (props: IProps) => {
  const { iconName, label, time, desc } = props;
  return (
    <NotificationBannerContainer>
      <NotificationIconWrapper>
        <NotificationIcon name={iconName} size={30} />
      </NotificationIconWrapper>
      <NotificationInfo>
        <NotificationTitle>{label}</NotificationTitle>
        {!!time && <NotificationTime>{time}</NotificationTime>}
        <NotificationDesc>{desc}</NotificationDesc>
      </NotificationInfo>
    </NotificationBannerContainer>
  );
}
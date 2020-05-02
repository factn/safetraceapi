import React from 'react';

import {
  HeatmapContainer,
  HeatmapPlaceholder,
  HeatmapHeaderTitle,
  HeatmapHeader,
  HeatmapMoreIcon,
  HeatmapMoreButton,
  HeatmapHeaderTitleWrapper,
  HeatmapNotificaitonBadge,
  HeatmapNotificationBadgeLabel,
} from './styles';

interface IProps {
  showBadge?: boolean;
  onMorePress?: any;
}

export const Heatmap = (props: IProps) => {
  const { showBadge, onMorePress } = props;
  return (
    <HeatmapContainer>
      <HeatmapHeader>
        <HeatmapHeaderTitleWrapper>
          <HeatmapHeaderTitle>
            Reported COVID cases in your area
          </HeatmapHeaderTitle>
          {showBadge && (
            <HeatmapNotificaitonBadge>
              <HeatmapNotificationBadgeLabel>2</HeatmapNotificationBadgeLabel>
            </HeatmapNotificaitonBadge>
          )}
        </HeatmapHeaderTitleWrapper>
        {onMorePress && (
          <HeatmapMoreButton onPress={onMorePress}>
            <HeatmapMoreIcon name="angle-right" size={24} />
          </HeatmapMoreButton>
        )}
      </HeatmapHeader>
      <HeatmapPlaceholder
        source={require('../../media/backgrounds/map_mockup.png')}
      />
    </HeatmapContainer>
  );
};

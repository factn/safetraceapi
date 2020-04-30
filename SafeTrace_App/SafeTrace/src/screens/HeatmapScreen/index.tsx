import React from "react";

import { RootContainer } from "./styles";
import {
  Header,
  BaseLayout,
  Heatmap,
  NotificationBanner,
} from "../../components";

interface IProps {
  navigation?: any;
}

export const HeatmapScreen = (props: IProps) => {
  const { navigation } = props;
  return (
    <BaseLayout>
      <RootContainer>
        <Header />
        <Heatmap showBadge={false} />
        <NotificationBanner
          iconName="flag"
          label="Potential contact notice"
          time="Yesterday around 10:11 am"
          desc="You may have come into contact with a person who reported a positive COVID status at location around time."
        />

        <NotificationBanner
          iconName="flag"
          label="We'll let you know"
          desc="If someone who reported positive for COVID-19 was in the same area at the same time as you, we'll let yo know. Not everyone reports their status and you could still have been around people with COVID-19."
        />
      </RootContainer>
    </BaseLayout>
  );
};

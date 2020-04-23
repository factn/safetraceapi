import React, { Component } from 'react';
import { View, Text } from 'react-native';
import * as Location from 'expo-location';
import Icon from 'react-native-vector-icons/FontAwesome5';
import moment from 'moment';


import {
  LocationListViewContainer,
  LocationListViewItem,
  LocationListViewLabel,
  LocationListViewValue
} from './styles';

export class LocationScreen extends Component {
  state = {
    location: {},
    error: '',
    hasPermission: '',
  };

  getPermissionsAndLocation = async () => {
    const { status } = await Location.requestPermissionsAsync();
    if (status !== 'granted') {
      this.setState({
        error: 'Permission to access location was denied',
        hasPermission: false,
      });
    } else {
      const location = await Location.getCurrentPositionAsync({});
      this.setState({ location, hasPermission: true });

      this.registerListener();
    }
  };

  registerListener = () => {
    Location.watchPositionAsync({}, (data) => {
      this.setState({ location: data });
      console.log(data);
    });
  };

  componentDidMount() {
    this.getPermissionsAndLocation();
  }

  render() {
    const { location, error } = this.state;

    if (!!error) {
      return (
        <View>
          <Text>{error}</Text>
        </View>
      );
    }

    return (
      <LocationListViewContainer>
        <LocationListViewItem>
          <LocationListViewLabel>Timestamp</LocationListViewLabel>
          <LocationListViewValue>{moment(location?.timestamp).format('YY/MM/DD-HH:mm:ss')}</LocationListViewValue>
        </LocationListViewItem>
        <LocationListViewItem>
          <LocationListViewLabel>Mocked</LocationListViewLabel>
          <LocationListViewValue>{location?.mocked ? (
            <Icon name="check" />
          ) : (
            <Icon name="times" />
          )}</LocationListViewValue>
        </LocationListViewItem>
        <LocationListViewItem>
          <LocationListViewLabel>Latitude</LocationListViewLabel>
          <LocationListViewValue>{location?.coords?.latitude}</LocationListViewValue>
        </LocationListViewItem>
        <LocationListViewItem>
          <LocationListViewLabel>Longitude</LocationListViewLabel>
          <LocationListViewValue>{location?.coords?.longitude}</LocationListViewValue>
        </LocationListViewItem>
        <LocationListViewItem>
          <LocationListViewLabel>Speed</LocationListViewLabel>
          <LocationListViewValue>{location?.coords?.speed}</LocationListViewValue>
        </LocationListViewItem>
        <LocationListViewItem>
          <LocationListViewLabel>Accuracy</LocationListViewLabel>
          <LocationListViewValue>{location?.coords?.accuracy}</LocationListViewValue>
        </LocationListViewItem>
      </LocationListViewContainer>
    );
  }
}

// timestamp, mocked, coords, altitude, longitude, speed, latitude, accuracy
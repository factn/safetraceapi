import React from 'react';
// import NavigationTestUtils from 'react-navigation/NavigationTestUtils';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';

import App from '../src/App';

jest.mock('expo', () => ({
  AppLoading: 'AppLoading',
  Linking: {
    makeUrl: jest.fn(),
  },
  SplashScreen: {
    preventAutoHide: jest.fn(),
  }
}));

const createTestProps = (props: object) => ({
  ...props
});

// jest.mock('../navigation/AppNavigator', () => 'AppNavigator');

describe('App', () => {
  jest.useFakeTimers();
  const props = createTestProps({});
  const wrapper = shallow<any>(<App {...props} />);

  console.log('--------', wrapper);

  beforeEach(() => {
    // NavigationTestUtils.resetInternalState();
  });

  it('renders correctly', () => {
    renderer.create(<App />);
  })

  // TODO: Fix test
  // it('should render a <View />', () => {
  //   expect(wrapper.find('RootNavigator')).toHaveLength(1);
  // });

  // TODO: Fix test
  // it('has 1 child', () => {
  //   const tree = renderer.create(<App />).toJSON();
  //   // expect(tree.children.length).toBe(1);
  // })

  it(`renders the loading screen`, () => {
    const tree = renderer.create(<App />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  // TODO: Fix test
  // it(`renders the root without loading screen`, () => {
  //   const tree = renderer.create(<App skipLoadingScreen={true} />).toJSON();
  //   expect(tree).toMatchSnapshot();
  // });
});

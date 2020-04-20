import React, { Component } from 'react';
import { NativeModules, Text } from 'react-native';

import { BaseLayout } from '../../components/BaseLayout';
import { ScrollView } from 'react-native-gesture-handler';

export class TestScreen extends Component {
  state = {
    splitOutput: [],
    joinOutput: '',
  };

  splitInput = '10010100001111101001000000000000';

  joinInput = [
    '{"shares": [[1, 239], [1, 100], [1, 39], [1, 12], [1, 178], [1, 233], [1, 102], [1, 195], [1, 254], [1, 16], [1, 181], [1, 186], [1, 42], [1, 11], [1, 28], [1, 2], [1, 67], [1, 108], [1, 158], [1, 76], [1, 33], [1, 86], [1, 124], [1, 191], [1, 195], [1, 83], [1, 103], [1, 125], [1, 160], [1, 149], [1, 78], [1, 128]]}',
    '{"shares": [[2, 198], [2, 200], [2, 78], [2, 27], [2, 127], [2, 202], [2, 204], [2, 157], [2, 231], [2, 32], [2, 114], [2, 108], [2, 87], [2, 21], [2, 59], [2, 4], [2, 133], [2, 216], [2, 39], [2, 155], [2, 66], [2, 172], [2, 248], [2, 101], [2, 157], [2, 166], [2, 206], [2, 250], [2, 91], [2, 49], [2, 156], [2, 27]]}',
    '{"shares": [[3, 40], [3, 172], [3, 105], [3, 22], [3, 205], [3, 34], [3, 170], [3, 94], [3, 25], [3, 48], [3, 198], [3, 215], [3, 124], [3, 31], [3, 38], [3, 6], [3, 199], [3, 180], [3, 185], [3, 214], [3, 99], [3, 250], [3, 132], [3, 218], [3, 94], [3, 245], [3, 169], [3, 135], [3, 251], [3, 164], [3, 210], [3, 155]]}',
  ];

  componentDidMount() {
    NativeModules.MPCModule.splitShares(this.splitInput)
      .then((data: string) => {
        this.setState({
          splitOutput: data,
        });
      })
      .catch((err: any) => alert('err: ' + err));

    NativeModules.MPCModule.joinShares(this.joinInput)
      .then((data: any) => {
        this.setState({
          joinOutput: data,
        });
      })
      .catch((err: any) => alert('err: ' + err));
  }

  render() {
    const { splitOutput, joinOutput } = this.state;
    return (
      <BaseLayout>
        <ScrollView>
          <Text>Input: {this.splitInput}</Text>
          <Text>Output: {JSON.stringify(splitOutput)}</Text>

          <Text>Input: {JSON.stringify(this.joinInput)}</Text>
          <Text>Output: {joinOutput}</Text>
        </ScrollView>
      </BaseLayout>
    );
  }
}

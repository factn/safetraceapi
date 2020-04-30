import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import * as Location from 'expo-location';

import Fences from '../geofences/fences.json';

// Thunk Action
export const getNodes = createAsyncThunk<any>(
  'nodes/get',
  async (body: any, thunkApi?) => {
    const response = await fetch('https://safetraceapi.herokuapp.com/api/nodes', {
      method: 'GET',
      headers: {
        api_key: `4b6bff10-760e-11ea-bcd4-03a854e8623c`,
      },
      body,
    });

    if (response.status !== 200) {
      return thunkApi.rejectWithValue((await response.json()) as any);
    }

    return (await response.json()) as any;
  },
);

export const postShares = createAsyncThunk<any>(
  'shares/post',
  async (body: any, thunkApi?) => {
    const response = await fetch('https://safetraceapi.herokuapp.com/api/shares', {
      method: 'POST',
      headers: {
        api_key: `4b6bff10-760e-11ea-bcd4-03a854e8623c`,
        'Content-Type': 'application/json',
      },
      body,
    });

    if (response.status !== 200) {
      return thunkApi.rejectWithValue((await response.json()) as any);
    }

    return (await response.json()) as any;
  },
);

export const locationSlice = createSlice({
  name: 'location',
  initialState: {
    token: {},
    error: '',
    loading: false,
    fences: Fences,
    position: {},
    recorder: {
      startTime: '',
      endTime: '',
      hasStarted: false,
      computationId: undefined,
    },
    bitData: [],
    nodes: {},
  },
  reducers: {
    startRecording: (state, action) => {
      console.log('Start Recoding initiated.');

      const fences = state.fences;

      state.recorder.startTime = Date.now();
      state.recorder.hasStarted = true;

      const newBitData = [1, 1];
      fences.forEach((fence) => {
        if (!!fence) {
          newBitData.push(0);
        }
      });
      state.bitData = newBitData;
    },
    updatePosition: (state, action) => {
      const { payload } = action;

      console.log('Updating Position', payload.position);
      state.position = payload.position;
    },
    computeDataOnFenceTrigger: (state, action) => {
      console.log('Compute Data on Fence Trigger.');

      const { payload } = action;
      const fences = state.fences;
      const recorder = state.recorder;
      let index = 0;
      
      if (!!recorder.hasStarted && !!payload && !!payload.data && !!payload.data.region && !!payload.data.region.identifier) {
        if (payload.data.region.identifier) {
          const newBitData = state.bitData;
          fences.forEach((fence) => {
            if (!!fence && fence.identifier === payload.data.region.identifier) {
              newBitData[index] = 1;
            } else {
              newBitData[index] = state.bitData[index];
            }

            index++;
          });
          state.bitData = newBitData;
        }
      }
    }
  },
  extraReducers: {
    [`${getNodes.fulfilled}`]: (state, action) => {
      const { payload } = action;
      const { nodes } = payload;
      
      if (!!nodes) {
        state.nodes = nodes;
      }
    },
    [`${getNodes.rejected}`]: (state, action) => {
      alert(JSON.stringify(action));
    }
  },
});

export const {} = locationSlice.actions;

// Selectors
export const selectError = (state: any) => state.location.error;
export const selectPosition = (state: any) => state.location.position;
export const selectBitData = (state: any) => state.location.bitData;
export const selectFences = (state: any) => state.location.fences;
export const selectNodes = (state: any) => state.location.nodes;

export default locationSlice.reducer;

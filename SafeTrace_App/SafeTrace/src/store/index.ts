import {configureStore, ThunkAction, Action} from '@reduxjs/toolkit';
import {useDispatch} from 'react-redux';

import {locationSlice} from './location.slice';

export const store = configureStore({
  reducer: {
    location: locationSlice.reducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export const useAppDispatch = () => useDispatch<AppDispatch>(); // Export a hook that can be resused to resolve types

export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;

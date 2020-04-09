import { createReducer, createActions } from 'reduxsauce'
import Immutable from 'seamless-immutable'

/* ------------- Types and Action Creators ------------- */
const { Types, Creators }: any = createActions({
  test: ['val']
});

export const AppTypes = Types
export default Creators

/* ------------- Initial State ------------- */
export const INITIAL_STATE = Immutable({
  val: 'Press me!',
});

/* ------------- Reducers ------------- */
export const performTest = (state: any, { val }: any) => {
  return { ...state, val };
}

/* ------------- Hookup Reducers To Types ------------- */
export const reducer = createReducer(INITIAL_STATE, {
  [Types.TEST]: performTest,
});
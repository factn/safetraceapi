import { compose, applyMiddleware, createStore, combineReducers } from "redux";
import thunk from "redux-thunk";
import { persistStore, persistReducer } from "redux-persist";
import { AsyncStorage } from 'react-native';

const rootReducer = combineReducers({
  app: require("./AppRedux").reducer,
});

export const configureStore = () => {
  const persistConfig = {
    key: "root",
    storage: AsyncStorage,
  };
  
  const middlewares: any[] = [thunk];
  const enhancers: any[] = [];
  
  if (__DEV__) {
    const { logger } = require("redux-logger");
  
    middlewares.push(logger);
  }

  enhancers.push(applyMiddleware(...middlewares));
  const persistedReducer = persistReducer(persistConfig, rootReducer);
  const store = createStore(persistedReducer, compose(...enhancers));
  const persistor = persistStore(store);

  return { store, persistor };
}
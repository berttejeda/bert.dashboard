// React core
import { BrowserRouter as Router } from 'react-router-dom';
import React, { FunctionComponent, useState } from "react";
import ReactDOM from 'react-dom/client'

// Hot-reloader logic
import { hot, AppContainer } from 'react-hot-loader';

import { Provider } from 'react-redux'

import store from 'store'

import history from 'history';

// Lesson App
import App from 'App'

const root = ReactDOM.createRoot(
  document.getElementById('app')
);

root.render(
    <React.StrictMode>
    <Provider store={store}>
      <Router history={history}>
        <App />
      </Router>
    </Provider>
    </React.StrictMode>
);

if(module.hot){
    module.hot.accept()
}
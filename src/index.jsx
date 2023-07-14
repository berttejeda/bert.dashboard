// React core
import { BrowserRouter as Router } from 'react-router-dom';
import React, { FunctionComponent, useState } from "react";
import ReactDOM from 'react-dom/client'

// Hot-reloader logic
import { hot, AppContainer } from 'react-hot-loader';

import { Provider } from 'react-redux'

import store from 'store'

// Lesson App
import App from 'App'

const root = ReactDOM.createRoot(
  document.getElementById('app')
);

root.render(
    <Provider store={store}>
      <Router>
        <App />
      </Router>
    </Provider>
);

if(module.hot){
    module.hot.accept()
}
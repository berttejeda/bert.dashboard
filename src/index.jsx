// React core
import { BrowserRouter as Router } from 'react-router-dom';
import React, { FunctionComponent, useState } from "react";
import ReactDOM from 'react-dom'

// Hot-reloader logic
import { hot, AppContainer } from 'react-hot-loader';

import { Provider } from 'react-redux'

import store from 'store'

// Lesson App
import App from 'App'

ReactDOM.render(

    <React.StrictMode>
    <Provider store={store}>
      <Router>
        <App />
      </Router>
    </Provider>
    </React.StrictMode>
  ,
  document.getElementById('app')
);

if(module.hot){
    module.hot.accept()
}
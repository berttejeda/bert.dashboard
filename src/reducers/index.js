import {combineReducers} from 'redux'

import currentUser from './currentUser'

import appData from './appData'

import dashboardData from './dashboardData'

import {combineReducers} from 'redux'

const rootReducer = combineReducers({
    appData,
    currentUser,
    dashboardData
})

export default rootReducer
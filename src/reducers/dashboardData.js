const dashboardData = (state = {}, action) => {
    switch(action.type){
        case "SET_DASHBOARD_DATA":
            return {
                ...state,
                data: action.payload
            }
        default:
            return state
    }
}

export default dashboardData;
const appData = (state = {}, action) => {
    switch(action.type){
        case "SET_APP_DATA":
            return {
                ...state,
                data: action.payload
            }
        default:
            return state
    }
}

export default appData;
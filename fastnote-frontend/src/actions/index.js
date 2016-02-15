/**
 * Created by techbk on 03/02/2016.
 */


// chua check trang thai dang fetching?????
//import fetch from 'isomorphic-fetch'

import { CALL_API, Schemas } from '../middleware/api'


export const USER_REQUEST = 'USER_REQUEST'
export const USER_REQUEST_S = 'USER_REQUEST_S'
export const USER_REQUEST_F = 'USER_REQUEST_F'

function fetchUser(login) {
  return {
    [CALL_API]: {
      types: [ USER_REQUEST, USER_REQUEST_S, USER_REQUEST_F ],
      endpoint: `users/${login}`,
      schema: Schemas.USER
    }
  }
}

export function loadUser(login, requiredFields = []){
  return (dispatch, getState) => {
    const user = getState().entities.users[login]
    if (user
      && requiredFields.every(key => user.hasOwnProperty(key))) {
      return null
    }

    return dispatch(fetchUser(login))
  }
}


export const NOTES_REQUEST = 'NOTES_REQUEST'
export const NOTES_REQUEST_S = 'NOTES_REQUEST_S'
export const NOTES_REQUEST_F = 'NOTES_REQUEST_F'





export const NOTE_CREATE = 'NOTE_CREATE'
export const NOTE_CREATE_S = 'NOTE_CREATE_S'
export const NOTE_CREATE_F = 'NOTE_CREATE_F'


export const NOTE_EDIT = 'NOTE_EDIT'
export const NOTE_EDIT_S = 'NOTE_EDIT_S'
export const NOTE_EDIT_F = 'NOTE_EDIT_F'


export const NOTE_DELETE = 'NOTE_DELETE'
export const NOTE_DELETE_S = 'NOTE_DELETE_S'
export const NOTE_DELETE_F = 'NOTE_DELETE_F'


export const NOTE_SEARCH = 'NOTE_SEARCH'
export const NOTE_SEARCH_S = 'NOTE_SEARCH_S'
export const NOTE_SEARCH_F = 'NOTE_SEARCH_F'


export const NOTE_TAG = 'NOTE_TAG'
export const NOTE_TAG_S = 'NOTE_TAG_S'
export const NOTE_TAG_F = 'NOTE_TAG_F'


export const RESET_ERROR_MESSAGE = 'RESET_ERROR_MESSAGE'

// Resets the currently visible error message.
export function resetErrorMessage() {
  return {
    type: RESET_ERROR_MESSAGE
  }
}
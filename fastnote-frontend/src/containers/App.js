/**
 * Created by techbk on 05/02/2016.
 */

import React, { Component, ProTypes } from 'react'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'
import Explore from '../components/Explore'
import { resetErrorMessage } from '../actions'

class App extends Component {

}

App.propTypes = {

}

function mapStateToProps(state) {
  return {
    errorMessage: state.errorMessage,
    inputValue: state.routing.location.pathname.substring(1)
  }
}

export default connect(mapStateToProps, {
  resetErrorMessage,
  push
})(App)
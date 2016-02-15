/**
 * Created by quang_000 on 05/02/2016.
 */

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { loadUser } from '../actions'
import User from '../components/User'
import zip from 'lodash/zip'

function loadData(props) {
  const { login } = props
  props.loadUser(login, [ 'name' ])
  props.loadStarred(login)
}

class UserPage extends Component {

}

function mapStateToProps(state, props) {
  const { login } = props.params

  return {
    login,
    user: users[login]
  }
}

export default connect(mapStateToProps, {
  loadUser
})
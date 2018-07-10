import React, { Component } from 'react';
import { Auth } from 'aws-amplify';
import { Button } from 'antd';
import CloudAccount from '../Block/CloudAccount';

class Settings extends Component {
  state = {
    username: ''
  }
  
  constructor(props) {
    super(props);
    var caller = this;
    
    Auth.currentAuthenticatedUser()
      .then(user => {
        caller.setState({ username: user.username });
      });
  }
  
  signOut = () => {
    Auth.signOut()
      .then(function(result) {
        window.location.reload();
      })
      .catch(err => console.log(err));
  }
  
  render() {
    return (
      <div>
        <h1>Hello { this.state.username }</h1>
        <Button type="primary" onClick={ this.signOut } style={{ marginTop: 20 }}>Sign Out</Button>
        <CloudAccount />
      </div>
    );
  }
}

export default Settings;

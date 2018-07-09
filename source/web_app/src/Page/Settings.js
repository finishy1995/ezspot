import React, { Component } from 'react';
import { withAuthenticator } from 'aws-amplify-react';
import { Auth, API } from 'aws-amplify';
import { Button } from 'antd';
import CloudAccount from '../Block/CloudAccount';

class Settings extends Component {
  state = {
    username: ''
  }
  
  componentWillMount = () => {
    var caller = this;
    
    Auth.currentAuthenticatedUser()
      .then(user => {
        caller.setState({ username: user.username });
      });
      
    Auth.currentSession().then(session => {
      // API.get('APIGateway', '/account?accessT=' + encodeURI(session.accessToken.jwtToken)).then(response => {
      //   console.log(response);
      // }).catch(error => {
      //   console.log(error);
      // });
      
      API.post('APIGateway', '/account').then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
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

export default withAuthenticator(Settings);

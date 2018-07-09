import React, { Component } from 'react';
import { withAuthenticator } from 'aws-amplify-react';

class Home extends Component {
  render() {
    return (
      <h1>Hello World!</h1>
    );
  }
}

export default withAuthenticator(Home);

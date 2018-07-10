import React, { Component } from 'react';
// eslint-disable-next-line
import Amplify, { Auth, API } from 'aws-amplify';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import { withAuthenticator } from 'aws-amplify-react';
import { Row, Col, Layout } from 'antd';
import './App.css';
import Home from '../Page/Home';
import Settings from '../Page/Settings';
declare var ezspot_config;

const { Header, Footer } = Layout;

Amplify.configure({
  Auth: {
    region: ezspot_config.SOLUTION_REGION,
    userPoolId: ezspot_config.SOLUTION_USERPOOLID,
    userPoolWebClientId: ezspot_config.SOLUTION_USERPOOLWEBCLIENTID,
    identityPoolId: ezspot_config.SOLUTION_IDENTITYPOOLID
  },
  API: {
    endpoints: [{
      name: "APIGateway",
      endpoint: ezspot_config.SOLUTION_APIENDPOINT,
      region: ezspot_config.SOLUTION_REGION,
    }]
  }
});

class App extends Component {
  // TODO: Use https://aws.github.io/aws-amplify/api/classes/authclass.html#currentauthenticateduser to show header only for auth user

  constructor(props) {
    super(props);
    this._validAuthStates = ['signedIn'];
  }

  render() {
    return (
      <div>
        <Router>
          <div>
            <Header className='app-header'>
              <Row>
                <Col span={8}>
                  <Link to="/home">EZSpot</Link>
                </Col>
                <Col span={16}>
                  <Link to="/settings" style={{float: 'right', color: '#fff'}}>Settings</Link>
                </Col>
              </Row>
            </Header>
            <Layout className="app-content">
              <Switch>
                <Route exact path='/' component={Home} />
                <Route path='/home' component={Home} />
                <Route path='/settings' component={Settings} />
              </Switch>
            </Layout>
            <Footer className="app-footer">
              <p>Serverless Web App all in AWS, using AWS S3, Lambda, DynamoDB etc.</p>
              <p>Designed and built with the customer obsession by @David Wang and @Frank Fang. Thanks for all contributors in this <a href="https://github.com/finishy1995/ezspot" target="_blank" rel="noopener noreferrer">project.</a></p>
            </Footer>
          </div>
        </Router>
      </div>
    );
  }
}

export default withAuthenticator(App);

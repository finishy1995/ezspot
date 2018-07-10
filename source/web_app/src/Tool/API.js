import { Auth, API } from 'aws-amplify';
import Lambda from 'aws-sdk/clients/lambda';
declare var ezspot_config;

function getParams(obj, callback) {
  Auth.currentSession().then(session => {
    var init = {
      queryStringParameters: {
        'accessT': session.accessToken.jwtToken
      }
    }
    // var init = {
    //   queryStringParameters: {
    //     'accessT': session.accessToken.jwtToken
    //   }
    // };
    
    // if ((obj) && (Object.keys(obj).length > 0)) {
    // //   init['headers'] = {
    // //     'a': encodeURIComponent('application/json')
    // //   };
    //   init['queryStringParameters']['body'] = encodeURIComponent(JSON.stringify(obj));
    // }
    callback(null, init);
  }).catch(error => {
    callback(error);
  });
}

export function call(method, path, obj, callback) {
  getParams(obj, function(error, res) {
    if (error)
      callback(error);
    else {
      if (method === 'get')
        API.get('APIGateway', path, res).then(response => {
          callback(null, response);
        }).catch(error => {
          callback(error);
        });
      else {
        Auth.currentCredentials()
          .then(credentials => {
            var lambda = new Lambda({
              credentials: Auth.essentialCredentials(credentials),
              region: ezspot_config.SOLUTION_REGION,
            });
            var event = res;
            event['queryStringParameters']['body'] = JSON.stringify(obj);
            event['path'] = path;
            event['httpMethod'] = method.toUpperCase();
            var params = {
              FunctionName: ezspot_config.SOLUTION_LAMBDA,
              Payload: JSON.stringify(event),
            };
              
            lambda.invoke(params, function(err, data) {
              if (err)
                callback(err);
              else {
                callback(null, data);
              }
            });
          });
      }
    }
  });
}

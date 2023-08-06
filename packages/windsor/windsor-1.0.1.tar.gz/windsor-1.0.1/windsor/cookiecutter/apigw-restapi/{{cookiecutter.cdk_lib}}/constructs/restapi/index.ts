import * as cdk from '@aws-cdk/core';
import * as apigw from '@aws-cdk/aws-apigateway';
import * as routes from './routes';


class RestApi extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const restApi: apigw.RestApi = new apigw.RestApi(this, 'RestAPI');
  }
}

export default RestApi;

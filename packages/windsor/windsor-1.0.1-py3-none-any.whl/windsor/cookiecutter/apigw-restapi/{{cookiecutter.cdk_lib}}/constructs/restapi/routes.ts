import * as lambda from '@aws-cdk/aws-lambda';


interface IRoute {
  handler: lambda.Function;
  resource: string;
  method: string;
}


export const urls: IRoute[] = [];

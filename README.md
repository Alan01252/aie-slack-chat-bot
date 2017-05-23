# AIE SlackBot

## About

A work in progress slack-bot for the AIE

## ChatBot Usage

`/aie [text]`

### Example commands

`/aie get checked in`

Returns a url by which to download a CSV file of those people who have checked in in the lat week

## Development

### Overview

The bot runs on AWS Lambda using the serverless.com framework for deployment.

### Adding to the bot dev

- Install node/npm
- Install serverless `npm install serverless -g`
- Create IAM credentials
- Create config file `serverless config credentials --provider aws --key [YOUR_IAM_KEY] --secret [YOUR_IAM_SECRET]
- Use aei-slack profile `export AWS_PROFILE="aei-slack" && export AWS_REGION=eu-west-1`
- Clone this repository
- Navigate to cloned repository
- npm install
- Create an environment file replace the things in brack as appropriate
   ````
   default_env: &default_env
    USER_ENDPOINT: [USERENDPOINT]
    REGISTER_ENDPOINT: [REGISTER_ENDPOINT]
    SLACK_HOOK_URL: [SLACK_HOOK_URL] 
    AUTH_HEADER:  [AUTH HEADER]
   
   dev:
    <<: *default_env
  
- Write code
- ???
- Deploy code and profit `serverless deploy -v`

### Deploying to production

- Deploy code and profit `serverless deploy --stage production`

`




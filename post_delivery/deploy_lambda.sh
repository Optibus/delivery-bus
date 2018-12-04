#!/usr/bin/env bash

mkdir deployment
cp ./lambda_code/* ./deployment/
cd deployment
pip install -r requirements.txt -t .

# zip package
zip -r lambda.zip . -x ".*"

# Upload zip to AWS (Update code)
aws --region us-east-1 lambda update-function-code --function-name Hackaton-Delivery-Bus --publish --zip-file fileb://"$(pwd)"/lambda.zip

cd ..
# remove deployment
rm -r ./deployment

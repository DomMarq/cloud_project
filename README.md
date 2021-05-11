# cloud_project
Final Project for cloud computing, implementing a distributed system to train a ML model and evaluate x-ray images submitted via a website using that model


## How to deploy to AWS
1. Run package.sh in the website directory
2. Upload lambda.zip to S3
3. Upload lambda.zip from S3 to Lambda
4. Deploy new lambda function on API Gateway

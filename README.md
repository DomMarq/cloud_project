# cloud_project
Final Project for cloud computing, implementing a distributed system to train a ML model and evaluate x-ray images submitted via a website using that model

# test throughput (repeat multiple times to get average)
time="$(time (./load_XXXX.sh ) 2>&1 1>/dev/null )"
echo "$time" > temp.txt
search in temp.txt for real time

# test latency (repeat multiple times to get average)
./load_XXXX.sh 2> outfile
python3 calculate_average.py outfile

## How to deploy to AWS
1. Run package.sh in the website directory
2. Upload lambda.zip to S3
3. Upload lambda.zip from S3 to Lambda
4. Deploy new lambda function on API Gateway
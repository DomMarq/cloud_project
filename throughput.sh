#!/bin/sh

# post 
start=$(date +%s.%N)
for run in {1..5}; do
    curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@00000003_000.png" https://kx0v87byqj.execute-api.us-east-1.amazonaws.com/dev/v1/uploadfile
done
runtime=$(echo "$(date +%s.%N) - $start" | bc)
throughput=$(echo "5/$runtime" | bc -l)

printf "\nPost throughput: "
echo "$throughput times/second"


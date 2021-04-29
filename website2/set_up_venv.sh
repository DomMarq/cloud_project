# run this before starting up the website or deploying
rm -r venv/
python3 -m venv venv
DOCKER_BUILDKIT=1 docker build --output layers/tflite_runtime/ .
pip install -r requirements.txt

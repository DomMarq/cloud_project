# run this before starting up the website or deploying
rm -r venv/
python3 -m venv venv
DOCKER_BUILDKIT=1 docker build --output . .
pip install -r requirements.txt
rm tflite_runtime-2.4.0-py3-none-any.whl

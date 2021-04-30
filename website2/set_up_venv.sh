# run this before starting up the website or deploying
rm -r venv/
python3 -m venv venv
# this command requires docker to be installed and running - docker desktop for local execution
DOCKER_BUILDKIT=1 docker build --output . .
# this line will probably not execute properly - run it in terminal
source venv/bin/activate && pip install -r requirements.txt \
&& rm tflite_runtime-2.4.0-py3-none-any.whl

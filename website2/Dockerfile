# Used to build wheel for tensorflow lite
# taken from https://dev.to/sandeepmistry/serverless-ml-inferencing-with-aws-lambda-and-tensorflow-lite-15el

# Use https://hub.docker.com/r/lambci/lambda as the base container
FROM lambci/lambda:build-python3.8 AS stage1

# set the working directory to /build
WORKDIR /build

# download Bazel (used to compile TensorFlow)
RUN curl -L https://github.com/bazelbuild/bazel/releases/download/3.7.1/bazel-3.7.1-linux-x86_64 -o /usr/bin/bazel && chmod +x /usr/bin/bazel

# make python3 the default python
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Use git to clone the TensorFlow source, checkout v2.4.0 branch
RUN git clone https://github.com/tensorflow/tensorflow.git --branch v2.4.0 --depth 1

# install TensorFlow Lite Python dependencies
RUN pip3 install pybind11 numpy

# start the TensorFlow Lite build with Bazel
RUN BAZEL_FLAGS='--define tflite_with_xnnpack=true' ./tensorflow/tensorflow/lite/tools/pip_package/build_pip_package_with_bazel.sh

# copy the built TensorFlow Lite Python .whl file to the Docker host
FROM scratch AS export-stage
COPY --from=stage1 /build/tensorflow/tensorflow/lite/tools/pip_package/gen/tflite_pip/python3/dist/tflite_runtime-2.4.0-py3-none-any.whl .

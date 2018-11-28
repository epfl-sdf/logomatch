# Build with: docker build -t opencv .
# Run with:   docker run -v $PWD:/wd opencv test.py

from python:3.5-stretch

VOLUME /wd
WORKDIR /wd
RUN pip3 install opencv-contrib-python==3.4.2.17
RUN pip3 install termcolor

ENTRYPOINT  ["python3"]

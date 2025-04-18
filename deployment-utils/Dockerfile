FROM mslipper/deployment-utils AS base

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip

# Install dependencies
RUN pip install --break-system-packages zstandard safe-pysha3 requests setuptools emoji

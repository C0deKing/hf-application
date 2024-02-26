# Use an NVIDIA base image with CUDA support
# Specify tag with specific base OS image
FROM nvidia/cuda:12.3.1-base-ubuntu20.04

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

# GCC is often needed for running pytorch
# CURL is needed to download poetry install scripts
RUN apt-get install curl gcc -y

RUN curl -sSL https://install.python-poetry.org | python3 -

# Set up application directory, and set it as the working directory
RUN mkdir -p /app
WORKDIR /app

ADD pyproject.toml .
ADD poetry.lock .
# Tell Poetry to not create a new virtual environment,
# and to use the existing one in the docker container
RUN $HOME/.local/bin/poetry config virtualenvs.create false

# Install dependencies specified in the pyptoject.toml and poetry.lock file
RUN $HOME/.local/bin/poetry install --without dev --no-root

# Add project files
ADD . .

RUN $HOME/.local/bin/poetry install --without dev

ENTRYPOINT ["python3", "my_project/entrypoint.py"]


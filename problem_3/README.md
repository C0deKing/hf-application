# Question 3

You're part of a team working on a new cloud integration. Your task is to create a Dockerfile that sets up an
environment supporting CUDA for GPU acceleration and the Hugging Face Transformers library for training LLMs. One of
your colleagues already started working on something for you to take over. The container should run on the latest
version of NVIDIA GPUs H100 and should be tested with a simple script after building. The container will be built inside
a CI environment and should be updated able for version changes.

## Solution

I have created a base project setup in this directory. The project has a few key components that I feel make composing
docker environments more consistent.

***Poetry***: [Poetry](https://python-poetry.org/) used as the dependency management tool to ensure that project
packages are consistent and compatible with one another. This is often accomplished with the poetry.lock file.

**docker ignore**: Docker ignore files are key to ensure that code involved with writing unit tests, or otherwise not
needed for production execution is left out of the docker container. The lockfile is also a great resource to view how
pyton library versions are resolved.

**Separation of dependencies and code**: Docker uses a caching mechanism to optimize the creation of docker images.
Splitting the installation of dependencies from the installation of python files into the docker file ensures that
program files and the dependencies managed in these files are stored in separate docker layers. This can often lead to
faster CI builds and deployments since common layers are often cached in the docker daemon.

## Building/Deploying the docker image

Below are the general steps to build and publish the docker image. This should be incorporated into your CI environment
build file (e.g. a Jenkinsfiles)

```shell
# Build the image
VERSION=$(poetry version --short)
# Tag it with the proejct version from poetry
docker build -t problem_3:$VERSION

#Log in to AWS ECR to push the image
REGION="us-east-2"
ACCOUNT_ID="ACCOUNT_ID"
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

#Tag the image 
docker tag problem_3:$VERSION $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/problem_3:$VERSION

# Push the image
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/problem_3:$VERSION

```
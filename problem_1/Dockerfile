FROM --platform=arm64 public.ecr.aws/lambda/python:3.9

RUN yum update -y

RUN yum install curl gcc -y
RUN curl -sSL https://install.python-poetry.org | python3 -

ADD pyproject.toml .
ADD poetry.lock .
RUN $HOME/.local/bin/poetry config virtualenvs.create false
RUN $HOME/.local/bin/poetry install --without dev --no-root

ADD . .

RUN $HOME/.local/bin/poetry install --without dev

ENTRYPOINT ["/lambda-entrypoint.sh"]
CMD [ "receipt_extractor.api_handler.lambda_handler" ]
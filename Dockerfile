FROM python:3.11.3-slim-bullseye as base

WORKDIR /actg-contacts

COPY . /actg-contacts

ADD requirements.txt /actg-contacts
RUN pip install -r requirements.txt

COPY . /actg-contacts

CMD ["python", "-m", "src.main"]

#########################
FROM base as test

#layer test tools and assets on top as optional test stage
RUN apt-get update && apt-get install -y curl

#########################
FROM base as final

# this layer gets built by default unless you set target to test
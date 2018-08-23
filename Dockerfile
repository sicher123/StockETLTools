FROM python:3.6

# RUN apt-get update && apt-get install -y libsnappy-dev \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/project

COPY ./requirements.txt /srv/project/

RUN pip install --no-cache -r requirements.txt

ENV PYTHONPATH=/srv/project

COPY ./ /srv/project/

VOLUME [ "/srv/project/data" ]
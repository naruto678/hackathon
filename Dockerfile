FROM python:3.9-alpine

USER root
RUN pip install --upgragde pip
RUN pip install --user pdm
COPY . /app
WORKDIR . "/app" 
RUN pdm install

ENTRYPOINT  python3 -m manager.py 
CMD "No command specified"

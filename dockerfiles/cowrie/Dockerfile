FROM python:3.8.16-buster
RUN apt update && apt install -y git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv
RUN useradd -m -p cowrie cowrie
USER cowrie
WORKDIR /home/cowrie
RUN git clone http://github.com/cowrie/cowrie
WORKDIR /home/cowrie/cowrie
USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade -r requirements.txt
USER cowrie
ENV COWRIE_STDOUT=yes
CMD ["/home/cowrie/cowrie/bin/cowrie", "start"]

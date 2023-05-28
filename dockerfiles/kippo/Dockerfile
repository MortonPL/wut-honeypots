FROM python:2.7.18-buster
RUN python -m pip install twisted==15.1.0 pycrypto pyasn1 zope.interface==3.6.0
RUN useradd -m -p kippo kippo
USER kippo
WORKDIR /home/kippo
RUN git clone https://github.com/desaster/kippo.git
WORKDIR /home/kippo/kippo
RUN cp kippo.cfg.dist kippo.cfg
CMD ["twistd", "-n", "-y", "kippo.tac"]

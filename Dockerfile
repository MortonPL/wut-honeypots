FROM debian:buster

WORKDIR /usr/

RUN apt update
RUN apt install -y sshpass openssh-client rsync nmap scanssh pcregrep

ENTRYPOINT ["sshpass"]

CMD ["--help"]

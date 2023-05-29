FROM alpine:3.6.5

WORKDIR /usr/

RUN apk --update --no-cache add sshpass openssh rsync nmap scanssh

ENTRYPOINT ["sshpass"]

CMD ["--help"]

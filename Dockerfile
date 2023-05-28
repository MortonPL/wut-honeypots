FROM alpine:latest

RUN apk --update --no-cache add sshpass openssh rsync

ENTRYPOINT ["sshpass"]

CMD ["--help"]

```
docker run -d -p 2222:2222 --name kippo tomdesinto/kippo
ssh -p 2222 root@localhost
docker logs -f kippo
docker stop kippo && docker rm kippo
```

```
docker run -d -p 2222:2222 --name cowrie cowrie/cowrie:latest
ssh -p 2222 root@localhost
docker logs -f cowrie
docker stop cowrie && docker rm cowrie
```

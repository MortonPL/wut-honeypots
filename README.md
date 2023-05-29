# Comparison of Kippo and Cowrie

## Setup

```sh
docker run -d --name kippo --hostname kippo tomdesinto/kippo
docker run -d --name cowrie --hostname cowrie cowrie/cowrie
```

## Running tests

```sh
docker build -t sshpass .
```

```sh
docker stop sshpass && docker rm sshpass
docker run --name sshpass --link=kippo --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/sh
```

```sh
export USER=root
export HOST=kippo
export PORT=2222
export PASS=123456
(cd test-cases-local; ./step1-1.sh)
(cd test-cases-local; ./step2-1.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step3-1.sh)
(cd test-cases-local; ./step4-1.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step4-2.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step5-1.sh)
```

```sh
docker stop sshpass && docker rm sshpass
```

```sh
docker run --name sshpass --link=cowrie --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/sh
```

```sh
export USER=root
export HOST=kippo
export PORT=2222
export PASS=123456
(cd test-cases-local; ./step1-1.sh)
(cd test-cases-local; ./step2-1.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step3-1.sh)
(cd test-cases-local; ./step4-1.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step4-2.sh)
(cd test-cases; sshpass -p "123456" ssh -oStrictHostKeyChecking=no -oKexAlgorithms=+diffie-hellman-group1-sha1 -p 2222 root@kippo < ./step5-1.sh)
```

```sh
docker stop sshpass && docker rm sshpass
```

## Cleanup

```sh
docker stop kippo && docker rm kippo
docker stop cowrie && docker rm cowrie
```

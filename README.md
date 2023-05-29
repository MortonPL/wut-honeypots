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
docker run --name sshpass --link=kippo --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/bash
```

```sh
export USER=root
export HOST=kippo
export PORT=2222
export PASS=123456
(cd test-cases-local; ./step1-1.sh)
(cd test-cases-local; ./step2-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p 2222 "$USER@$HOST" < ./step3-1.sh)
(cd test-cases-local; ./step4-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step4-2.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step5-1.sh)
```

```sh
docker stop sshpass && docker rm sshpass
```

```sh
docker stop sshpass && docker rm sshpass
docker run --name sshpass --link=cowrie --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/sh
```

```sh
export USER=root
export HOST=cowrie
export PORT=2222
export PASS=
(cd test-cases-local; timeout 10ss ./step1-1.sh)
(cd test-cases-local; timeout 10ss ./step2-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p 2222 "$USER@$HOST" < ./step3-1.sh)
(cd test-cases-local; timeout 10s ./step4-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step4-2.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step5-1.sh)
```

```sh
docker stop sshpass && docker rm sshpass
```

## Cleanup

```sh
docker stop kippo && docker rm kippo
docker stop cowrie && docker rm cowrie
```

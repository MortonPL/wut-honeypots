# Comparison of Kippo and Cowrie

## Setup

```sh
docker run -d --name kippo --hostname kippo -v ./mounts/kippo/data:/kippo-app/data -v ./mounts/kippo/honeyfs:/kippo-app/honeyfs -v ./mounts/kippo/kippo.cfg:/kippo-app/kippo.cfg -v ./mounts/kippo/fs.pickle:/kippo-app/fs.pickle tomdesinto/kippo
docker run -d --name cowrie --hostname cowrie -v ./mounts/cowrie/etc:/cowrie/cowrie-git/etc -v ./mounts/cowrie/honeyfs:/cowrie/cowrie-git/honeyfs -v ./mounts/cowrie/fs.pickle:/cowrie/cowrie-git/share/cowrie/fs.pickle cowrie/cowrie
```

## Running tests

```sh
docker build -t sshpass .
```

```sh
docker rm -f sshpass
docker run --name sshpass --link=kippo --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/bash
```

```sh
export USER=marcin001
export HOST=kippo
export PORT=2222
export PASS=zdt7*UHB
(cd test-cases-local; timeout 10s ./step1-1.sh)
(cd test-cases-local; timeout 10s ./step2-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step3-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" sftp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" "$USER@$HOST" < ./step4-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step4-2.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step5-1.sh)
```

```sh
docker rm -f sshpass
docker run --name sshpass --link=cowrie --expose=2222 -v ./test-cases:/usr/test-cases -v ./test-cases-local:/usr/test-cases-local -it sshpass /bin/bash
```

```sh
export USER=marcin001
export HOST=cowrie
export PORT=2222
export PASS=zdt7*UHB
(cd test-cases-local; timeout 10s ./step1-1.sh)
(cd test-cases-local; timeout 10s ./step2-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step3-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" sftp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" "$USER@$HOST" < ./step4-1.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step4-2.sh)
(cd test-cases; timeout 5s sshpass -p "$PASS" ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p "$PORT" "$USER@$HOST" < ./step5-1.sh)
```

```sh
docker rm -f sshpass
```

## Cleanup

```sh
docker rm -f kippo cowrie
```

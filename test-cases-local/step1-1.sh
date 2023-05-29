# [Local commands]


# Scanning using nmap

## Regular scan
nmap -v -p "$PORT" "$HOST"

## Stealth scan
nmap -sS -v -p "$PORT" "$HOST"

## Scan with additional scripts
nmap -v -p "$PORT" --script +ssh-auth-methods,+ssh-hostkey,+sshv1,+ssh2-enum-algos "$HOST"


# Retrieving additional information using verbose flag in ssh client

ssh -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -o "BatchMode=yes" -vv -p "$PORT" "$HOST"


# Scanning using scanssh

scanssh -n "$PORT" -s ssh "$HOST"

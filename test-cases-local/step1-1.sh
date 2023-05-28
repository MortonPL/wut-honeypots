# [Local commands]

HOST=
PORT=


# Scanning using nmap

## Regular scan
nmap -v -p "$PORT" "$HOST"

## "Stealth" scan
sudo nmap -sS -v -p "$PORT" "$HOST"

## Scan with additional scripts
nmap -v -p "$PORT" --script ssh-auth-methods,ssh-hostkey,sshv1,ssh2-enum-algos "$HOST"


# Retrieving additional information using verbose flag in ssh client

ssh -vv -p "$PORT" "$HOST"


# Scanning using ssh_scan

docker run --network=host mozilla/ssh_scan /app/bin/ssh_scan -t "$HOST" -p "$PORT"

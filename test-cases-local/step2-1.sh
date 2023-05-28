# [Local commands]

HOST=
PORT=

# Try different credentials (valid and invalid)

## Password-based authentication

nmap -v -p "$PORT" --script ssh-brute --script-args userdb=usernames.lst,passdb=passwords.lst "$HOST"

## Public key-based authentication

nmap -v -p "$PORT" --script ssh-publickey-acceptance --script-args 'ssh.usernames={"jkaczmarski", "marcin001"}, publickeys={"./rsa1.pub", "./rsa2.pub"}' "$HOST"

# [Local commands]


# Download files using SFTP

sshpass -p "$PASS" scp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" "$USER"@"$HOST":~/my_private_file.txt ./
sshpass -p "$PASS" scp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" "$USER"@"$HOST":~/my_private_script.sh ./


# Upload files using SFTP

sshpass -p "$PASS" scp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" ./malicious_script.sh "$USER"@"$HOST":~/
sshpass -p "$PASS" scp -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -P "$PORT" ./some_data.csv "$USER"@"$HOST":~/

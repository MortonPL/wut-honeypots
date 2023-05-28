# [Local commands]

USER=
HOST=
PORT=


# Download files using SFTP

sftp -P "$PORT" "$USER"@"$HOST":~/my_private_file.txt ./
sftp -P "$PORT" "$USER"@"$HOST":~/my_private_script.sh ./


# Upload files using SFTP

sftp -P "$PORT" ./malicious_script.sh "$USER"@"$HOST":~/
sftp -P "$PORT" ./some_data.csv "$USER"@"$HOST":~/

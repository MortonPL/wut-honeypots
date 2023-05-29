# [SSH session commands]


# File operations

## Modification

sed -i 's/ala/koala/ig' ~/my_private_file.txt

## Deletion

rm -f ~/my_private_file.txt

## Creation

echo "Example content" > ~/my_new_file.txt


# Superuser access

## Invalid credentials

echo "bad password" | sudo -S ls /

## Valid credentials

echo "good password" | sudo -S ls /


# Making file executable

echo "curl -X HEAD -i https://google.com/" > ~/malicious_script.sh
echo "echo HELLO" > ~/hello.sh
chmod +x ~/malicious_script.sh
chmod +x ~/hello.sh


# Adding cron task to run uploaded script

(crontab -l; echo -n "0 4 8-14 * * "; echo -n ~/hello.sh) | crontab -


# Running uploaded script

~/malicious_script.sh &

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

chmod +x ~/malicious_script.sh
chmod +x ~/hello_wget.sh
chmod +x ~/hello_curl.sh


# Adding cron task to run uploaded script

(crontab -l; echo -n "0 4 8-14 * * "; echo -n ~/hello_wget.sh) | crontab -


# Running uploaded script

~/malicious_script.sh &

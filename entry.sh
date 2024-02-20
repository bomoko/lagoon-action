#!/bin/sh

# Create SSH directory
mkdir -p ~/.ssh/

# Copy SSH private key from environment variable
echo -e "$INPUT_SSH_PRIVATE_KEY" > ~/.ssh/id_rsa

# Set correct permissions
chmod 600 ~/.ssh/id_rsa

# Add Lagoon host to known hosts
# ssh-keyscan your-lagoon-hostname >> ~/.ssh/known_hosts

# Set correct permissions for known_hosts
touch ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

cp /root/.lagoon.yml ~/.lagoon.yml


# envplate the .lagoon.yaml file
ep ~/.lagoon.yml

env | sort | grep GITHUB_

cat $GITHUB_EVENT_PATH

# /lagoon -l lagoon --force -i ~/.ssh/id_rsa $INPUT_LAGOON_COMMAND
# python3 action.py



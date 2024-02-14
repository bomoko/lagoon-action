#!/bin/sh

# Create SSH directory
mkdir -p ~/.ssh/

# Copy SSH private key from environment variable
echo -e "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa

# Set correct permissions
chmod 600 ~/.ssh/id_rsa

# Add Lagoon host to known hosts
# ssh-keyscan your-lagoon-hostname >> ~/.ssh/known_hosts

# Set correct permissions for known_hosts
touch ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

# envplate the .lagoon.yaml file
ep ~/.lagoon.yml

env | sort >> $GITHUB_OUTPUT

# /lagoon -l lagoon $LAGOON_COMMAND

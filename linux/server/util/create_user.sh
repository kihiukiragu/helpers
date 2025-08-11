#!/bin/bash

# --- Script to automate user creation and SSH setup from parameters ---
# This script must be run with sudo privileges.
#
# Usage:
#   sudo ./create_user.sh <username> "<ssh_key_1> <ssh_key_2> ..."
#
# Example:
#   sudo ./create_user.sh jdoe "ecdsa-sha2-... pontyit@PontyIT"

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo."
   exit 1
fi

# Check if both username and SSH keys were provided as arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Please provide both a username and at least one SSH key."
    echo "Usage: $0 <username> \"<ssh_key_1> <ssh_key_2> ...\""
    exit 1
fi

USERNAME=$1
SSH_KEYS=$2
PASSWORD="${USERNAME}4321"

# --- USER CREATION AND PASSWORD SETUP ---

echo "1. Creating user '$USERNAME' with a home directory."
useradd -m "$USERNAME"

echo "2. Setting a temporary password and forcing a change on first login."
echo "${USERNAME}:${PASSWORD}" | chpasswd
passwd -e "$USERNAME"

echo "3. Adding user '$USERNAME' to the 'sudo' group."
usermod -aG sudo "$USERNAME"

# --- SSH SETUP ---
echo "4. Setting up SSH keys for '$USERNAME'..."
# The `sudo -u` command executes the following block as the new user.
sudo -u "$USERNAME" bash << 'EOF_SSH'
# Create the .ssh directory if it doesn't exist.
mkdir -p ~/.ssh
# Set restrictive permissions on the .ssh directory.
chmod 700 ~/.ssh
# Write the public keys from the passed parameter to the authorized_keys file.
# The `printf` command handles the content more safely than `echo`.
printf "%s" "$SSH_KEYS" > ~/.ssh/authorized_keys
# Set restrictive permissions on the authorized_keys file.
chmod 600 ~/.ssh/authorized_keys
EOF_SSH

echo "User '$USERNAME' created successfully."
echo "Default password: '$PASSWORD'."
echo "The user must change this password upon first login."

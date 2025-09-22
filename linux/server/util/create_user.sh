#!/bin/bash

# --- Script to automate user creation and SSH setup from parameters ---
# This script must be run with sudo privileges.
#
# Usage:
#   sudo ./create_user.sh <username> "<ssh_key_1> <ssh_key_2> ..."
#
# Example:
#   sudo ./create_user.sh jdoe "ecdsa-sha2-... pontyit@PontyIT"

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo."
   exit 1
fi

# Check if both username and SSH keys were provided as arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Please provide both a username and at least one SSH key."
    echo "Usage: $0 <username> \"<ssh_key_1>\" \"<ssh_key_2>\" ..."
    exit 1
fi

USERNAME=$1
shift # Shift to get the rest of the arguments as keys
export SSH_KEYS=("$@") # Export the array as an environment variable
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

# Create the .ssh directory and set permissions as the new user.
sudo -u "$USERNAME" mkdir -p /home/"$USERNAME"/.ssh
sudo -u "$USERNAME" chmod 700 /home/"$USERNAME"/.ssh

# Use a loop to process each key and add it to the file.
for key in "${SSH_KEYS[@]}"; do
    # Use sudo and tee to write the key to the file with the correct permissions.
    echo "$key" | sudo -u "$USERNAME" tee -a /home/"$USERNAME"/.ssh/authorized_keys > /dev/null
done

# Set restrictive permissions on the authorized_keys file.
sudo -u "$USERNAME" chmod 600 /home/"$USERNAME"/.ssh/authorized_keys

echo "User '$USERNAME' created successfully."
echo "Default password: '$PASSWORD'."
echo "The user must change this password upon first login."

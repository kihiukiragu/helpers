# Server Setup & Configurations on Debian
You can use your home Debian PC or laptop as a server. You can use this for testing mostly or host an actual server on a budget!

## (Optional) Securing SSH service
> [!WARNING]
> Always have an extra ssh session open when making sshd changes in case something goes wrong, you can undo on the other session
1. Secure access to your server by adding a custom sshd configurations (NB: Avoid editing `/etc/ssh/sshd_config` as that gets overwritten during system updates):
   - Edit configuration file: `sudo vi /etc/ssh/sshd_config.d/custom-sshd.conf`
     - Disable Root login: `PermitRootLogin no`
     - Disable Password Authentication: `PasswordAuthentication no`
   - OR run the following:
   ```
   sudo zsh -c 'cat << "EOF" > /etc/ssh/sshd_config.d/custom-sshd.conf
   PermitRootLogin no
   PasswordAuthentication no
   EOF'
   ```
   OR
   ```
   sudo bash -c 'cat << "EOF" > /etc/ssh/sshd_config.d/custom-sshd.conf
   PermitRootLogin no
   PasswordAuthentication no
   EOF'
   ```
2. Verify using:
   ```
   grep -E '^PermitRootLogin|^PasswordAuthentication' /etc/ssh/sshd_config/custom-sshd.conf
   ```
   Output should be:
   ```
   PermitRootLogin no
   PasswordAuthentication no
   ```
3. Restart sshd service: `sudo service sshd restart`

## Server Applications Installation:
1. Install certbot & nginx plugin (for TLS certs):
   1. Install certbot and python certbot nginx plugin:
      ```
      apt install certbot python-certbot-nginx
      ```
   2. Generate certificate as follows: `certbot --nginx certonly -d mydomainname.com`
2. Install Nginx:
   1. Install: `sudo apt install nginx`
   2. Adjust Firewall:
      1. Allow HTTP & HTTPS: `sudo ufw allow 'Nginx Full'`
      2. Allow SSH: `sudo ufw allow ssh`
      2. Check status: `ufw status`
   3. Check nginx status: `systemctl status nginx`

## Install & nginx & certbot and SSL certs
1. Install nginx: `sudo apt install nginx`
2. Install certbot python plugin: `sudo apt install python3-certbot-nginx`
3. Generate SSL certs: `certbot --nginx certonly -d domain.example.com`

## (Optional) Allow a User to sudo without password
> [!WARNING]
> This option should ONLY be used if you fully understand the implications.
1. Create a file in `/etc/sudoers.d`
2. Edit the file and put the following rule: `username ALL=(ALL) NOPASSWD: ALL`


# Server Setup & Configurations on Debian
You can use your home Debian PC or laptop as a server. You can use this for testing mostly or host an actual server on a budget!

## (Optional) Securing SSH service
> [!WARNING]
> Always have an extra ssh session open when making sshd changes in case something goes wrong, you can undo on the other session
1. Secure access to your server by changing sshd configurations:
   - Edit configuration file: `sudo vi /etc/ssh/sshd_config`
     - Disable Root login: `PermitRootLogin no`
     - Disable Password Authentication: `PasswordAuthentication no`
   - OR run the following as user `root`:
   ```
   if [ ! -d "~/backup" ]; then
    mkdir ~/backup
   fi
   timestamp=d$(date +"%Y%m%d").t$(date +"%H%M%S")
   cp /etc/ssh/sshd_config ~/backup/sshd_config.$timestamp.bak
   sed -i 's/\(#P\|P\)ermitRootLogin.*$/PermitRootLogin no/g' /etc/ssh/sshd_config
   sed -i 's/#PasswordAuthentication.*$/PasswordAuthentication no/g' /etc/ssh/sshd_config
   ```
2. Verify using:
   ```
   grep -E '^PermitRootLogin|^PasswordAuthentication' /etc/ssh/sshd_config
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


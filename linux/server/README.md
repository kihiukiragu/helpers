# Server Setup & Configurations on Debian
You can use your home Debian PC or laptop as a server. You can use this for testing mostly or host an actual server on a budget!

## (Optional) Securing SSH service
> [!WARNING]
> Always have an extra ssh session open when making sshd changes in case something goes wrong, you can undo on the other session.
> Before disabling password authentication, confirm you can already log in with an SSH key (`ssh-copy-id user@server`), or you will lock yourself out.
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
   grep -E '^PermitRootLogin|^PasswordAuthentication' /etc/ssh/sshd_config.d/custom-sshd.conf
   ```
   Output should be:
   ```
   PermitRootLogin no
   PasswordAuthentication no
   ```
3. Restart sshd service: `sudo service sshd restart`

## Server Applications Installation:
1. Install Nginx:
   1. Install: `sudo apt install nginx`
   2. Adjust Firewall:
      1. Allow HTTP & HTTPS: `sudo ufw allow 'Nginx Full'`
      2. Allow SSH: `sudo ufw allow ssh`
      3. Check status: `sudo ufw status`
   3. Check nginx status: `systemctl status nginx`
2. Install certbot & nginx plugin (for TLS certs):
   1. Install certbot and the certbot nginx plugin: `sudo apt install certbot python3-certbot-nginx`
   2. Generate certificate as follows: `sudo certbot --nginx certonly -d mydomainname.com`

## (Optional) Allow a User to sudo without password
> [!WARNING]
> This option should ONLY be used if you fully understand the implications.
1. Create the file with `sudo visudo -f /etc/sudoers.d/username` (visudo checks the syntax; a broken sudoers file can lock you out of sudo)
2. Put the following rule in it: `username ALL=(ALL) NOPASSWD: ALL`


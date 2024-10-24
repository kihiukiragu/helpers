> [!NOTE]
> The content and links in this guide will periodically become outdated. Let me know when that happens! If you're willing to help, create a fix and create a pull request

# Debian 12.X (Bookworm) Installation Guide
If you’re new to Linux, welcome aboard!

## Download Debian

Download an ISO containing the last version of Debian which also bundles non-free firmware from this link: https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ (scroll down to the bottom of page and download .iso file)

1. Windows - download it using your prefered download manager or browser (Chrome / Firefox)
2. Linux command line download:
> [!IMPORTANT]
> If the URL below in the wget statement is broken go to https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ and download the `.iso` file.
```
wget -c https://cdimage.debian.org/cdimage/release/12.7.0/amd64/iso-dvd/debian-12.7.0-amd64-DVD-1.iso
```

### Installation
#### Steps
1. Preparing installation media
    1. If using Windows:-
       1. USB - [Ubuntu based guide - Remember to use the Debian ISO and not an Ubuntu ISO](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview)
       2. DVD - burn the downloaded ISO to a DVD
    2. (Highly Recommended) If using Linux or MacOS use the following steps to:
       1. Burn the ISO image to DVD using Brasero or any other image writing software or
       2. USB
          1. From the terminal, check USB drive:
             ```user@my-pc > lsblk #or dmesg```

          2. Linux command to write image to USB drive - (https://www.debian.org/releases/bookworm/amd64/ch04s03.en.html)
             ```
             #NB: Verify sdX is the usb drive you wish to create a bootable from eg cp debian-12.7.0-amd64-DVD-1.iso /dev/sdc
             cp debian-file.iso /dev/sdX
             sync #ensures files are securely copied
             ```

2. Ensure you can boot to USB/DVD on the computer where Debian is to be installed
3. Boot laptop/desktop with USB/DVD containing iso and proceed with the prompts
4. Remember to note down the root credentials (username & password) during installations. You will be prompted to create a new user.
5. Once installation is complete, proceed to configure your OS for updates etc

### Configuration of OS for Updates and Package Installations
1. (Optional if user created was created with root privileges) - Login as root to:
   1. Start a terminal session
   2. Add the new user you created during install as follows:
      ```
      sudo su - root
      adduser theusernameyoucreated sudo
      ```
      OR
      ```
      # Add an existing user to list of sudoers
      usermod -aG sudo nameOfNewUser
      ```

  3. Logout as root and login as the above user.
2. Check if root privileges worked: Start a Terminal session:
   1. Enter command (you will be prompted to enter your password): `sudo su - root`
   2. If no error messages occur, then that means you’re now root!
3. Editing application options:
   1. vi/vim - shell application that's ideal for experienced Linux users
      - Install vim: For some reason vim is usually not installed fully: `sudo apt install vim`
      - Start: `vi /path/to/file/to/be/edited`
   2. gedit - ideal for beginners
4. Edit sources file located at: `/etc/apt/sources.list`
   1. Switch to root user (see #2 above)
   2. Backup sources.list:
      ```
      if [ ! -d "~/backup" ]; then
          mkdir ~/backup
      fi
      cp /etc/apt/sources.list ~/backup/sources.list.d$(date +"%Y%m%d").t$(date +"%H%M%S").bak
      ```
   3. Type command: `gedit /etc/apt/sources.list` or `vi /etc/apt/sources.list`
   4. Comment out DVD source as update application will keep asking for DVD to be inserted. Comment out a line by adding `#` at the beginning of the DVD source line. You can also just delete the line
   5. You can insert additional sources for updates here
   6. It should look like:
      ```
      deb http://deb.debian.org/debian/ bookworm main
      deb-src http://deb.debian.org/debian/ bookworm main
      deb http://deb.debian.org/debian/ bookworm-updates main
      deb-src http://deb.debian.org/debian/ bookworm-updates main
      deb http://security.debian.org/debian-security bookworm-security main
      deb-src http://security.debian.org/debian-security bookworm-security main
      # Only add the backports if they already exist
      deb http://deb.debian.org/debian bookworm-backports main
      deb-src http://deb.debian.org/debian bookworm-backports main
      ```

5. Run updates on your Debian OS installation:
    1. Start a Terminal session
    2. Fetch latest version of the package list from Debian repo and 3rd party repos: `sudo apt update`
    3. Download and install for any outdated packages: `sudo apt dist-upgrade`

### Older Debian Versions eg Stretch and Buster

#### Update Debian 9.X Stretch OR (Upgrade Debian 7.X Jessie to Debian 8.X Stretch)

```
deb http://archive.debian.org/debian/ stretch main contrib non-free
deb http://archive.debian.org/debian/ stretch-proposed-updates main contrib non-free
deb http://archive.debian.org/debian-security stretch/updates main contrib non-free
```

#### Update old instance of Buster OR (Upgrade from Debian 9.X Stretch to Debian 10.X Buster)

```
deb http://archive.debian.org/debian/ buster-updates main contrib non-free
deb-src http://archive.debian.org/debian/ buster-updates main contrib non-free
deb http://archive.debian.org/debian buster main contrib non-free
deb-src http://archive.debian.org/debian buster/updates main contrib non-free
deb http://archive.debian.org/debian-security/ buster/updates main contrib non-free
deb-src http://archive.debian.org/debian-security/ buster/updates main contrib non-free
```

## Terminal Application Customizations (Optional but recommended)
### Install ZSH and Oh-My-Zsh (Optional)
1. Install zsh and dependencies (zsh is the base of oh-my-zsh):
   ```
   sudo apt install zsh curl git fonts-powerline powerline
   ```
2. Change to desired user which you want to install oh-my-zsh eg.: `su kkiragu`
3. Run oh my zsh install script:
   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```
4. Install theme eg powerlevel9k:
   ```
   git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
   ```
5. Edit .zshrc and add:
   ```
   sed -i 's/\(ZSH_THEME="robbyrussell"\)/#\1\nZSH_THEME="powerlevel9k\/powerlevel9k"/g' .zshrc
   ```
6. Re-run steps 3 -> 5 for other users
7. To make zsh (oh-my-zsh) default, log out completely and log back in for changes to take effect.
8. To change prompt color (in .zshrc ???):

   ```
   strPowerlevel9k=$(cat <<'EOF'

   # Change prompt color
   POWERLEVEL9K_DIR_HOME_BACKGROUND='195'
   POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND='195'
   POWERLEVEL9K_DIR_ETC_BACKGROUND='195'
   POWERLEVEL9K_DIR_DEFAULT_BACKGROUND='195'

   EOF
   );

   echo $strPowerlevel9k >> ~/.zshrc
   ```

9. If you’ll be using nvm to install and manage node/npm, add the following to the .zshrc file:
   ```
   export NVM_DIR=~/.nvm
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
   ```
10. sudo apt-get install powerline
    ```
    sudo symlink /etc/systemd/user/default.target.wants/powerline-daemon.service → /usr/lib/systemd/user/powerline-daemon.service.
    ```
11. For user postgres (or root): Install but don’t set it as default. Then start by:l0

    ```
    sudo -u postgres zsh
    sudo -u root zsh
    ```

### (Optional) Change default Editor to vim
1. Type: `sudo update-alternatives --config editor`
2. Select `vim.basic`

## Install Google Chrome
Debian comes with Firefox installed but you can add Chrome if you like: <https://www.linuxcapable.com/how-to-install-google-chrome-on-debian-linux/>

1. Open terminal
2. Append the sources list to include the Google Chrome repository with the following command:

   ```
   printf 'deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
   ```
3. Add a signing key as follows:
   ```
   wget -O- https://dl.google.com/linux/linux_signing_key.pub |gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg
   ```
4. Run: `sudo apt-get update`
5. Run: `sudo apt-get install google-chrome-stable`

## Server Setup
### Install & nginx & certbot and SSL certs
1. Install nginx: `sudo apt install nginx`
2. Install certbot python plugin: `sudo apt install python3-certbot-nginx`
3. Generate SSL certs: `certbot --nginx certonly -d domain.example.com`

### (Optional) Allow a User to sudo without password
> [!WARNING]
> This option should ONLY be used if you fully understand the implications.
1. Create a file in `/etc/sudoers.d`
2. Edit the file and put the following rule: `username ALL=(ALL) NOPASSWD: ALL`

### (Optional) Securing SSH service
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

### Server Applications Installation:
1. Install certbot & nginx plugin (for TLS certs):
   1. Install certbot and python certbot nginx plugin:
      ```
      apt install certbot python-certbot-nginx
      ```
   2. Generate certificate as follows: `certbot --nginx certonly -d mydomainname.com`
2. Install Nginx:
   1. Install: `apt install nginx`
   2. Adjust Firewall:
      1. Allow HTTP & HTTPS: `ufw allow 'Nginx Full'`
      2. Allow SSH: `ufw allow ssh`
      2. Check status: `ufw status`
   3. Check nginx status: `systemctl status nginx`

## Network and Printing Setup
### Configure Internet Sharing (Share WiFi via Ethernet Port)
1. Leave WiFi connection untouched
2. Edit the Ethernet connection (Wired) and change IPv4 setting to “Shared to other Computers”
3. Restart network manager service if need be.

### Configure VPN eg by Keep Solids (VPN Unlimited)

### Install & Configure Printing, LibreOffice:
1. Setting up printing: <https://wiki.debian.org/SystemPrinting>
2. Install LibreOffice (if it’s not installed already):
   1. sudo apt update
   1. sudo apt install libreoffice
3. AnyDesk (Use the following link, then convert the keyring as shown later in this guide)- http://deb.anydesk.com/howto.html


## Software Development Setup
### Install Dev Tools:
1. Install git: sudo apt-get install git
2. Configure:
   - Set your email and name:
   ```
   git config --global user.email “<YourEmail@email.com>”
   git config --global user.name “Firstname Lastname”
   ```
   - Set the editor of your choice:
   ```
   sudo update-alternatives --config editor
   ```
   OR
   ```
   git config --global core.editor "vim" #if not using Debian based distro
   ```
3. Install Java JDK:
    ```
    sudo apt-get install default-jre
    sudo apt-get install default-jdk
    ```
4. Gradle: sudo apt-get install gradle
5. Install node:
   1. Install nvm:
    ```
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.35.3/install.sh | bash
    ```
   2. If using zsh, edit .zshrc and add:
    ```
    export NVM_DIR=~/.nvm
      [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    ```
   3. `source ./zshrc`
   4. `nvm install node`
6. Install Visual Code
   1. Prepare sources:
    ```
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    sudo install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/microsoft-archive-keyring.gpg
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
    ```
   2. Install:
    ```
    sudo apt-get install apt-transport-https
    sudo apt-get update
    sudo apt-get install code
    ```
7. Install IntelliJ
   1. Install snaps (use this to manage IntelliJ installs) - sudo apt install snapd
   2. Install IntelliJ - sudo snap install intellij-idea-community --classic
8. Install Eclipse 2020-06:
   1. Download: curl -O http://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/neon/2/eclipse-java-neon-2-linux-gtk-x86_64.tar.gz
   2. Extract to /usr/ (So users can use it): sudo tar -zxvf eclipse-java-neon*.tar.gz -C /usr/
   3. Symlink to bin: sudo ln -s /usr/eclipse/eclipse /usr/bin/eclipse
   4. Create Icon:
      1. `sudo vi /usr/share/applications/eclipse.desktop`
      2. Copy and paste ini type of info:
         ```
         [Desktop Entry]
         Encoding=UTF-8
         Name=Eclipse 4.7
         Comment=Eclipse Neon
         Exec=/usr/bin/eclipse
         Icon=/usr/eclipse/icon.xpm
         Categories=Application;Development;Java;IDE
         Version=1.0
         Type=Application
         Terminal=0
         ```
      3. Save and exit

## (Troubleshooting) Post Debian Installation
###  Blank Screen
1. Likely causes:
   1. Missing display drivers
   2. Incomplete install of display drivers
2. Potential solutions:
   1. Edit Grub on start:
      1. Select a Grub option but but do NOT press “enter”
      2. Press ‘e’ to edit
      3. Look for a line ending in splash quiet and edit it so it has somewhere in the line: nomodeset
      4. If above does not work also try pci=nomsi

###  Key Ring Issues

Key ring issues - To resolve key ring warnings when you run `apt update`, do the following:

List existing keyrings using `apt-key list` but filter for the last 8 chars of the older existing key eg:
```
apt-key list | grep anydesk -B 3 | grep -Eo '[A-Z0-9]{4} [A-Z0-9]{4}$' | sed 's/ //g'
```

Export existing key to `trusted.gpg.d` folder:

```
apt-key export 210976F2 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/pgadmin.gpg
apt-key export CDFFDE29 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/anydesk.gpg
apt-key export 77E11517 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/php.gpg
```

Delete outdate or invalid keyrings:
```
apt-key del "DAC8....."
```

For `php`, if the above doesn't work, you might need to: delete and add the key again

## Additional Resources
> [!TIP]
> The following might be helpful to get your Linux PC or Server appropriately configured:

1. [PostgreSQL - Installing, Configuring & Uninstalling](database/README.md)
2. [Configuring Linux Desktop & Installing LibreOffice, IDEs etc](linux/desktop/README.md)

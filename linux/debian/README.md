# **Debian 12.X (Bookworm) Installation Guide**
If you’re new to Linux, welcome aboard! 

## Download

**NB**: If you find a broken link, see if you can locate a more current one online create a pull request.

Download ISO containing Debian latest version and bundles non-free firmware from here (scroll down to the bottom of page and download .iso file): [Link: ](https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/11.6.0+nonfree/amd64/iso-dvd/)<https://cdimage.debian.org/cdimage/release/12.5.0/amd64/iso-dvd/>

### Installation
#### Steps
1. Preparing installation media
    1. If using Windows: - 
        1. USB - https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview
        1. DVD - burn the downloaded ISO to a DVD
    1. (Highly Recommended) If using Linux or MacOS use the following steps to:
       1. Burn the ISO image to DVD using Brasero or any other image writing software or 
       1. USB
          1. From the terminal, check USB drive: 
            ```user@my-pc > lsblk #or dmesg```

        1. Linux command to write image to USB drive - 
        ```
        user@my-pc > cp debian-file.iso /dev/sdX #verify sdX is usb drive
        user@my-pc > sync #ensures files are securely copied
        ```

1. Ensure you can boot to USB/DVD on the computer where Debian is to be installed
1. Boot laptop/desktop with USB/DVD containing iso and proceed with the prompts
1. Remember to note down the root credentials (username & password) during installations. You will be prompted to create a new user.
1. Once installation is complete, proceed to configure your OS for updates etc

### Configuration of OS for Updates and Package Installations
1. (Optional if user created was created with root privileges) - Login as root to:
   1. Start a terminal session
   1. Add the new user you created during install as follows:
    ```
    sudo su - root
    adduser theusernameyoucreated sudo
    ```
    OR
    ```
    # Add an existing user to list of sudoers
    usermod -aG sudo nameOfNewUser
    ```

  1. Logout as root and login as the above user.
1. Check if root privileges worked: Start a Terminal session:
   1. Enter command (you will be prompted to enter your password): `sudo su - root`
   1. If no error messages occur, then that means you’re now root!
1. Editing application options:
    1. vi/vim - shell application that's ideal for experienced Linux users
        1. Install vim: For some reason vim is usually not installed fully: `sudo apt install vim`
        2. Start: `vi /path/to/file/to/be/edited`
    2. gedit - ideal for beginners
1. Edit sources file located at: `/etc/apt/sources.list`
   1. Switch to root mode (see #2 above)
   2. Type command: `gedit /etc/apt/sources.list` or `vi /etc/apt/sources.list`
   3. Comment out DVD source as update application will keep asking for DVD to be inserted. Comment out a line by adding `#` at the beginning of the DVD source line. You can also just delete the line
   4. You can insert additional sources for updates here
   5. It should look like:
    ```
    deb http://deb.debian.org/debian/ bookworm main
    deb-src http://deb.debian.org/debian/ bookworm main
    deb http://deb.debian.org/debian/ bookworm-updates main
    deb-src http://deb.debian.org/debian/ bookworm-updates main
    deb http://security.debian.org/debian-security bookworm-security main
    deb-src http://security.debian.org/debian-security bookworm-security main
    deb http://deb.debian.org/debian bookworm-backports main
    deb-src http://deb.debian.org/debian bookworm-backports main
    ```

1. Run updates on your Debian OS installation:
    1. Start a Terminal session
    2. Fetch latest version of the package list from Debian repo and 3rd party repos: `sudo apt update`
    3. Download and install for any outdated packages: `sudo apt dist-upgrade`


**(Optional) Change default Editor to vim**

1. Type: `sudo update-alternatives --config editor`
1. Select `vim.basic`

### Install Google Chrome
Debian comes with Firefox installed but you can add Chrome if you like: <https://www.linuxcapable.com/how-to-install-google-chrome-on-debian-linux/>

1. Open terminal
2. Append the sources list to include the Google Chrome repository with the following command:

    ```
    user@my-pc > cat << EOF > /etc/apt/sources.list.d/google-chrome.list deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main EOF
    ```
3. Add a signing key as follows:
    ```
    user@my-pc > wget -O- https://dl.google.com/linux/linux\_signing\_key.pub |gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg
    ```
4. Run: `sudo apt-get update`
5. Run: `sudo apt-get install google-chrome-stable`


### Terminal Application Customizations (Optional but recommended)
#### Install ZSH and Oh-My-Zsh (Optional)
1. Install zsh and dependencies (zsh is the base of oh-my-zsh): 
    ```
    sudo apt install zsh curl git fonts-powerline powerline
    ```
1. Change to desired user which you want to install oh-my-zsh eg.: `su kkiragu`
1. Run oh my zsh install script: 
    ```
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
1. Install theme eg power: 
    ```
    git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
    ```
1. Edit .zshrc and add: 
    ```
    sed -i 's/\(ZSH\_THEME="robbyrussell"\)/#\1\nZSH\_THEME="powerlevel9k\/powerlevel9k"/g' .zshrc
    ```
1. Re-run steps 3 -> 5 for other users
1. To make zsh (oh-my-zsh) default, log out completely and log back in for changes to take effect.
1. To change prompt color (in .zshrc ???):

    ```
    strPowerlevel9k=$(cat <<'EOF'
    
    # Change prompt color
    POWERLEVEL9K\_DIR\_HOME\_BACKGROUND='195'
    POWERLEVEL9K\_DIR\_HOME\_SUBFOLDER\_BACKGROUND='195'
    POWERLEVEL9K\_DIR\_ETC\_BACKGROUND='195'
    POWERLEVEL9K\_DIR\_DEFAULT\_BACKGROUND='195'
    
    EOF
    ); 
    
    echo $strPowerlevel9k >> ~/.zshrc
    ```

1. If you’ll be using nvm to install and manage node/npm, add the following to the .zshrc file:
    ```
    export NVM\_DIR=~/.nvm
     [ -s "$NVM\_DIR/nvm.sh" ] && . "$NVM\_DIR/nvm.sh"
    ```
1. sudo apt-get install powerline
    ```
    sudo symlink /etc/systemd/user/default.target.wants/powerline-daemon.service → /usr/lib/systemd/user/powerline-daemon.service.
    ```
1. For user postgres (or root): Install but don’t set it as default. Then start by:l0

    ```
    sudo -u postgres zsh
    sudo -u root zsh
    ```
    
### Server Setup
#### Install & nginx & certbot and SSL certs
1. Install nginx: `sudo apt install nginx`
1. Install certbot python plugin: `sudo apt install python3-certbot-nginx`
1. Generate SSL certs: `certbot --nginx certonly -d domain.example.com`

#### <a name="_ybuv6ma0em4e"></a>Allow User to sudo without password
1. Create a file in `/etc/sudoers.d`
1. Edit the file and put the following rule: `username ALL=(ALL) NOPASSWD: ALL`

#### <a name="_u0be09k83nct"></a>Securing SSH Port and Configuration
1. Change default ssh port:
1. Edit configuration file: `vi /etc/ssh/sshd\_config`

1. Disable Root login: `PermitRootLogin no`
1. Restart sshd: `service sshd restart`

#### Server Applications Installation:
1. Install PostgreSQL 15
   1. Add Repo: `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
   1. Add repo to Debian repo lists folder: `echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb\_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list`
   1. Install psql server and client: `apt -y install postgresql-15`
   1. (Recommended) Secure user postgres - TBD
1. Install certbot & nginx plugin (for TLS certs): 
   1. Install certbot: `apt install certbot`
   1. apt install python-certbot-nginx
   1. Generate cert: certbot --nginx certonly -d erp.mydomainname.com
1. Install Nginx:
   1. Install: apt install nginx
   1. Adjust Firewall:
      1. Allow HTTP: ufw allow 'Nginx Full'
      1. Check status: ufw status 
   1. Check nginx status: systemctl status nginx
### <a name="_lzakmelblg3e"></a>Network and Printing Setup
#### <a name="_rp6v2oqyhlrq"></a>**Configure Internet Sharing (Share WiFi via Ethernet Port)**
1. Leave WiFi connection untouched
1. Edit the Ethernet connection (Wired) and change IPv4 setting to “Shared to other Computers”
1. Restart network manager service if need be.
#### <a name="_9gxog3pxp4kr"></a>**Install & Configure Printing, LibreOffice:**
1. Setting up printing: <https://wiki.debian.org/SystemPrinting> 
1. Install LibreOffice (if it’s not installed already): 
   1. sudo apt update
   1. sudo apt install libreoffice
1. AnyDesk


### Software Development Setup
#### **Install Dev Tools:**
1. Install git: sudo apt-get install git
1. Configure:
   1. git config --global user.email “<YourEmail@email.com>”
   1. git config --global user.name “Firstname Lastname”
1. Install Java JDK: 
   1. sudo apt-get install default-jre
   1. sudo apt-get install default-jdk
1. Gradle: sudo apt-get install gradle
1. Install node:
   1. Install nvm: 

      curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.35.3/install.sh | bash

   1. If using zsh, edit .zshrc and add:

      export NVM\_DIR=~/.nvm

      ` `[ -s "$NVM\_DIR/nvm.sh" ] && . "$NVM\_DIR/nvm.sh"

   1. source ./zshrc
   1. nvm install node
1. Install Visual Code
   1. Prepare sources:
      1. curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
      1. sudo install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/microsoft-archive-keyring.gpg
      1. sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
   1. Install:
      1. sudo apt-get install apt-transport-https
      1. sudo apt-get update
      1. sudo apt-get install code

1. Install IntelliJ
   1. Install snaps (use this to manage IntelliJ installs) - sudo apt install snapd 
   1. Install IntelliJ - sudo snap install intellij-idea-community --classic
1. Install Eclipse 2020-06:
   1. Download: curl -O http://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/neon/2/eclipse-java-neon-2-linux-gtk-x86\_64.tar.gz
   1. Extract to /usr/ (So users can use it): sudo tar -zxvf eclipse-java-neon\*.tar.gz -C /usr/
   1. Symlink to bin: sudo ln -s /usr/eclipse/eclipse /usr/bin/eclipse
   1. Create Icon:
      1. ` `sudo vi /usr/share/applications/eclipse.desktop
      1. Copy and paste ini type of info: 
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
      1. Save and exit


#### (Troubleshooting) Post Debian Installation Blank Screen
1. Likely causes:
   1. Missing display drivers
   1. Incomplete install of display drivers
1. Potential solutions:
   1. Edit Grub on start:
      1. Select a Grub option but but do NOT press “enter”
      1. Press ‘e’ to edit
      1. Look for a line ending in splash quiet and edit it so it has somewhere in the line: nomodeset
      1. If above does not work also try pci=nomsi
1. Key ring issues - To resolve key ring warnings when you run `apt update`, do the following:

```
   apt-key export 210976F2 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/pgadmin.gpg
   apt-key export CDFFDE29 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/anydesk.gpg
```

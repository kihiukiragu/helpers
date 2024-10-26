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
4. Remember to note down the root credentials (username & password) during installations. You will also be prompted to create a new primary user. This user will be a `sudoer` by default.
5. Once installation is complete, proceed to configure your OS for updates etc

### Configuration of OS for Updates and Package Installations
> [!NOTE]
> During Debian installation, you created a primary user/username. Those credentials will come in handy in the next steps.
> If you're new to Linux and command line, you likely will want to substituate any instances of the editor usage of `vi` with beginner editors eg `gedit` or `kwrite` or `nano`.
> Command line newbies - when prompted to enter a password, nothing will appear on the screen. Don't panic!

Your Debian installation needs to be configured to pull and apply updates in future:
1. Start a terminal session
2. (Optional) Add new user(s):
  ```
  sudo su - root
  adduser newusername sudo
  ```
  OR
  ```
  # Add an existing user to list of sudoers
  usermod -aG sudo newusername
  ```

3. Test if you actually have root privileges:
   1. Enter command (you will be prompted to enter your password): `sudo su - root`
   2. If no error messages occur, then that means you’re now root!
   3. Install gedit, and kwrite:
      ```
      sudo apt install gedit kwrite
      ```
4. Editing application options:
   - gedit - ideal for beginners OR
   - vi/vim - shell application that's ideal for experienced Linux users
      - Install vim: For some reason vim is usually not installed fully: `sudo apt install vim`
      - Start: `vi /path/to/file/to/be/edited`
5. Edit sources file located at: `/etc/apt/sources.list`
   1. Backup sources.list in case something goes awry:
      ```
      if [ ! -d "~/backup" ]; then
          mkdir ~/backup
      fi
      cp /etc/apt/sources.list ~/backup/sources.list.d$(date +"%Y%m%d").t$(date +"%H%M%S").bak
      ```
   2. Open an editor to make the changes:
      ```
      sudo gedit /etc/apt/sources.list
      ```
      OR for vi folks:
      ```
      sudo vi /etc/apt/sources.list
      ```
   3. It should look like (feel free to choose an alternative mirror site other than the default `deb.debian.org` based on your geographical location - doesn't make much difference if you have a good internet connection):
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

6. Update your Debian OS installation:
   - Fetch latest version of the package list from Debian repo and 3rd party repos:
     ```
     sudo apt update
     ```
   - Download and install for any outdated packages:
     ```
     sudo apt full-upgrade
     ```

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
5. Run the following (NB: This updattes `.zshrc` file):
   ```
   sed -i 's/\(ZSH_THEME="robbyrussell"\)/#\1\nZSH_THEME="powerlevel9k\/powerlevel9k"/g' .zshrc
   ```
6. Re-run steps 3 -> 5 for other users
7. To make zsh (oh-my-zsh) default, log out completely and log back in for changes to take effect.
8. Run the following to change prompt color (NB: This updattes `.zshrc` file):

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
Debian comes with Firefox installed but you can add Chrome if you like.

1. Open a terminal session
2. Append the sources list to include the Google Chrome repository with the following command:

   ```
   printf 'deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
   ```
3. Add a signing key as follows:
   ```
   wget -O- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg
   ```
4. Update the repositories:
   ```
   sudo apt-get update
   ```
5. Install Chrome (recommend the stable option):
   ```
   sudo apt-get install google-chrome-stable
   ```

## Network and Printing Setup
### Configure Internet Sharing (Share WiFi via Ethernet Port)
1. Leave WiFi connection untouched
2. Edit the Ethernet connection (Wired) and change IPv4 setting to “Shared to other Computers”
3. Restart network manager service if need be.

### Configure VPN eg by Keep Solids (VPN Unlimited)
TBD

### Install & Configure Printing, LibreOffice:
1. Setting up printing: <https://wiki.debian.org/SystemPrinting>
2. Install LibreOffice (if it’s not installed already):
   ```
   sudo apt update
   sudo apt install libreoffice
   ```
3. AnyDesk (Use the following link, then convert the keyring as shown later in this guide)- http://deb.anydesk.com/howto.html

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

1. [PostgreSQL - Installing, Configuring & Uninstalling](../database/README.md)
2. [Configuring Linux Desktop & Installing LibreOffice, IDEs etc](../desktop/README.md)

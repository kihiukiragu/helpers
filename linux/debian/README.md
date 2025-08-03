> [!NOTE]
> The content and links in this guide will periodically become outdated. Let me know when that happens! If you're willing to help, create a fix and create a pull request

# Debian 13.X (Trixie) Installation Guide
Why Debian GNU/Linux? Debian might be right for you if you:
- Like stability in an Operating System.
- Do NOT care for the very latest Linux tools and applications until they are thoroughly tested.
- Have older hardware and want something lean and mean.

## Download Debian

Download an ISO containing the last version of Debian which also bundles non-free firmware from this link: https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ (scroll down to the bottom of page and download .iso file)

1. Windows - download it using your preferred download manager or browser (Chrome / Firefox)
2. Linux command line download:
> [!IMPORTANT]
> If the URL below in the wget statement is broken go to https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ and download the `.iso` file.
```
wget -c https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/debian-12.11.0-amd64-DVD-1.iso
```

### Installation
#### Steps
1. Preparing Linux installation media
   - If using a Ventoy USB drive, simply insert it and boot (i.e. continue to step #2).
   - If not using Ventoy (but also using Windows):<br>
     a. USB - [Ubuntu based guide - NB: Remember to use the Debian ISO and not an Ubuntu ISO](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview)<br>
     b. DVD - burn the downloaded ISO to a DVD
   - (Highly Recommended) If using Linux or macOS use the following steps to:<br>
     a. Burn the ISO image to DVD using Brasero or any other image writing software or<br>
     b. USB
        - From the terminal, check USB drive from the command line, type `lsblk` or `dmesg` and get output as follows:
          ```
          ...
          loop21        7:21   0   347M  1 loop /snap/wine-platform-runtime/390
          sda           8:0    0 931.5G  0 disk
          ├─sda1        8:1    0   128M  0 part
          └─sda2        8:2    0 931.4G  0 part
          sdb           8:16   1  28.9G  0 disk
          └─sdb1        8:17   1  28.9G  0 part /media/kkiragu/docs
          sdc           8:32   1  28.9G  0 disk
          └─sdc1        8:33   1  28.9G  0 part
          sr0          11:0    1  1024M  0 rom
          nvme0n1     259:0    0 476.9G  0 disk
          ├─nvme0n1p1 259:1    0 445.2G  0 part /
          ├─nvme0n1p2 259:2    0     1K  0 part
          ...
          ```
          Where in the above case, the USB drive is `sdb1`

        - You might need to format the usb drive. If your PC or Laptop is UEFI only. You will need the USB formatted to `FAT32` to make it UEFI compatible.
        - Linux command to write image to USB drive - (https://www.debian.org/releases/bookworm/amd64/ch04s03.en.html)
          ```
          #NB: Verify sdX is the usb drive you wish to create a bootable from e.g. cp debian-12.7.0-amd64-DVD-1.iso /dev/sdc
          cp debian-file.iso /dev/sdX
          sync #ensures files are securely copied
          ```

2. Check boot sequence in your BIOS settings, ensure you can boot using USB/DVD and that it's first option.
3. Boot the laptop/desktop with USB/DVD containing the Debian iso and proceed with the prompts.
4. IMPORTANT: If installing Dual Boot Windows and Linux (please read this guide first if you haven't - [Dual Boot Windows & Linux](../dual-boot-linux-windows.md): Once you get to **Partition Disks** eg. see [screenshot](https://www.debugpoint.com/wp-content/uploads/2023/11/Select-manual-partitioning.jpg):
   - Select **Manual**
   - It will scan your hard-drives and display different partitions on your computer similar to [this](https://www.debugpoint.com/wp-content/uploads/2023/11/Choose-the-partition-for-Debian-12-installation.jpg).
   - Determine the ~ 30 GB partition (i.e. the one you shrunk/set up earlier) and select it. If unsure of the right partition, take a picture and share with an experienced Linux user.
   - Once sure, press enter to set up the partition.
   - Select "Finish partitioning and write changes to disk"
5. Proceed with installation.
6. Remember to note down the root credentials (username & password) during installations. You will also be prompted to create a new primary user. This user will be a `sudoer` by default.
7. Once installation is complete, proceed to configure your OS for updates etc.

### Configuration of OS for Updates and Package Installations
> [!NOTE]
> During Debian installation, you created a primary user/username. Those credentials will come in handy in the next steps.
> If you're new to Linux and command line, you likely will want to substitute any instances of the editor usage of `vi` with beginner editors e.g. `gedit` or `kwrite` or `nano`.
> Command line newbies - when prompted to enter a password, nothing will appear on the screen. Don't panic!

Your Debian installation needs to be configured to pull and apply updates in the future:
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
   1. Backup `sources.list` in case something goes awry:
      ```
      if [ ! -d ~/backup ]; then
          mkdir ~/backup
      fi
      cp /etc/apt/sources.list ~/backup/sources.list.d$(date +"%Y%m%d").t$(date +"%H%M%S").bak
      ```
   2. Use vi editor to make the changes:
      ```
      sudo vi /etc/apt/sources.list
      ```
   3. It should look like (feel free to choose an alternative mirror site other than the default `deb.debian.org` based on your geographical location - doesn't make much difference if you have a good internet connection):
      ```
      deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
      deb-src http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware

      deb http://deb.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
      deb-src http://deb.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware

      deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
      deb-src http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware

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

### Older Debian Versions e.g. Stretch and Buster

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

## Add New Users
To add a new user e.g. for `Jane Doe` run the following:
```
sudo adduser jdoe
```
To ensure Jane resets the password on first login or password attempt:
```
chage -d 0 jdoe
```

OPTIONAL - You can also create ssh keys for this new user if they will require for ssh authentication later. Steps:
1. Switch to the new user: `sudo su - jdoe`
2. Run: `ssh-keygen -t ecdsa`. This also creates the folder `.ssh` with the necessary permissions. Though not recommended, do not change any default option or enter any passphrase.

## Terminal Application Customizations (Optional but recommended)
### Install ZSH and Oh-My-Zsh (Optional)
1. Install zsh and dependencies (zsh is the base of oh-my-zsh):
   ```
   sudo apt install zsh curl git fonts-powerline powerline
   ```

   OR for Fedora
   ```
   sudo dnf install zsh curl git powerline
   ```

2. Change to desired user which you want to install oh-my-zsh  e.g.: `su kkiragu`
3. Run oh my zsh install script:
   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```
4. Install theme e.g. powerlevel9k:
   ```
   git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
   ```
5. Run the following (NB: This updates `.zshrc` file):
   ```
   sed -i 's/\(ZSH_THEME="robbyrussell"\)/#\1\nZSH_THEME="powerlevel9k\/powerlevel9k"/g' .zshrc
   ```
6. Re-run steps 3 -> 5 for other users
7. To make zsh (oh-my-zsh) default, log out completely and log back in for changes to take effect.
8. Run the following to change prompt color (NB: This updates `.zshrc` file):

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
    sudo -i -u postgres zsh
    sudo -i -u root zsh
    ```

### (Optional) Change default Editor to vim

1. Type:
   - `select-editor` OR
   - `sudo update-alternatives --config editor`
2. Select `vim.basic`

## Install Google Chrome
Debian comes with Firefox installed, but you can add Chrome if you like.

1. Open a terminal session
2. Append the sources list to include the Google Chrome repository with the following command:

   ```
   sudo zsh -c 'cat << "EOF" > /etc/apt/sources.list.d/google-chrome.list
   deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main
   EOF'
   ```
3. Add a signing key as follows:
   ```
   curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/google-chrome.gpg >> /dev/null
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
### Configure Internet Sharing (Share Wi-Fi via Ethernet Port)
1. Leave Wi-Fi connection untouched
2. Edit the Ethernet connection (Wired) and change IPv4 setting to “Shared to other Computers”
3. Restart network manager service if need be.

### Configure VPN e.g. by Keep Solids (VPN Unlimited)
TBD

### Install & Configure Printing, LibreOffice:
1. Setting up printing: https://wiki.debian.org/SystemPrinting
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
   2. Incomplete installation of display drivers
2. Potential solutions:
   1. Edit Grub on start:
      1. Select a Grub option but do NOT press “enter”
      2. Press ‘e’ to edit
      3. Look for a line ending in splash quiet and edit it so it has somewhere in the line: nomodeset
      4. If above does not work also try pci=nomsi

###  Key Ring Issues

Key ring issues - To resolve key ring warnings when you run `apt update`, do the following:

List existing keyrings using `apt-key list` but filter for the last 8 chars of the older existing key e.g.:
```
apt-key list | grep anydesk -B 3 | grep -Eo '[A-Z0-9]{4} [A-Z0-9]{4}$' | sed 's/ //g'
```

Export existing key to `trusted.gpg.d` folder:

```
apt-key export 210976F2 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/pgadmin.gpg
apt-key export CDFFDE29 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/anydesk.gpg
apt-key export 77E11517 | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/php.gpg
```

Delete outdated or invalid keyrings:
```
apt-key del "DAC8....."
```

For `php`, if the above doesn't work, you might need to: delete and add the key again

## Additional Resources
> [!TIP]
> The following might be helpful to get your Linux PC or Server appropriately configured:

1. [PostgreSQL - Installing, Configuring & Uninstalling](../database/README.md)
2. [Configuring Linux Desktop & Installing LibreOffice, IDEs etc](../desktop/README.md)

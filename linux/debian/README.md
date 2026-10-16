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
2. Linux command line download (looks up the current file name, so it keeps working after point releases):
   ```
   BASE=https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd
   wget -c $BASE/SHA512SUMS
   ISO=$(awk '$2 ~ /-DVD-1\.iso$/ {print $2}' SHA512SUMS)
   wget -c $BASE/$ISO
   ```
3. Verify the download (on Windows use `certutil -hashfile <file>.iso SHA512` and compare with the `SHA512SUMS` file). Expect `<file>.iso: OK`:
   ```
   sha512sum -c --ignore-missing SHA512SUMS
   ```
   To also verify the signature of `SHA512SUMS` see https://www.debian.org/CD/verify

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
          Removable disks have `1` in the `RM` column (not shown above); here `sdb` and `sdc` are both removable.

        - Linux command to write image to USB drive - (https://www.debian.org/releases/trixie/amd64/ch04s03.en.html)
          > [!WARNING]
          > Everything on the target drive is erased. Use the whole disk (`/dev/sdX`), never a partition (`/dev/sdX1`). Unplug the USB drive, run `lsblk`, plug it in and run `lsblk` again: the disk that appeared is the one to use. In the example above `sdb1` is mounted at `/media/kkiragu/docs` so it holds files; the stick to write is `sdc`.

          Unmount any mounted partitions of the drive, then write the image (no formatting needed; the image replaces the partition table and is bootable on both BIOS and UEFI):
          ```
          sudo umount /dev/sdX1
          sudo dd if=debian-13.X.0-amd64-DVD-1.iso of=/dev/sdX bs=4M status=progress conv=fsync
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
6. Remember to note down the root credentials (username & password) during installations. You will also be prompted to create a new primary user. If you left the root password empty, this user is added to the `sudo` group; if you set a root password, add the user yourself (log in as root and run `usermod -aG sudo username`).
7. Once installation is complete, proceed to configure your OS for updates etc.

### Configuration of OS for Updates and Package Installations
> [!NOTE]
> During Debian installation, you created a primary user/username. Those credentials will come in handy in the next steps.
> If you're new to Linux and command line, you likely will want to substitute any instances of the editor usage of `vi` with beginner editors e.g. `gedit` or `nano`.
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
   3. Install gedit (desktop only):
      ```
      sudo apt install gedit
      ```
4. Editing application options:
   - gedit - ideal for beginners OR
   - vi/vim - shell application that's ideal for experienced Linux users
      - Install vim: For some reason vim is usually not installed fully: `sudo apt install vim`
      - Start: `vi /path/to/file/to/be/edited`
5. Edit the APT sources. Debian 13 uses the deb822 format: the default file is `/etc/apt/sources.list.d/debian.sources` and `/etc/apt/sources.list` normally holds only comments.
   1. Backup the sources in case something goes awry:
      ```
      mkdir -p ~/backup
      cp /etc/apt/sources.list.d/debian.sources ~/backup/debian.sources.d$(date +"%Y%m%d").t$(date +"%H%M%S").bak
      ```
   2. If you installed from the DVD and a `deb cdrom:` line exists (check with `grep -r cdrom /etc/apt/sources.list /etc/apt/sources.list.d/`), delete or comment it out, otherwise `apt update` asks for the disc.
   3. Open the file:
      ```
      sudo vi /etc/apt/sources.list.d/debian.sources
      ```
   4. A default install looks like this:
      ```
      Types: deb
      URIs: http://deb.debian.org/debian
      Suites: trixie trixie-updates
      Components: main
      Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

      Types: deb
      URIs: http://deb.debian.org/debian-security
      Suites: trixie-security
      Components: main
      Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
      ```
   5. Add `contrib non-free non-free-firmware` to `Components` (and `deb-src` to `Types` if you need source packages). Feel free to choose an alternative mirror in `URIs` instead of the default `deb.debian.org` - doesn't make much difference if you have a good internet connection:
      ```
      Types: deb deb-src
      URIs: http://deb.debian.org/debian
      Suites: trixie trixie-updates
      Components: main contrib non-free non-free-firmware
      Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

      Types: deb deb-src
      URIs: http://deb.debian.org/debian-security
      Suites: trixie-security
      Components: main contrib non-free non-free-firmware
      Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
      ```
   6. Only if you want backports, add `trixie-backports` to `Suites` of the first stanza (the suite must match your release, not an older one).
   7. If you still have one-line `.list` files (e.g. from an upgrade or third-party repositories), `sudo apt modernize-sources` converts them to `.sources` and keeps `.list.bak` copies.

6. Update your Debian OS installation:
   - Fetch latest version of the package list from Debian repo and 3rd party repos:
     ```
     sudo apt update
     ```
   - Download and install for any outdated packages:
     ```
     sudo apt full-upgrade
     ```

### Older Debian Versions e.g. Stretch, Buster & Bullseye

> [!NOTE]
> Stretch, Buster and Bullseye are end of life and now live on `archive.debian.org`. The archive's `Release` files have expired, so add `-o Acquire::Check-Valid-Until=false` to `apt update`. This section is kept for reference only.

#### Update old instance of Bullseye OR (Upgrade from Debian 10.X Buster to Debian 11.X Bullseye)

```
deb http://archive.debian.org/debian bullseye main contrib non-free
deb http://archive.debian.org/debian bullseye-updates main contrib non-free
deb http://archive.debian.org/debian-security bullseye-security main contrib non-free
```

#### Update old instance of Buster OR (Upgrade from Debian 9.X Stretch to Debian 10.X Buster)

```
deb http://archive.debian.org/debian/ buster-updates main contrib non-free
deb-src http://archive.debian.org/debian/ buster-updates main contrib non-free
deb http://archive.debian.org/debian buster main contrib non-free
deb-src http://archive.debian.org/debian buster main contrib non-free
deb http://archive.debian.org/debian-security/ buster/updates main contrib non-free
deb-src http://archive.debian.org/debian-security/ buster/updates main contrib non-free
```

#### Update Debian 9.X Stretch OR (Upgrade Debian 7.X Jessie to Debian 8.X Stretch)

```
deb http://archive.debian.org/debian/ stretch main contrib non-free
deb http://archive.debian.org/debian/ stretch-proposed-updates main contrib non-free
deb http://archive.debian.org/debian-security stretch/updates main contrib non-free
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

OPTIONAL - If the new user will use ssh key authentication later. Steps:
1. Switch to the new user: `sudo su - jdoe`
2. Prefer that the user generates their own key pair on their own machine (`ssh-keygen -t ed25519`, with a passphrase) and sends you only the public key (`~/.ssh/id_ed25519.pub`), so the private key never exists on the server. Create the folder and install the key:
   ```
   mkdir -p ~/.ssh && chmod 700 ~/.ssh
   vi ~/.ssh/authorized_keys   # paste the public key
   chmod 600 ~/.ssh/authorized_keys
   ```

## Terminal Application Customizations

Optional but recommended

### Install ZSH and Oh-My-Zsh

This is highly recommended for newbies to the command line.

1. Install zsh and dependencies (zsh is the base of oh-my-zsh):
   ```
   sudo apt install zsh curl git fonts-powerline powerline
   ```

2. Change to the user which you want to install oh-my-zsh e.g.: `su - jdoe`
3. Run oh my zsh install script:
   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```
4. Install theme e.g. powerlevel9k (no longer maintained; its successor is [powerlevel10k](https://github.com/romkatv/powerlevel10k), which uses a different `ZSH_THEME` value and `POWERLEVEL10K_*` settings):
   ```
   git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
   ```
5. Run the following (NB: This updates `.zshrc` file):
   ```
   sed -i 's/\(ZSH_THEME="robbyrussell"\)/#\1\nZSH_THEME="powerlevel9k\/powerlevel9k"/g' ~/.zshrc
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

   echo "$strPowerlevel9k" >> ~/.zshrc
   ```

9. If you’ll be using nvm to install and manage node/npm, add the following to the .zshrc file:
   ```
   export NVM_DIR=~/.nvm
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
   ```
10. Start the powerline daemon with your session (installed in step 1):
    ```
    systemctl --user enable --now powerline-daemon.service
    ```
11. For user postgres (or root): Install but don’t set it as default. Then start by:

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
   sudo tee /etc/apt/sources.list.d/google-chrome.list << 'EOF'
   deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main
   EOF
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
3. AnyDesk (use the following link; for key warnings see Key Ring Issues below)- http://deb.anydesk.com/howto.html

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
   2. To make it permanent once installed: add the option to `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub` (e.g. `"quiet splash nomodeset"`), then run `sudo update-grub`.

###  Key Ring Issues

`apt-key` and `/etc/apt/trusted.gpg.d/` are deprecated: a key placed there is trusted for every repository. Give each third-party repository its own keyring and reference it with `signed-by`, as in the Chrome section above (or `Signed-By:` in a `.sources` file).

To resolve key ring warnings from `apt update` for a repository (here AnyDesk; the key URL is also on http://deb.anydesk.com/howto.html):
```
curl -fsSL https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo gpg --dearmor -o /usr/share/keyrings/anydesk.gpg
```
Then add `signed-by=/usr/share/keyrings/anydesk.gpg` to that repository's `deb` line (or `Signed-By:` in its `.sources` file) and remove any old copy of the key from `/etc/apt/trusted.gpg.d/` or `/etc/apt/trusted.gpg`.

## Additional Resources
> [!TIP]
> The following might be helpful to get your Linux PC or Server appropriately configured:

1. [PostgreSQL - Installing, Configuring & Uninstalling](../database/README.md)
2. [Configuring Linux Desktop & Installing LibreOffice, IDEs etc](../desktop/README.md)

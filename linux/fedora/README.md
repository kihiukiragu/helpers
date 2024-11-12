# Fedora 41 Installation Guide
If you’re new to Linux, welcome aboard!

## Download Debian

Download an ISO containing the last version of Fedora which also bundles non-free firmware from this link: https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ (scroll down to the bottom of page and download .iso file)

1. Windows - download it using your prefered download manager or browser (Chrome / Firefox)
2. Linux command line download:
> [!IMPORTANT]
> If the URL below in the wget statement is broken go to https://cdimage.debian.org/cdimage/release/current/amd64/iso-dvd/ and download the `.iso` file.
```
wget -c https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso 
```

## Configure Fedora
### Enable & Start sshd

Check status of sshd:
```
sudo systemctl status sshd
```
 If it shows disabled, then you need to enable and start it.

Enable and start the sshd daemon (this a one-time thing):
```
sudo systemctl enable sshd
sudo systemctl start sshd
```

### Desktop Environments
To install Cinnamon, KDE Plasma and XFCE:
```
sudo dnf install @cinnamon-desktop-environment @kde-desktop-environment @xfce-desktop-environment
```


### Oh-My-Zsh

1. Install deps:
   ```
   sudo dnf install zsh curl git powerline
   ```

## Update / Upgrade Fedora

Simply type:
```
sudo dnf upgrade
```



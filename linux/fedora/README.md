> [!WARNING]
> This Fedora 41 Workstation installation guide is a very rough draft and incomplete. This banner will be removed once it's stable.

# Fedora 41 Workstation Installation Guide
If you’re new to Linux, welcome aboard!

## Download Debian

Download an ISO containing the last version of Fedora which also bundles non-free firmware from this link: https://fedoraproject.org/workstation/download (download the .iso file that suits your processor. For most folks, that will be AMD x86_64 systems):

1. Windows - download it using your prefered download manager or browser (Chrome / Firefox)
2. Linux command line download:
> [!IMPORTANT]
> If the URL below in the wget statement is broken go to https://fedoraproject.org/workstation/download and download the `.iso` file.
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
2. Proceed with #2 of the following [steps](https://github.com/kihiukiragu/helpers/tree/main/linux/debian#install-zsh-and-oh-my-zsh-optional)

## Update / Upgrade Fedora

Simply type:
```
sudo dnf upgrade
```



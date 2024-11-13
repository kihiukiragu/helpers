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

## Install Google Chrome

Install Third-Party Repositories:
```
sudo dnf install fedora-workstation-repositories
```

Output:
```
Updating and loading repositories:
 RPM Fusion for Fedora 41 - Nonfree - NVIDIA Driver                                   100% |   7.1 KiB/s |  24.8 KiB |  00m04s
 RPM Fusion for Fedora 41 - Nonfree - Steam                                           100% |   7.4 KiB/s |  20.4 KiB |  00m03s
 google-chrome                                                                        100% |   3.1 KiB/s |   3.3 KiB |  00m01s
 Copr repo for PyCharm owned by phracek                                               100% |   1.7 KiB/s |   3.9 KiB |  00m02s
Repositories loaded.
Package "fedora-workstation-repositories-38-6.fc41.x86_64" is already installed.
```

Enable Google Chrome repo:
```
sudo dnf config-manager setopt google-chrome.enabled=1
```

Install
```
sudo dnf install google-chrome-stable
```

Output:
```
Updating and loading repositories:
Repositories loaded.
Package                                                          Arch           Version                                                          Repository                               Size
Installing:
 google-chrome-stable                                            x86_64         131.0.6778.69-1                                                  google-chrome                       349.9 MiB
Installing dependencies:
 liberation-fonts-all                                            noarch         1:2.1.5-12.fc41                                                  fedora                                0.0   B

Transaction Summary:
 Installing:         2 packages

Total size of inbound packages is 110 MiB. Need to download 110 MiB.
After this operation, 350 MiB extra will be used (install 350 MiB, remove 0 B).
Is this ok [y/N]: y
[1/2] liberation-fonts-all-1:2.1.5-12.fc41.noarch                         100% |   1.4 KiB/s |   8.1 KiB |  00m06s
[2/2] google-chrome-stable-0:131.0.6778.69-1.x86_64                       100% |   7.6 MiB/s | 110.5 MiB |  00m14s
------------------------------------------------------------------------------------------------------------------
[2/2] Total                                                               100% |   6.6 MiB/s | 110.5 MiB |  00m17s
[1/3] https://dl.google.com/linux/linux_signing_key.pub                   100% |  54.5 KiB/s |  16.5 KiB |  00m00s
------------------------------------------------------------------------------------------------------------------
[3/3] Total                                                               100% |   6.6 MiB/s | 110.5 MiB |  00m17s
Importing PGP key 0x7FAC5991:
 UserID     : "Google, Inc. Linux Package Signing Key <linux-packages-keymaster@google.com>"
 Fingerprint: 4CCA1EAF950CEE4AB83976DCA040830F7FAC5991
 From       : https://dl.google.com/linux/linux_signing_key.pub
Is this ok [y/N]: y
The key was successfully imported.
Importing PGP key 0xD38B4796:
 UserID     : "Google Inc. (Linux Packages Signing Authority) <linux-packages-keymaster@google.com>"
 Fingerprint: EB4C1BFD4F042F6DDDCCEC917721F63BD38B4796
 From       : https://dl.google.com/linux/linux_signing_key.pub
Is this ok [y/N]: y
The key was successfully imported.
[1/4] Verify package files                                                100% |   5.0   B/s |   2.0   B |  00m00s
[2/4] Prepare transaction                                                 100% |  12.0   B/s |   2.0   B |  00m00s
[3/4] Installing liberation-fonts-all-1:2.1.5-12.fc41.noarch              100% |   8.6 KiB/s | 124.0   B |  00m00s
[4/4] Installing google-chrome-stable-0:131.0.6778.69-1.x86_64            100% |  70.9 MiB/s | 349.9 MiB |  00m05s
Complete!
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



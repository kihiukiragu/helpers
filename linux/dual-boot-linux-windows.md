# Dual Boot Linux and Windows

You might want to have Linux and Windows on the same PC. Follow this guide to make this happen.

## UEFI Bootable USB using Ventoy
> [!NOTE]
> This section is NOT necessary if the installation targeted PC has an option for Legacy BIOS boot mode. However, most modern PCs have UEFI and this can make your life easier in terms of making a USB that contains several ISOs and you can just overwrite the files when you get a newer one. With UEFI you don't have to worry about tinkering with making BIOS changes other than boot sequence.

Some PC manufactures have started to abandon support for Legacy BIOS boot support in favor of the new UEFI boot mode support ONLY.
To ensure your USB is recognized by a UEFI Boot mode, you can utilize Ventoy to make your USB UEFI bootable:
- Download Ventoy tar/zip file for Linux: https://www.ventoy.net/en/download.html
- Untar the file (in a suitable folder of your choice):
  ```
  tar -xvf ventoy-1.0.99-linux.tar.gz
  ```
- Run the VentoyWeb.sh:
  - Go to options and switch partition type from `MBR` to `GPT`.
  - Click on `Install`.
  
- The above process will create 2 partitions:
  1. VTOYEFI - contains the Ventoy Software. Leave this as is.
  2. A free `dos` partion - you can figure out what drive it is by executing `lsblk`

- Format the free `dos` partion space to ext4 so that it is visible in Linux eg:
  ```
  sudo mkfs -t ext4 /dev/sdbX # where X will be a number eg sdb1 or sdb2 etc
  ```
- Copy as many ISO files to the ext4 partion part of the USB eg you can have CentOS, Debian, Fedora, Ubuntu ISO's on one Ventoy USB drive:
  ```
  sudo cp /path/to/iso/file(s)
  sudo sync
  ```
- Proceed to boot from USB and install Windows

### Windows & Partitioning & Shrinking and Reclaiming Space
## Install Windows First
Windows OS requires primary partition on a PC to be formatted to NTFS format. For this reason, Windows has to go first!

Steps:
- Boot with your USB (Ventoy or Other) device containing Windows
- Select: `Custom: Install Windows only (advanced)`
- When presented with the question `Where do you want to install Windows?`, *AND* you only have 1 disk on the PC:
  - Click on `*New` to create a new partion
  - You will be required to enter the size of the new partition. The number displayed by default will be the total MBs on your disk
  - For beginners, roughly divide that number by 2 and enter the number. This means half for Windows, and half for Linux. For advanced users, pick a partition size that works for you.
  - Click `Apply` and you will have the following partions:
    - Drive 0 Partion 1: System Reserved
    - Drive 0 Partion 2: Primary # This is where Windows will be installed
    - Drive 0 Unallocated Space # This is where Linux will be installed later
- Click `Next` to start Windows installation
- Once finished, you can either boot into Windows to ensure it installed ok.
- Restart the PC and then installe the Linux Distro of your choice.

## Windows Already Installed and occupies all available space
If Windows was installed and all the partion space taken, you can:
- Shrink the Windows partion and
- Reclaim the space you want to have for Fedora or Debian etc installation.

This process will be available during the Linux installation. Play close attention so as to indicate that you are reclaiming and not overriding the Windows partion and therefore getting rid of Windows!

## Install Linux after Windows
Boot with a Linux Distro bootable source and proceed to follow the Debian or Fedora installation guides.
  
## Other Options
### Creating a Bootable USB from a Windows ISO
This will work for Legacy USB Boot PCs but *NOT* for newer UEFI ONLY Boot options:
```
sudo dd bs=4M if=/media/kkiragu/isumsoft/Win11_24H2_EnglishInternational_x64.iso of=/dev/sdc1 status=progress oflag=sync
```

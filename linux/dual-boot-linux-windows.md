# Dual Boot Linux and Windows

You might want to have Linux and Windows on the same PC. Follow this guide to make this happen.

## UEFI Bootable USB using Ventoy
> [!NOTE]
> This section is NOT necessary if the installation targeted PC has an option for Legacy BIOS boot mode.

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
  
- (This might NOT be necessary if you chose the `GPT` option above) Format the free space to ext4 so that it is visible in Linux:
  ```
  sudo mkfs -t ext4 /dev/sdb1
  ```
- Copy as many ISO files to the ext4 partion part of the USB eg you can have CentOS, Debian, Fedora, Ubuntu ISO's on one Ventoy USB drive:
  ```
  sudo cp /path/to/iso/file(s)
  sudo sync
  ```
- Proceed to boot from USB and install Windows

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

## Install Linux after Windows
Boot with a Linux Distro bootable source and proceed to follow the Debian or Fedora installation guides.
  
## Other Options
### Creating a Bootable USB from a Windows ISO
This will work for Legacy USB Boot PCs but *NOT* for newer UEFI ONLY Boot options:
```
sudo dd bs=4M if=/media/kkiragu/isumsoft/Win11_24H2_EnglishInternational_x64.iso of=/dev/sdc1 status=progress oflag=sync
```

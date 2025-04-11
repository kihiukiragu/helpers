# Dual Boot Linux and Windows

You might want to have Linux and Windows on the same PC. Follow this guide to make this happen.

## Windows Users - Preparing Ventoy USB
- Get a blank USB Flash/Thumb Drive 8GB minimum.
- Insert it in the USB drive.
- Access `My Computer` and make note of the driver letter representing the USB Flash drive eg `L:\` (this will vary from PC to PC).
- Downloading Ventoy:
  - Download the Ventoy Software ventoyu.net
  - Download the zip file - ensure the windows zip file
  - Unzip/Extract the zip file. You'll get a folder eg `Ventoy-1.0.93`
- Running Ventoy - Inside the folder, doubleclick on the `Ventoy2Disk.exe` file. This will start the Ventoy program.
  - Ventoy will try to guess the USB drive. Correct it by picking the right drive as earlier identified if it's not the right one.
  - Click on install and accept to formatting "The device will be formatted and all the data will be lost. Continue?".
  - Close all open Windows after that process is complete.
- Downloading Debian/Linux:
  - Use the [Debian 12.X (Bookworm) Installation Guide #Download](debian/README.md#download-debian) just to download the ISO file.
  - Go to `My Computer` and copy and paste the ISO file to the USB flash
  - Return to the [Debian 12.X (Bookworm) Installation Guide](debian/README.md) and start the Debian/Linux process.

## Linux - UEFI Bootable USB using Ventoy
> [!NOTE]
> This section is NOT necessary if the installation targeted PC has an option for Legacy BIOS boot mode. However, most modern PCs have UEFI and this can make your life easier in terms of making a USB that contains several ISOs and you can just overwrite the files when you get a newer one. With the UEFI specification you don't have to worry about tinkering with making BIOS changes other than boot sequence.

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
  2. A free `dos` partition - you can figure out what drive it is by executing `lsblk`

- Format the free `dos` partition space to ext4 so that it is visible in Linux eg:
  ```
  sudo mkfs -t ext4 /dev/sdbX # where X will be a number eg sdb1 or sdb2 etc
  ```
- Copy as many ISO files to the ext4 partition part of the USB e.g. you can have CentOS, Debian, Fedora, Ubuntu ISO's on one Ventoy USB drive:
  ```
  sudo cp /path/to/iso/file(s)
  sudo sync
  ```
- Proceed to boot from USB and install Windows

### Windows & Partitioning & Shrinking and Reclaiming Space
## Windows Already Installed and occupies all available space
If Windows was installed and all the partition space taken, you can:
- Shrink the Windows partition by:
  - Start menu, run `Disk Management` or `partition manage` (Run as administrator).
  - Right click on `C:` drive and select `Shrink Volume`.
  - In the 3rd field ("Enter the amount of space to shrink"), enter an amount larger than 25000 (ie ~25 GB).
  - Click on `Shrink`. This will create space that will be used during Debian / Fedora Linux installation.
- CAUTION: Next you can proceed to Linux installation. However, pay close attention during Linux installation so you only use the space that you shrunk in the previous steps and do not accidentally install over the existing Windows installation.
- Return to the [Debian 12.X (Bookworm) Installation Guide](debian/README.md) and start the Debian/Linux process.

## Windows does NOT Exist - Install Windows First
Windows OS requires primary partition on a PC to be formatted to NTFS format. For this reason, Windows has to go first!

Steps:
- Boot with your USB (Ventoy or Other) device containing Windows
- Select: `Custom: Install Windows only (advanced)`
- When presented with the question `Where do you want to install Windows?`, *AND* you only have 1 disk on the PC:
  - Click on `*New` to create a new partition
  - You will be required to enter the size of the new partition. The number displayed by default will be the total MBs on your disk
  - For beginners, roughly divide that number by 2 and enter the number. This means half for Windows, and half for Linux. For advanced users, pick a partition size that works for you.
  - Click `Apply` and you will have the following partitions:
    - Drive 0 Partition 1: System Reserved
    - Drive 0 Partition 2: Primary # This is where Windows will be installed
    - Drive 0 Unallocated Space # This is where Linux will be installed later
- Click `Next` to start Windows installation
- Once finished, you can either boot into Windows to ensure it installed ok.
- Restart the PC and then install the Linux Distro of your choice.

This process will be available during the Linux installation. Pay close attention to indicate that you are reclaiming and not overriding the Windows partition and therefore getting rid of Windows!

## Install Linux after Windows
Boot with a Linux Distro bootable source and proceed to follow the Debian or Fedora installation guides.
  
## Other Options
### Creating a Bootable USB from a Windows ISO
This will work for Legacy USB Boot PCs but *NOT* for newer UEFI ONLY Boot options:
```
sudo dd bs=4M if=/media/kkiragu/isumsoft/Win11_24H2_EnglishInternational_x64.iso of=/dev/sdc1 status=progress oflag=sync
```

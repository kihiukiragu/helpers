> [!IMPORTANT]
> It's always a good idea to back up your most important files, photos, videos before running an Operating System. A small misstep could wipe out the wrong hard-drive or partition.

# Dual Boot Linux and Windows

You might want to have Linux and Windows on the same PC. Follow this guide to make this happen.

## Windows Users
### Preparing Ventoy USB
- Get a blank USB Flash/Thumb Drive 8GB minimum.
- Insert it in the USB drive.
- Access `My Computer` and make note of the driver letter representing the USB Flash drive eg `L:` (this will vary from PC to PC).
- Downloading Ventoy:
  - Navigate to the Ventoy Software Download page https://www.ventoy.net/en/download.html
  - Download the **Windows** zip file.
  - Unzip/Extract the zip file. You'll get a folder e.g. `Ventoy-1.1.05`.
- Running Ventoy - Inside the folder, doubleclick on the `Ventoy2Disk.exe` file. This will start the Ventoy program.
  - Ventoy will try to guess the USB drive. Correct it by picking the right drive as earlier identified if it's not the right one.
  - Click on install and accept to formatting "The device will be formatted and all the data will be lost. Continue?".
  - Close all open Windows after installation process is complete.
- Downloading Debian/Linux:
  - Use the [Debian 13.X (Bookworm) Installation Guide #Download](debian/README.md#download-debian) just to download the ISO file.
  - Go to `My Computer` and copy and paste the downloaded ISO file to the USB flash.
- IMPORTANT: See Windows & Partitioning section below to reserve/dedicate space on your PC hard-drive for Linux installation.
- Once you have space reserved, resume to the [Debian 13.X (Bookworm) Installation Guide](debian/README.md) and start the Debian/Linux process.

### Windows & Partitioning & Shrinking and Reclaiming Space
#### Windows Already Installed and Occupies All Available space
If Windows was installed and all the partition space taken, you can:
- Shrink the Windows partition by:
  - Start menu, run `Disk Management` or `partition manage` (Run as administrator).
  - Right click on `C:` drive (or any other hard-drive if one exists) and select `Shrink Volume`.
  - In the 3rd field ("Enter the amount of space to shrink"), enter an amount larger than 30000 (ie ~30 GB) but not larger than 50,000 unless you have the space that is.
  - This leaves a block of unallocated space labeled "Free Space" or "Unallocated". Leave it exactly like that—do not format it or assign a drive letter.
  - Click on `Shrink`. This will create space that will be used during Debian / Fedora Linux installation.
- CAUTION: Next you can proceed to Linux installation. However, pay close attention during Linux installation so you only use the space that you shrunk in the previous steps and do not accidentally install over the existing Windows installation.
  - Choose the Right Method: Select Guided - use the largest continuous free space. This tells the installer to only look at the blank 50GB space you created in Step 1.
  - Review the Partition Map: * Your existing Windows partitions will usually be labeled as ntfs or fat32.
    - Ensure there is no formatting flag (like a lowercase f or a "Format" checkmark) next to any of your Windows ntfs partitions.
    - Look for the new Linux partitions (usually ext4 assigned to / and a small swap partition). These should have the formatting flag.
    ```shell
    This is an overview of your currently configured partitions and mount points. Select a partition to modify its settings (file system, mount point, etc.), or invoke "Guided partitioning" to start over.

      Guided partitioning
      Configure software RAID
      Configure the Logical Volume Manager
      Configure encrypted volumes
      Configure iSCSI volumes

      LVM VG ventoy, LV ventoy - 4.0 GB Linux device-mapper (linear)
      ▼ SCSI1 (0,0,0) (sda) - 256.1 GB ATA MTFDDAV256MBF-1A
        >      #1  primary    52.4 MB   B      ntfs
        >      #2  primary   202.9 GB          ntfs
        >      #5  logical    49.7 GB   f      ext4           /
        >      #6  logical     2.7 GB   f      swap           swap
        >      #3  primary   633.3 MB          ntfs
      ▼ SCSI7 (0,0,0) (sdb) - 31.0 GB USB DISK 3.0
        >               1.0 MB          FREE SPACE
        >      #1       31.0 GB                        Ventoy
        >      #2       33.6 MB         fat16          VTOYEFI
        >               3.6 kB          FREE SPACE

      Undo changes to partitions
      Finish partitioning and write changes to disk
    ```
  - The Final Confirmation Check (for partitioning) Before any changes are actually written to your drive, the installer will throw a final confirmation screen summary. Always pause here and read carefully:
    - The Rule: The summary must only state that it is formatting the new Linux partitions (e.g., partition #5 as ext4 and partition #6 as swap).
    - The Red Flag: If you see any mention of formatting an ntfs partition, or if a partition matching the size of your Windows drive (e.g., ~200GB) is listed under "going to be formatted", DO NOT PROCEED. Cancel or turn off the machine.
    - NB: If only the Linux partitions are listed to be formatted, select Yes to write changes to disk. GRUB will safely install alongside Windows, allowing you to choose your OS at every boot.
    ```shell
    Partition disks

    If you continue, the changes listed below will be written to the disks. Otherwise, you will be able to make further changes manually.

    The partition tables of the following devices are changed:
       SCSI1 (0,0,0) (sda)

    The following partitions are going to be formatted:
       partition #5 of SCSI1 (0,0,0) (sda) as ext4
       partition #6 of SCSI1 (0,0,0) (sda) as swap

    Write the changes to disks?

      ( ) No
      (*) Yes
    ```
- Return to the [Debian 13.X (Bookworm) Installation Guide](debian/README.md) and start the Debian/Linux process.
- You might encounter a GRUB Boot loader installation question as follows:
  ```shell
  Install the GRUB boot loader

  The following other operating systems have been detected on this computer: Windows Vista

  If all of your operating systems are listed above, then it should be safe to install the boot loader to your primary drive (UEFI partition/boot record). When your computer boots, you will be able to choose to load one of these operating systems or the newly installed Debian system.

  Install the GRUB boot loader to your primary drive?

    ( ) No
    (*) Yes
  ```
  And then (NOTE: make sure to select `/dev/sda` and NOT `/dev/sdb` is the removable media eg USB drive or CD/DVD:
  ```shell
  Install the GRUB boot loader

  You need to make the newly installed system bootable, by installing the GRUB boot loader on a bootable device. The usual way to do this is to install GRUB to your primary drive (UEFI partition/boot record). You may instead install GRUB to a different drive (or partition), or to removable media.

  Device for boot loader installation:

    Enter device manually
    /dev/sda (ata-MTFDDAV256MBF-1AN15ABHA_16451493F785)
    /dev/sdb (usb-_USB_DISK_3.0_070A4864D4AF8F88-0:0)
  ```

#### Windows does NOT Exist - Install Windows First
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

- CAUTION: Next you can proceed to Linux installation. However, pay close attention during Linux installation so you only use the space that you shrunk in the previous steps and do not overriding the Windows partition and therefore getting rid of Windows!
- Return to the [Debian 13.X (Bookworm) Installation Guide](debian/README.md) and start the Debian/Linux process.

## Linux Users - UEFI Bootable USB using Ventoy
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

### Other Linux USB Creation Options - Creating a Bootable USB from a Windows ISO
This will work for Legacy USB Boot PCs but *NOT* for newer UEFI ONLY Boot options:
```
sudo dd bs=4M if=/media/kkiragu/isumsoft/Win11_24H2_EnglishInternational_x64.iso of=/dev/sdc1 status=progress oflag=sync
```

### Install Linux after Windows
Boot with a Linux Distro bootable source and proceed to follow the Debian or Fedora installation guides.

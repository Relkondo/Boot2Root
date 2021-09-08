Bonus 2 - Manipulating the ISO

We can extract the filesystem from the iso.

For that we’ll use pycdlib.

We made a script that allows us to explore the iso :

(_exploit_iso) ➜  $> ./exploit_iso.py '/' ~/Downloads/BornToSecHackMe-v1.1.iso
.
..
CASPER
INSTALL
ISOLINUX
MD5SUM.TXT;1
PRESEED
README.DISKDEFINES;1
UBUNTU.;1
_DISK

(_exploit_iso) ➜  $> ./exploit_iso.py '/CASPER' ~/Downloads/BornToSecHackMe-v1.1.iso
.
..
FILESYSTEM.MANIFEST;1
FILESYSTEM.MANIFEST_DESKTOP;1
FILESYSTEM.SIZE;1
FILESYSTEM.SQUASHFS;1
INITRD.GZ;1
README.DISKDE

Then, with the help of SquashFsImage, we extract the bh_history in root :

(_exploit_iso) ➜  $> ./exploit_iso.py '/CASPER/FILESYSTEM.SQUASHFS;1' '/root/.bash_history' ~/Downloads/BornToSecHackMe-v1.1.iso
Extract filesystem.squashfs from the iso ...
Downloading /root/.bash_history ...

(_exploit_iso) ➜  $>  cat output | grep "adduser" -A 2
…
adduser zaz
646da671ca01bb5d84dbb5fb2238dc8e
…

We have zaz. We can enter zaz and execute a DirtyCow or Return2Libc attack.


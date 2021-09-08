## Bonus 5 : Admin du Forum, autre methode

Sur la page https://192.168.0.30/phpmyadmin/ 

Allons sur la  base de données : forum_db

La seule table qui semble intéressante c'est mlf2_userdata mais il faut trouver quel hash est utilisé
Mais nous ne trouvons pas parmi les décrypteurs connus

Après quelques recherches, on s'aperçoit que le footer contient le lien de l'hébergeur : MyLittleForum

En allant dans la partie Code et en faisant des CmdF pour trouver le 'hash', on finit par trouver leur fonction de hashage :
https://github.com/ilosuna/mylittleforum/blob/master/includes/login.inc.php

On l'a donc utilisée pour hasher un nouveau mot de passe et le remplacer dans la base de données (cf fichier testhash.php)

On peut se connecter à l'espace admin du forum !

Little_owl
==========
*Little_owl* est un outil d'aide à l'administration réseau.
Il permet de découvrir l'environnement réseau local du poste qui l'utilise.
Dans le cas d'un poste connecté à Internet,
*Little_owl* peut donner l'adresse IP publique ainsi que la liste des routeurs récurants

L'utilisation des droits administrateur (*sudo*) est nécessaire au bon fonctionnement de l'outil.

*Little_owl* va scanner séparement l'activité des couches **Liaison** et **Réseau**.
Le protocole IPv4 est pleinement supporté.
Le protocole IPv6 est partiellement supporté, uniquement les informations du poste de travail sont recueillies.

Il est possible d'exporter le résultat d'une recherche au format JSON pour pouvoir le consulter ultérieurement sur un autre poste.


Fonctionnalités
"""""""""""""""
Les fonctionnalités disponibles sont décrites ci-dessous:

* scanner actif
* scanner passif
* scanner de ports TCP (SynScan) / UDP
* recherche de voisins
* découverte dhcp
* exportation json
* importation json
* résolution constructeur MAC
* découverte adresse IP publique
* découverte points de passages obligés



Installation
************
Cette section décrit le processus d'installation et de desintallation du programme

Pré-requis
""""""""""
Les modules suivants seront installés pour faire fonctionner l'outil:

* netifaces
* psutil
* scapy

L'utilisation de **scapy** requiert que le programme **tcpdump** soit installé et fonctionnel.

A partir de pip3
""""""""""""""""
Installation à partir de pip3

::

    pip3 install little_owl

Installation à partir du fichier .whl (*Remplacer X.Y.Z par la version*).

::

    pip3 install little_owl-X.Y.Z-py3-none-any.whl

A partir des sources
""""""""""""""""""""
Installation à partir des sources (*Remplacer X.Y.Z par la version*).

::

    tar -xzvf little_owl.X.Y.Z.tar.gz
    cd little_owl
    python3 setup.py install


Désintallation
**************
Cette section décrit la procédure de désinstallation

A partir de pip3
""""""""""""""""
Avec la commande :

::

    pip3 uninstall little_owl

    # Supprimer les modules python complémentaires
    # Attention, adapter cette commande si d'autres programmes ont besoin de ces modules
    pip3 uninstall scapy netifaces psutil

A partir des sources
""""""""""""""""""""
La désinstallation des sources doit se faire avec la suppression manuelle des fichiers installer.
Pour ce faire :

::

    # récupérer la liste des fichiers installés
    python3 setup.py install --record fichiers_lo.txt

    # Supprimer les fichiers
    xargs rm -rf < fichiers_lo.txt

    # Supprimer les modules python complémentaires
    # Attention, adapter cette commande si d'autres programmes ont besoin de ces modules
    pip3 uninstall scapy netifaces psutil

Usage
=====
Aide à l'usage

Les droits administrateurs sont nécessaire à la bonne execution du programme.

::

    little_owl -h
    usage: little_owl [-h] [-q] [-d SEC] [-l] [-s | -m | -r JSONF] [-e [JSONF]] [-o [FICHIER]] [-p]

    Decouverte des reseaux et machines voisines a partir du poste de travail. Scan passif, actif, et des ports ouverts.

    optional arguments:
        -h, --help                          show this help message and exit
        -q, --quiet                         l'affichage des infos et erreurs est désactivé
        -d SEC, --duree SEC                 temps en seconde pour le scan passif
        -l, --local                         recherche uniquement les informations des réseaux locaux
        -s, --single-p                      déroulé sequentiel du programme
        -m, --mulpi-p                       réalisation de scans en parallèle (par défaut)
        -r JSONF, --read JSONF              lecture et affichage d'un fichier JSONF de données au format json
        -e [JSONF], --export [JSONF]        fichier JSONF pour l'exportation des données au format json
        -o [FICHIER], --output [FICHIER]    fichier FICHIER de sortie pour l'affichage
        -p, --no-port                       Ne scanne pas les ports ouverts pour les machines détectées

    Attention ce programme n'est absolument pas discret, ENJOY


Sortie
======
Les informations recueillies et mise en forme par le programme sont:

* les informations sur le poste administrateur:
    * noms des interfaces réseaux
    * adresses MAC
    * constructeurs des interfaces réseaux
    * adresses IP associées
    * listes des ports en écoute par adresse IP
* la listes des machines avec:
    * adresses MAC détectées
    * adresses IP associées à l'adresse MAC
    * liste des ports ouvert TCP/UDP (uniquement pour les adresses IP privées)
* la liste des réseaux L2 (couche liaision du modèle OSI):
    * liste des machines détectées sur le réseaux
    * Informations DHCP
        * adresse BOOTPC
        * serveur DHCP
        * masque de sous réseau
        * offre IP
        * gateway
        * serveurs DNS
        * domaine
* la liste des réseaux L3 (couche Réseau)
    * liste des machines détectées sur le réseaux
    * gateway
    * adresse IP publique avec localisation
    * route par défaut avec adresse IP et localisation


Déroulement
===========
*little_owl* recherche dans un premier temps les informations du postes administrateur.
Pour cela il recherche les interfaces réseaux présentes et "UP".
Il récupère les adresses MAC et avec sa base de données des constructeurs, il détermine la marque.
Le nombre d'interface réseau découvertes va déterminer le nombre de réseau L2 qui seront créés.
Le nombre de réseaux L3 sera déterminé par le nombre d'adresse IP pour chaque interface réseau.
Le programme utilise également le module *psutils* pour déterminer les ports en écoutes pour chaque adresse IP.

Une fois l'ensemble des informations du poste administrateur recueillies,
*little_owl* va écouter passivement toutes ses interfaces réseaux et lancer une requête DHCP.
Si un serveur DHCP est présent les éléments de réponses seront associé au réseau.
Des machines pourront être détectée durant cette phase.

Le scan des réseaux L3 se fait de manière active à l'aide d'un ping scan.

Une fois l'ensemble des machines découvertes, le programme va rechercher des informations complémentaires
si la connectivité vers Internet est assurée. Il va pouvoir déterminer l'adresse IP publique ainsi que la route par défaut.
Cette route comporte la liste des routeurs qui semblent obligatoire pour rejoindre le WEB.
Pour ce faire plusieurs traceroute sont lancés vers plusieurs sites hébergés dans plusieurs pays.

Enfin *little_owl* effectue un scanne basique des ports TCP/UDP ouvert pour chaque machine qui a été détectée.
Ce scanne n'aura lieu pour les adresses IP privées.


Informations complémentaires
============================
De la documentation complémentaire sur les modules, les objets et l'utilisation de JSON est disponible dans le dossier :
*docs/*


Auteur
======
Programme écrit part GOEHRY Martial

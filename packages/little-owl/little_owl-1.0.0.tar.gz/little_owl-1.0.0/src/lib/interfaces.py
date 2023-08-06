#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Nom : interfaces.py - regroupement des fonctions liees aux NIC
# Auteur : GOEHRY Martial
# Date : 2020/03/29

# ========================================================================= #
# ===                            IMPORTATIONS                           === #
# ========================================================================= #
import netifaces
import psutil
import json
import sys
import re
import fcntl
import struct
from socket import *
import lib.tools as tools


# ========================================================================= #
# ===                             FONCTIONS                             === #
# ========================================================================= #
def get_ifaces():
    """
    :return List, la liste des interfaces de connexion disponible sans 'lo'
    """
    ifaces = netifaces.interfaces()
    ifaces.remove('lo')
    return ifaces


def get_iface_info(interface):
    """
    Recupere les informations a partir de l'interface donnee en argument
    :param interface: String, designant une interface de connexion (wifi, ethernet)
    :return Tuple de String, adresse mac, IP4/CIDR, IP6/CIDR
    """
    try:
        addr = netifaces.ifaddresses(interface)
    except ValueError:
        tools.debug("Fonction 'get_iface_info' : Valeur '{}' incorrect".format(interface))
        return None, None, None

    mac = addr[netifaces.AF_LINK][0]['addr']    # Problème avec VPN pas de AF_LINK

    if netifaces.AF_INET in addr:
        ip4 = addr[netifaces.AF_INET][0]['addr']
        nm4 = addr[netifaces.AF_INET][0]['netmask']
    else:
        ip4 = nm4 = None

    if netifaces.AF_INET in addr:
        ip6 = addr[netifaces.AF_INET6][0]['addr'].split('%')[0]
        nm6 = addr[netifaces.AF_INET6][0]['netmask']
    else:
        ip6 = nm6 = None

    if ip4 and nm4:
        ip4_cidr = ip4 + '/' + tools.nm4_to_cidr(nm4)
    else:
        ip4_cidr = None

    if ip6 and nm6:
        ip6_cidr = ip6 + '/' + tools.nm6_to_cidr(nm6)
    else:
        ip6_cidr = None

    return mac, ip4_cidr, ip6_cidr


def import_mac_db(path):
    """
    Importe la base de donnees des compagnies ayant des adresses MAC attribuees.
    Telechargement du fichier JSON :  https://macaddress.io/database-download
    Chemin du fichier par default : ./data/macaddress.io-db.json
    :param path: chemin vers le fichier JSON a importer
    :return None ou les donnees dans une liste
    """
    try:
        with open(path, 'r') as f:
            data = f.read().split('\n')
            if not data:
                print("Pas de donnees pour les adresses MAC", file=sys.stderr)
                return None
            return data
    except FileNotFoundError:
        return None


def get_mac_vendor(mac, data):
    """
    Recherche le constructeur lie a l'adresse mac
    :param mac: String, une adresse mac
    :param data: la base de donnee des constructeur une fois chargee
    :return String, le nom de le compagnie et le bigramme du pays
    """
    if not data:
        return 'NULL'
    mac_id = mac[:8].upper()
    for line in data:
        try:
            entry = json.loads(line)
        except json.decoder.JSONDecodeError:
            return 'NULL'
        if mac_id == entry["oui"]:
            return entry.get('companyName', 'Inconnu') + '; ' + entry.get('countryCode', 'Inconnu')
    return 'Inconnu'


def is_mac(mac):
    """
    Regarde une chaine de caractere est bien une adresse mac valide
    :param mac: str, une adresse mac
    :return: Bool, True si mac est une adresse mac valide
    """
    if isinstance(mac, str):
        return True if re.match('^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$', mac) else False
    return False


def is_up(iface):
    """
    Regarde si une interface reseau est up ou down.
    https://www.oreilly.com/library/view/python-cookbook/0596001673/ch07s05.html
    :param iface: str, le nom de l'interfae
    :return: bool, True si UP, False si DOWN
    """
    SIOCGIFFLAGS = 0x8913
    null256 = '\0' * 256

    s = socket(AF_INET, SOCK_DGRAM)
    result = fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, iface + null256)
    flags, = struct.unpack('H', result[16:18])
    up = flags & 1

    return (False, True)[up]


def open_adm_ports():
    """
    Recupere la liste des ports ouverts pour la machine administrateur
    :return: list
    """
    return [con for con in psutil.net_connections() if con.status == 'LISTEN']

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================================= #
# ===                        IMPORTATIONS                               === #
# ========================================================================= #
import ipaddress
import sys
import os

import obj
import lib
import data.settings as settings
from getpass import getuser
from socket import gethostname


# ========================================================================= #
# ===                          FONCTIONS                                === #
# ========================================================================= #
def nm4_to_cidr(netmask):
    """
    Transforme un netmask 255.255.255.0 en notation CIDR
    :param netmask: String, le masque de sous reseau
    :return: String, l'equivalent en CIDR
    """
    return str(sum(bin(int(x)).count('1') for x in netmask.split('.')))


def nm6_to_cidr(netmask):
    """
    Transforme un netmask IPv6 en notation CIDR
    :param netmask: String, le masque de reseau
    :return: String, l'equivalent CIDR
    """
    bits = []
    for x in netmask.split(':'):
        if not x:
            break
        bits.append(bin(int(x, 16)))
    return str(sum(x.count('1') for x in bits))


def username():
    """
    Recupere le nom d'utilisateur de la machine courante
    :return: String, nom d'utilisateur
    """
    return getuser()


def hostname():
    """
    Recupere le nom de la machine
    :return: String, le nom de la machine
    """
    return gethostname()


def info(message):
    """
    Affiche un message d'infirmation sur la console
    :param message: String, message a afficher
    :return: None
    """
    if not settings.QUIET:
        print("INFO : <{}>".format(message))


def debug(message):
    """
    Affiche un message d'infirmation sur la console
    Pour activer ces message il faut mettre DEBUG a True dans data/settings.py
    :param message: String, message a afficher
    :return: None
    """
    if settings.DEBUG:
        print("DEBUG : <{}>".format(message))


def error(message):
    """
    Affiche un message d'infirmation sur la console
    :param message: String, message a afficher
    :return: None
    """
    if not settings.QUIET:
        print("Error : <{}>".format(message), file=sys.stderr)


def get_ip_interface(adresse):
    """
    Donne l'objet ipaddress.IPInterface
    On remonte une SyntaxError si on ne peut pas obtenir un objet IPInterface
    :param adresse: str, IPAddress, IPInterface
    :return: IPInterface
    """
    if isinstance(adresse, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
        return adresse
    elif isinstance(adresse, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return ipaddress.ip_interface(str(adresse))
    else:
        try:
            return ipaddress.ip_interface(adresse)
        except (ValueError, TypeError):
            raise SyntaxError("get_ip_interface, {} Impossible".format(adresse))


def get_ip_ip(adresse):
    """
    Donne l'objet ipaddress.IPAdress
    On remonte une SyntaxErrot si on ne peut pas obtenir l'objet voulu
    :param adresse: str, IPAddress, IPInterface
    :return: IPAddress
    """
    if isinstance(adresse, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
        return adresse.ip
    elif isinstance(adresse, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return adresse
    else:
        try:
            return ipaddress.ip_interface(adresse).ip
        except (ValueError, TypeError):
            raise SyntaxError("get_ip_ip, {} Impossible".format(adresse))


def create_neigh(rzo, mac, ip):
    """
    Creer une nouvelle machine a partir d'une adresse MAC et d'une adresse IP, si besoin.
    Puis l'ajouter au reseau.

    1. On regarde si une machine possede deja cette adresse MAC
        1.1 On ajoute l'adresse IP a la machine (NIC.add_adresse)
                gere si l'adresse IP est deja utilisee ou pas
        1.2 On ajoute la machine au reseau (ReseauL3.add_machine)

    2. creation d'une nouvelle machine

    :param rzo: ReseauL2 ou ReseauL3, le reseau auquel il faut ajouter la machine
    :param mac: str, l'adresse physique
    :param ip: str, IPaddress, IPInterface, l'adresse IP.
    :return: None
    """
    for machine in settings.LS_MACHINES:
        nfm = machine.nic_from_mac(mac)
        if nfm:
            try:
                nfm.add_adresse(ip)
            except SyntaxError:
                error("create_neigh, IP {} invalide".format(ip))
                return
            rzo.add_machine(machine)
            return

    if isinstance(rzo, obj.ReseauL3.ReseauL3):
        ip = ip + '/{}'.format(rzo.netaddr.prefixlen)

    if mac == '00:00:00:00:00:00':
        return

    try:
        new_nic = obj.Nic.Nic(mac=mac, adresse=ip)
    except (ValueError, SyntaxError):
        error("create_neigh, Echec lors de la creation de la Nic avec {}".format(mac))
        return
    new_neigh = obj.Machine.Machine(nic=new_nic)
    rzo.add_machine(new_neigh)
    info("New neigh : {}".format(new_neigh))


def divide_list(liste, length):
    """
    Divise une liste en sous tableau d'une certaine taille.
    [1,2,3,4,5,6,7], 3 => [[1,2,3], [4,5,6], [7]]
    :param liste: list, le tableau a diviser
    :param length: int, la longueur des sous partie
    :return: list, le tableau séparé
    """
    if length <= 1:
        return [[element] for element in liste]

    result = []
    tmp = []
    for i in range(len(liste)):
        if (i % length) == 0:
            tmp = [liste[i]]
        elif (i % length) == 1:
            tmp.append(liste[i])
            result.append(tmp)
        else:
            tmp.append(liste[i])

    if len(tmp) == 1:
        result.append(tmp)

    return result


def multip_exec(process):
    """
    Execution d'une liste de processus en évitant que les coeurs des processeur soient débordés.
    :param process: list, liste de processus
    :return: None
    """
    debug("Proc : {}, Processus : {}".format(os.cpu_count(), len(process)))
    process = divide_list(process, os.cpu_count()-1)
    for subp in process:
        for p in subp:
            p.start()
        for p in subp:
            p.join()
        debug("fin de tour")


def show_result(pcadm, file=sys.stdout):
    """
    Affichage des resultats dans le stdout
    1. Informations sur la machine de l'administrateurs
    2. Nombre et liste des machines detectees avec ports ouverts
    3. Affachage des reseaux L2, appartenance et DHCP info
    4. Affichage des reseaux L3, appartenance et information d'internet
    :param pcadm: PCAdmin, Ordinateur a l'origine du scan
    :param file: Fichier de sortie
    :return: None
    """
    outstr = "\n"
    outstr += "Informations poste administrateur: \n{}\n".format(pcadm)
    for addr in pcadm.ls_online_addr():
        if addr.ls_tcp() or addr.ls_udp():
            outstr += "\t\t{} - TCP: {}, UDP: {}\n".format(str(addr.ip()), addr.ls_tcp(), addr.ls_udp())

    outstr += '\n'
    outstr += "Nombres de machine(s) detectee(s) : {}\n".format(pcadm.count - 1)
    for machine in settings.LS_MACHINES:
        if isinstance(machine, obj.PcAdmin.PcAdmin):
            continue
        outstr += "\t{}\n".format(machine.__str__())
        for addr in machine.ls_online_addr():
            if addr.ls_tcp() or addr.ls_udp():
                outstr += "\t\t{} - TCP: {}, UDP: {}\n".format(str(addr.ip()), addr.ls_tcp(), addr.ls_udp())

    outstr += '\n'
    for rzo2 in pcadm.rzo['L2']:
        nic_n = rzo2.adm_nic.nom
        if rzo2.adm_nic.etat:
            outstr += "Reseau L2 de {}:\n".format(nic_n)
            outstr += "\t{}\n".format(rzo2)

            if any(rzo2.dhcp_info.values()):
                outstr += rzo2.str_dhcp_info()
                outstr += '\n'
            else:
                outstr += "\tAucune informations DHCP\n"
                outstr += '\n'
        else:
            outstr += "Interface {} est down\n".format(nic_n)
            outstr += '\n'

    outstr += '\n'
    for rzo3 in pcadm.rzo['L3']:
        outstr += "Reseau L3 : {}\n".format(rzo3.netaddr)
        outstr += "\t{}\n".format(rzo3)

        if rzo3.gateway:
            outstr += "\tGateway : {}\n".format(str(rzo3.gateway))

        if rzo3.pubip:
            outstr += "\tPublic ip : {}, {}\n".format(rzo3.pubip, rzo3.geoloc)

        if rzo3.route:
            outstr += "\tRoute par defaut :\n"
            for hop, ip in rzo3.route.items():
                outstr += "\t\t{}: {}, {}, {}\n".format(hop,
                                                        ip,
                                                        lib.network.reverse_dns(ip),
                                                        lib.network.get_loc(ip))
    if isinstance(file, str):
        with open(file, 'w') as f:
            print(outstr, file=f)
    else:
        print(outstr, file=file)

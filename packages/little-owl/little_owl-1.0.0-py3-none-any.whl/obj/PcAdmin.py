#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : PcAdmin - Objet sous classe de machine representant la pc de l'administrateur
# Auteur : Goehry Martial
# Date : 2020/06/09
#
# Variable d'instance
#   super : _label, _nics, _desc
#   _rzo : dict, dictionnaire des reseaux L2 et L3
#           key : L2 = Liste des reseaux L2 (Adresse MAC)
#           key : L3 = Liste des reseaux L3 (Adresse IP)

# ========================================================================= #
# ===                         IMPORTATIONS                              === #
# ========================================================================= #
import ipaddress

import netifaces
from lib import tools, interfaces
from obj.Machine import Machine
from obj.Nic import Nic
import obj.ReseauL2
import obj.ReseauL3


# ========================================================================= #
# ===                         DEFINITION                                === #
# ========================================================================= #
class PcAdmin(Machine):
    """
    Sous-Class de Machine representant la machine administrateur.
    Le nombre de ses interfaces nic active donne le nombre de reseau L2.
    Le nombre de ses adresses IP donne le nombre des reseau L3
    Lors de la creation de la machine on execute automatiquement :
        - la recherche d'informations des interfaces (nombre, nom, adresses)
        - la recherche des gateways
        - la creation des reseaux L2 et L3
        - la recuperation des ports en ecoute sur la machine

    Liste des attributs:
    (super) _label: String, nom de la machine
    (super) _nics: List, liste des interfaces reseaux
    (super) _description: String, description de la machine
    _rzo : dict, Listes des reseaux {'L2': [ReseauL2, ...], 'L3': [ReseauL3, ...]}
    """
    def __init__(self):
        super().__init__(label=tools.hostname(),
                         nic=None,
                         desc="Poste administrateur")
        self._rzo = {'L2': [], 'L3': []}

        # Recuperation des informations des interfaces reseaux
        for iface in interfaces.get_ifaces():
            mac, ip4, ip6 = interfaces.get_iface_info(iface)
            self.add_nic(Nic(mac=mac, nom=iface, adresse=[ip4, ip6]))

        # Recuperation des gateway
        self.set_gateway()

        # Recuperation des ports ouverts
        self.open_ports()

    def __str__(self):
        return "<{} : {}\n\t{}>".format(self.label, self.desc, '\n\t'.join([nic.__str__() for nic in self.nics]))

    @property
    def rzo(self):
        return self._rzo

    def create_rzo(self, nic):
        """
        Cree le reseau L2 et les reseaux L3 lie a une interface nic
        On ne creer les reseaux L3 que si le PCAdmin a une de ses IP dans l'adresse du reseau
        :param nic: Nic, interface reseau servant a creer le reseau
        :return: Tuple (ReseauL2, [ReseauL3])
        """
        rzol2 = obj.ReseauL2.ReseauL2(adm_nic=nic, nom="L2 Reseau: {}".format(nic.nom), machines=self)
        rzol3 = []

        for addr in self.ls_online_addr():
            netwaddr = addr.network()
            rzo = obj.ReseauL3.ReseauL3(netaddr=netwaddr, nom="L3 Reseau: {}".format(str(netwaddr)), machines=self)
            rzol3.append(rzo)
        rzol3 = list(set(rzol3))

        return rzol2, rzol3

    def add_rzo(self, key, reseau):
        """
        Ajoute un ou plusieurs reseau dans la liste des reseaux L2 ou L3
        :param key: str, cle du dictionnaire pour ajouter le reseau dans la bonne liste
        :param reseau: ReseauL2 ou [ReseauL3,...]
        :return: None
        """
        if key not in ['L2', 'L3']:
            raise ValueError("Add_rzo - Cle {} invalide".format(key))

        if isinstance(reseau, list):
            for rzo in reseau:
                self.add_rzo(key, rzo)
            return

        if key == "L2":
            if (isinstance(reseau, obj.ReseauL2.ReseauL2)) and (reseau not in self.rzo[key]):
                self.rzo[key].append(reseau)
        else:
            if (isinstance(reseau, obj.ReseauL3.ReseauL3)) and (reseau not in self.rzo[key]):
                self.rzo[key].append(reseau)

    def add_nic(self, new_nic):
        """
        Ajoute une interface nic et les reseaux associes
        :param new_nic: Nic, Une interface reseau
        :return: None
        """
        check = super(PcAdmin, self).add_nic(new_nic)

        if check:
            rzo_l2, rzo_l3 = self.create_rzo(new_nic)
            self.add_rzo('L2', rzo_l2)
            self.add_rzo('L3', rzo_l3)

    def set_gateway(self):
        """
        Definis les gateway pour tous les reseaux L3 a partir des interfaces deja renseignees
        On ne s'occupe pas de la gateway par defaut
        :return: None
        """
        gws = netifaces.gateways()
        gateway = []
        if 'default' in gws.keys():
            del gws['default']

        for value in list(gws.values()):
            for entry in value:
                gateway.append(entry[0])

        for rzo in self.rzo['L3']:
            for adresse in gateway:
                ip = tools.get_ip_ip(adresse)
                if ip and ip in rzo.netaddr:
                    rzo.gateway = ip
                    break

    def open_ports(self):
        """
        Recupere la liste des ports ouverts et les ajoute a la bonne adresse
        :return: None
        """
        for l_con in interfaces.open_adm_ports():
            ip = l_con.laddr.ip
            port = l_con.laddr.port
            proto = l_con.type

            if ip == "0.0.0.0":
                ipv4 = ipaddress.IPv4Address
                [addr.add_port(proto, port) for addr in self.ls_online_addr() if isinstance(addr.ip(), ipv4)]
                continue
            elif ip == "::":
                ipv6 = ipaddress.IPv6Address
                [addr.add_port(proto, port) for addr in self.ls_online_addr() if isinstance(addr.ip(), ipv6)]

            else:
                addr = self.addr_from_ip(ip)
                if addr:
                    addr.add_port(proto, port)

    def contains_rzo(self, other):
        """
        Recherche un reseau a partie d'une autres instance de reseau
        :param other: Reseau, un autre reseau ou une copie
        :return: ReseauL2 | ReseauL3
        """
        if isinstance(other, obj.ReseauL2.ReseauL2):
            for rzo in self.rzo['L2']:
                if other == rzo:
                    return rzo

        elif isinstance(other, obj.ReseauL3.ReseauL3):
            for rzo in self.rzo['L3']:
                if other == rzo:
                    return rzo

        else:
            raise ValueError("Aucun reseau de ce type dans PcAdmin")

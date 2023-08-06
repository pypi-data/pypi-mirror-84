#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : ReseauL2 - Representation d'un reseau L2 via adresse MAC
# Auteur : Goehry Martial
# Date : 2020/07/10

# Variable d'instance :
#   (super) _nom, _machines
#   _adm_nic, Interface reseau du PCadmin qui en liaision sur ce reseau.
#   _dhcp_info, Dict
#       keys :
#           - bootp, adresse du serveur bootp
#           - netm, masque de sous reseau
#           - gw, default gateway
#           - dhcp, adresse serveur DHCP
#           - dns, liste des adresses DNS
#           - domain, le nom de domain
#           - client

# ========================================================================= #
# ===                       IMPORTATIONS                                === #
# ========================================================================= #
from lib import network, tools
from obj.Nic import Nic
from obj.Reseau import Reseau


# ========================================================================= #
# ===                       DEFINITION                                  === #
# ========================================================================= #
class ReseauL2(Reseau):
    """
    Classe permettant de representer les Machines en reseau.
    Elle regroupe toute les Machines ayant au moins une interface sur le meme reseau

    :param adm_nic: Nic, Interface reseau du PCadmin
    :param nom: String, nom du reseau
    :param machines: Machine list, liste des machines appartenant au reseau.
    :param dhcp_info: dict, Informations DHCP
    """
    def __init__(self, adm_nic, nom=None, machines=None, dhcp_info=None):
        if (not nom) or (not isinstance(nom, str)):
            nom = "Nouveau reseau L2"

        super(ReseauL2, self).__init__(nom=nom, machines=machines)
        self.adm_nic = adm_nic
        self.dhcp_info = dhcp_info

    def __repr__(self):
        n = "'nom': " + self.nom
        m = "'machines': [{}]".format(", ".join([machine.label for machine in self.machines]))
        return "{" + n + ', ' + m + '}'

    def __str__(self):
        return "{} <[{}]>".format(self.nom, ", ".join([m.label for m in self.machines]))

    def __hash__(self):
        return hash(self.adm_nic)

    def __eq__(self, other):
        if isinstance(other, ReseauL2):
            return self.adm_nic == other.adm_nic
        return NotImplemented

    @property
    def adm_nic(self):
        return self._adm_nic

    @adm_nic.setter
    def adm_nic(self, value):
        """
        Definit l'interface Nic du PCadmin en liaison avec ce reseau
        :param value: Nic, l'interface du PCadmin
        :return: None
        """
        if not value:
            raise SyntaxError("Setter adm_nic : Interface nic absente")

        if not isinstance(value, Nic):
            raise ValueError("Setter adm_nic : Objet Nic attendu")

        self._adm_nic = value

    @property
    def dhcp_info(self):
        return self._dhcp_info

    @dhcp_info.setter
    def dhcp_info(self, value):
        """
        Setter des informations DHCP sur le reseau L2
        :param value: list, informations issue de find_dhcp
        :return: None
        """
        self._dhcp_info = {'bootp': None,
                           'netm': None,
                           'gw': None,
                           'dhcp': None,
                           'dns': [],
                           'domain': None,
                           'client': None}

        if (not value) or (not isinstance(value, list)):
            return

        if (len(value) != 9) or (not (value[7] == self.adm_nic.mac)):
            return

        self._dhcp_info['bootp'] = value[0]
        self._dhcp_info['netm'] = value[1]
        self._dhcp_info['gw'] = value[2]
        self._dhcp_info['dhcp'] = value[3]
        self._dhcp_info['dns'] = [value[4], value[5]]
        self._dhcp_info['domain'] = value[6]
        self._dhcp_info['client'] = value[8]

    def str_dhcp_info(self):
        """
        Retourne les informations dhcp de l'interface
        :return: str
        """
        h = "DHCP info {}\n".format(self.nom)
        b = "\tAdresse serveur BOOTPC : {}\n".format(self._dhcp_info.get('bootp', 'Inconnu'))
        n = "\tMasque de sous reseau : {}\n".format(self._dhcp_info.get('netm', 'Inconnu'))
        c = "\tOffre IP : {}\n".format(self._dhcp_info.get('client', 'Inconnu'))
        g = "\tGateway : {}\n".format(self._dhcp_info.get('gw', 'Inconnu'))
        d = "\tAdresse serveur DHCP : {}\n".format(self._dhcp_info.get('dhcp', 'Inconnu'))
        s = "\tServeurs DNS : {}\n".format(self._dhcp_info.get('dns', 'Inconnu'))
        o = "\tDomaine : {}\n".format(self._dhcp_info.get('domain', 'Inconnu'))

        return h + b + n + c + g + d + s + o

    def find_dhcp(self, queue=None):
        """
        Recherche un eventuel dhcp, et ajoute les donnees recoltees
        :param queue: Queue, file d'attente pour le multi processing
        :return: None
        """
        info = network.find_dhcp(self.adm_nic.nom)
        if not queue:
            self.dhcp_info = info
        else:
            queue.put([self, info])

    def sniff(self, duration, queue=None):
        """
        Lancement du scan passif sur l'interface reseau.
        Analyse de paquets.
        Creation des voisins si necessaire
        Ajout des voisins dans le reseau
        :param duration: int, temps du scan en seconde
        :param queue: Queue, file d'attente pour le multi processing
        :return: None
        """
        paquets = network.p_scan(self.adm_nic.nom, duration)
        analyse = network.paquets_analyse(paquets)
        for key, value in analyse.items():
            for ip in value:
                if not queue:
                    tools.create_neigh(rzo=self, mac=key, ip=ip)
                else:
                    queue.put([self, key, ip])

    def to_json(self, key):
        """
        Prepare l'exportation en JSON
        :param: list, cle des machines membres (cd jsondata.export_json)
        :return: dict, format pour l'exportation en JSON
        """
        rzo = super(ReseauL2, self).to_json(key)
        rzo['adm_mac'] = self.adm_nic.mac
        rzo['dhcp_info'] = {
            'bootp': self._dhcp_info['bootp'],
            'netm': self._dhcp_info['netm'],
            'gw': self._dhcp_info['gw'],
            'dhcp': self._dhcp_info['dhcp'],
            'dns': self._dhcp_info['dns'],
            'domain': self._dhcp_info['domain'],
            'client': self._dhcp_info['client']
        }
        return rzo

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : Machine - Objet representant les machines les Machines
# Auteur : Goehry Martial
# Date : 2020/06/05
#
# Variables d'instance :
#   _label : str, Nom de la machine
#   _nics : list, liste des interfaces Nic.Nic de la machine
#   _desc : str, description de la machine

# Variable de classe :
#   count : int, comptabilise le nombre de machine creees

# ========================================================================= #
# ===                         IMPORTATIONS                              === #
# ========================================================================= #
from lib import network
from obj.Nic import Nic
import data.settings as settings
import lib.tools as tools


# ========================================================================= #
# ===                           DEFINITION                              === #
# ========================================================================= #
class Machine:
    """
    Classe representant les machines disponibles sur le reseau

    Liste des attributs :
    :param label: String,  nom de la machine
    :param nic: Nic, interface de connexion
            nics[] : liste des interfaces reseau d'une machine
    :param desc: description de la machine
    """
    count = 0

    def __init__(self, label='Machine{}', nic=None, desc=""):
        self.label = label.format(Machine.count)
        self.nics = nic
        self.desc = desc

        if self in settings.LS_MACHINES:
            raise Exception("Machine deja existante")
        settings.LS_MACHINES.append(self)

        Machine.count += 1

    def __repr__(self):
        """
        Representation d'une machine
        :return: Dictionnaire
        """
        l = "'label': {}".format(self.label)
        n = "'nics': [{}]".format(", ".join([nic.nom for nic in self.nics]))
        return "{" + l + ', ' + n + '}'

    def __str__(self):
        """
        Methode d'affichage
        :return: String
        """
        return "<{} : {}>".format(self.label, ', '.join([nic.__str__() for nic in self.nics]))

    def __eq__(self, other):
        """
        Gere la condition d'egalite entre 2 Machines
        :param other: Machine, une autre instance de Machine
        :return: Bool
        """
        if isinstance(other, Machine):
            return hash(self) == hash(other)
        return NotImplemented

    def __hash__(self):
        """
        Rendre la machine hashable pour etre utiliser comme cle et etre comparee
        :return: Int, le hash de l'objet
        """
        return hash(str([hash(nic) for nic in self.nics]))

    @property
    def label(self):
        """
        Getter label (nom) de la machine
        :return: String
        """
        return self._label

    @label.setter
    def label(self, value):
        """
        Changement du label de la machine.
        La nouvelle valeur doit etre de type string.
        :param value: String, le nouveau label
        :return: None
        """
        if (not value) or (not isinstance(value, str)):
            self._label = "Machine"
        else:
            self._label = value

    @property
    def nics(self):
        return self._nics

    @nics.setter
    def nics(self, value):
        """
        Reinitialise les interfaces reseaux d'une machine
        :param value: Nic, list, interface ou une liste d'interface
        :return: None
        """
        self._nics = []
        if not value:
            return
        if isinstance(value, list):
            for nic in value:
                self.add_nic(nic)
        else:
            self.add_nic(value)

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        """
        Modifie la description de la machine
        :param value: String, Nouvelle description
        :return: None
        """
        if (not value) or (not isinstance(value, str)):
            self._desc = ""
        else:
            self._desc = value

    def add_nic(self, new_nic):
        """
        Ajoute une interface reseau.
        Controle si l'interface n'est pas deja dans la liste des interface de cette machine.
        Controle de la collision d'adresse IP. Deux interfaces reseau ne doivent pas avoir la meme adresse
        :param new_nic: Nic, la nouvelle interface
        :return: Bool, True si l'interface a ete ajoutee. (utilise par PCAdmin)
        """
        if not isinstance(new_nic, Nic):
            tools.error("add_nic: Impossible d'ajouter {} aux interfaces de {}".format(new_nic, self.label))
            return False

        if new_nic in self.nics:
            tools.debug("add_nic: '{}' deja presente sur '{}'".format(new_nic, self.label))
            return False

        for new_ip in new_nic.ls_online_ip():
            if new_ip in self.ls_online_ip():
                tools.debug("add_nic: {} deja utilise par une autre interface".format(new_ip))
                return False

        self.nics.append(new_nic)
        return True

    def remove_nic(self, nic):
        """
        Supprime une interface reseau a la machine
        :param nic: Nic, une interface reseau
        :return: None
        """
        if nic in self.nics:
            self.nics.remove(nic)

    def nic_from_ip(self, ip):
        """
        Regarde si une adresse IP n'est pas deja utilisee par la machine (Adresse online)
        :param ip: str, IPAddress, IPInterface, l'adresse a controler
        :return: Nic ou None
        """
        for nic in self.nics:
            if ip in nic:
                return nic
        return None

    def nic_from_mac(self, mac):
        """
        Regarde si une adresse Mac est utilisee par cette machine.
        :param mac: str, une adresse mac
        :return: Nic ou None
        """
        for nic in self.nics:
            if mac == nic.mac:
                return nic
        return None

    def addr_from_ip(self, ip):
        """
        Regarde si une adresse IP est utilisee par cette machine
        :param ip: str, l'adresse IP
        :return: Adresse, l'objet Adresse relie a l'adresse IP
        """
        for addr in self.ls_online_addr():
            if ip == str(addr.ip()):
                return addr
        return None

    def ls_all_ip(self):
        """
        Liste toutes les adresses IP ipaddress.IPAddress
        Mise a plat de la liste source : http://sametmax.com/applatir-un-iterable-like-a-boss-en-python/
        :return: list, liste de toutes les IP de la machines, IPAddress
        """
        ls = [nic.ls_all_ip() for nic in self.nics]
        return [y for x in ls for y in x]

    def ls_online_ip(self):
        """
        :return: list, liste des toutes les IP en ligne de la machine
        """
        ls = [nic.ls_online_ip() for nic in self.nics]
        return [y for x in ls for y in x]

    def ls_all_mac(self):
        """
        :return: list, liste de toutes les adresses physique de la machine
        """
        return [nic.mac for nic in self.nics]

    def ls_all_addr(self):
        """
        :return: list, liste des objets Adresse
        """
        ls = [nic.adresses for nic in self.nics]
        return [y for x in ls for y in x]

    def ls_online_addr(self):
        """
        :return: list, liste des objets Adresse en ligne
        """
        ls = [nic.ls_online_addr() for nic in self.nics]
        return [y for x in ls for y in x]

    def host_scan(self, queue=None):
        """
        Scan une machine a la recherche de ports TCP/UDP ouverts
        On ne s'interesse qu'aux adresses locale
        :param queue: Queue, file d'attente pour le multiprocessing
        :return: None
        """
        for adresse in [addr for addr in self.ls_online_addr() if addr.ip().is_private]:
            tcp_opn, udp_opn = network.host_scan(target=str(adresse.ip()),
                                                 tcp_ports=settings.TCP_PORTS,
                                                 udp_ports=settings.UDP_PORTS)
            if not queue:
                adresse.l_port = [tcp_opn, udp_opn]
            else:
                queue.put([self, adresse, tcp_opn, udp_opn])

    def to_json(self):
        """
        Prepare l'exportation en JSON
        :return: dict, format pour l'exportation en JSON
        """
        machine_json = {
            'label': self.label,
            'nics': [nic.to_json() for nic in self.nics],
            'desc': self.desc
        }
        return machine_json

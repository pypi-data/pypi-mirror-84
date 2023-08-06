#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : ReseauL3 - Representation d'un reseau L3 via IP4 ou IP6
# Auteur : Goehry Martial
# Date : 2020/07/10

# Variables d'instance :
#   (super) _nom, _machines
#   _netaddr : ipaddress.IPNetwork, adresse IP du reseau
#   _gateway : ipaddress.IPaddress, adresse IP de la gateway du reseau.
#   _pubip: ipaddress.IPaddress adresse public pour le reseau
#   _geoloc : str, adresse geographique de l'adresse IP public
#   _route: list, [(ipaddressIPaddress, str(reverse DNS)), ...]

# ========================================================================= #
# ===                          IMPORTATIONS                             === #
# ========================================================================= #
import ipaddress
import socket

from lib import tools, network
import obj.PcAdmin
from obj.Reseau import Reseau


# ========================================================================= #
# ===                           DEFINITION                              === #
# ========================================================================= #
class ReseauL3(Reseau):
    """
    Classe permettant de representer les Machines en reseau L3 IP.
    Elle regroupe les machines ayant une adresse IP dans le reseau.

    :param netaddr : ipadress.IPv4Network, IPv6Network, l'adresse du reseau IP
    :param nom : str, nom du reseau
    :param machines: Machine list, liste des machines appartenant au reseau.
    :param gateway : IPAddress, adresse de la gateway pour ce reseau
    :param pubip : str, IPAddress, IPInterface, adresse publique du reseau
    :param geoloc : str, geolocalisation de l'adresse ip
    :param route : dict, route par defaut
    :return None
    """
    def __init__(self, netaddr, nom=None, machines=None, gateway=None, pubip=None, geoloc=None, route=None):
        if (not nom) or (not isinstance(nom, str)):
            nom = "Nouveau reseau L3"

        super().__init__(nom=nom)
        self.netaddr = netaddr
        self.machines = machines
        self.gateway = gateway
        self.pubip = pubip
        self.geoloc = geoloc
        self.route = route

    def __repr__(self):
        n = "'nom': " + self.nom
        a = "'netaddr': " + self.netaddr.with_prefixlen
        g = "'gateway': " + str(self.gateway)
        m = "'machines': [{}]".format(", ".join([machine.label for machine in self.machines]))
        return "{" + n + ', ' + a + ', ' + g + ', ' + m + '}'

    def __str__(self):
        return "{} <{} [{}]>".format(self.nom, self.netaddr, ", ".join([m.label for m in self.machines]))

    def __hash__(self):
        return hash(self.netaddr)

    def __eq__(self, other):
        if isinstance(other, ReseauL3):
            return self.netaddr == other.netaddr
        return NotImplemented

    @property
    def machines(self):
        return self._machines

    @machines.setter
    def machines(self, value):
        """
        Setter des machines pour le reseau L3
        :param value: List, Machine, definition des machines du reseau
        :return: None
        """
        self._machines = []
        if not value:
            return

        if isinstance(value, list):
            for machine in value:
                self.add_machine(machine)
        else:
            self.add_machine(value)

    @property
    def netaddr(self):
        return self._netaddr

    @netaddr.setter
    def netaddr(self, value):
        """
        Modifier l'adresse du reseau,
        :param value: IPv4Network, IPv6Network
        :return: None
        """
        if isinstance(value, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            self._netaddr = value
        elif isinstance(value, str):
            try:
                self._netaddr = ipaddress.ip_network(value)
            except ValueError:
                raise ValueError("Reseau : '{}' adresse de reseau invalide.".format(value))
        else:
            raise ValueError("Reseau : '{}' adresse de reseau invalide.".format(value))

    @property
    def gateway(self):
        return self._gateway

    @gateway.setter
    def gateway(self, value):
        """
        Setter de la gateway.
        :param value: str, IPAddress, IPInterface
        :return: None
        """
        try:
            gw = tools.get_ip_ip(value)
        except SyntaxError:
            gw = None

        if not gw:
            self._gateway = gw
        else:
            self._gateway = gw if gw in self.netaddr else None

    @property
    def pubip(self):
        return self._pubip

    @pubip.setter
    def pubip(self, ip):
        """
        Setter de l'adresse IP public du reseau
        :param ip: str, IPAddress, IPInterface
        :return: None
        """

        try:
            self._pubip = tools.get_ip_ip(ip)
        except SyntaxError:
            self._pubip = None

    @property
    def geoloc(self):
        return self._geoloc

    @geoloc.setter
    def geoloc(self, loc):
        """
        Setter de la localisation de l'adresse IP
        :param loc: str, la geolocalisation de l'adresse IP publique
        :return: None
        """
        self._geoloc = None
        if not loc:
            return
        if isinstance(loc, str):
            self._geoloc = loc

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, rte):
        """
        Setter de la route par defaut
        :param rte: dict, route par defaut {key = nombre de saut, value = adresse IP}
        :return:
        """
        self._route = None
        if not rte:
            return

        if isinstance(rte, dict):
            self._route = rte

    def add_machine(self, machine):
        """
        Ajoute une machine au reseau.
        1. Si c'est bien une machine.       gere par super
        2. Si elle n'est pas deja presente  gere par super
        3. Si au moins une de ses adresses IP entre dans le range IP

        Si ses adresses IP ne entre en collision les adresses IP deja presente, on remonte un warnings
        :param machine: Machine, la machine a ajouter
        :return: None
        """
        if not super(ReseauL3, self).check_machine(machine):
            return

        if not [True for ip in machine.ls_online_ip() if ip in self.netaddr]:
            tools.debug("RZO_L3 add_machine : Aucune adresse n'entre dans le reseau")
            return

        if [True for ip in machine.ls_online_ip() if ip in self.ls_online_ip()]:
            tools.debug("RZO_L3 add_machine : Collision detectee")    # Inutile peut etre

        self.machines.append(machine)

    def ls_online_ip(self):
        """
        :return: list, donne la liste des adresses IP utilisee dans le reseau (online)
        """
        ls = []
        for machine in self.machines:
            for ip in machine.ls_all_ip():
                if ip in self.netaddr:
                    ls.append(ip)
        return ls

    def internet_info(self, queue=None):
        """
        Recupere les informations disponibles sur internet.
        Recuperation de l'adresse ip public
        Recuperation de la route par defaut
        Utilisation de la premiere adresse IP de PcAdmin qui est dans le reseau
        :param queue, Queue, file d'attente pour le multiprocessing
        :return: None
        """
        src = None
        for machine in self.machines:
            if isinstance(machine, obj.PcAdmin.PcAdmin):
                for addr in machine.ls_online_addr():
                    if addr.ip() in self.netaddr:
                        src = str(addr.ip())
                        break
        if not src:
            return

        try:
            pubip, geoloc = network.get_public_ip(src)
            route = network.get_route(src)
        except socket.gaierror:
            return

        if not queue:
            self.pubip = pubip
            self.geoloc = geoloc
            self.route = route
        else:
            queue.put([self, pubip, geoloc, route])

    def to_json(self, key):
        """
        Prepare l'exportation en JSON
        :param key: list, cle des machines membres (cd jsondata.export_json)
        :return: dict, format pour l'exportation en JSON
        """
        rzo = super(ReseauL3, self).to_json(key)
        rzo['netaddr'] = self.netaddr.with_prefixlen
        rzo['gateway'] = self.gateway.__str__()
        rzo['pubip'] = self.pubip.__str__()
        rzo['geoloc'] = self.geoloc
        rzo['route'] = self.route

        return rzo


if __name__ == '__main__':
    pass

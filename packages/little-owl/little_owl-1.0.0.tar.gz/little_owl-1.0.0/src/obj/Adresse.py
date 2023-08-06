#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : Adresse - Adresse de contact d'une interface
# Auteur : Goehry Martial
# Date : 2020/07/27
# Version : 1.0
#
# Variables d'instance :
#   _adresse : IPInterface (IPv4 ou IPv6)
#   _etat: bool, True si accessible, False sinon
#   _type: AF_INET ou AF_INET6 : type de l'adresse IP
#   _l_ports : dict, Liste des ports ouverts,
#       key: SOCK_STREAM (TCP), SOCK_DGRAM (UDP)
#       value: list d'entier


# ========================================================================= #
# ===                           IMPORTATIONS                            === #
# ========================================================================= #
import ipaddress
from socket import AF_INET, AF_INET6, SOCK_STREAM, SOCK_DGRAM
import lib.tools as tools


# ========================================================================= #
# ===                            DEFINITION                             === #
# ========================================================================= #
class Adresse:
    """
    Classe representant une adresse de contact d'une interface
    :param adresse: str, IPAddress, IPInterface - l'adresse IP
    :param etat: bool, True si l'adresse est utilisee par une interface actuellement
    :param l_port: list, l_port[0] liste ports TCP, l_port[1] liste ports UDP

    autres attributs d'instances:
    type : int, type d'adresse AF_INET (IPV4) ou AF_INET6 (IPV6)
    l_port : dict, key = int( SOCK_STREAM|DGRAM), value: list d'entier
    """

    def __init__(self, adresse, etat=True, l_port=None):
        self.adresse = adresse
        self.etat = etat
        self.l_port = l_port

    def __repr__(self):
        """
        Representation d'une adresse
        :return: dictionnaire
        """
        a = "adresse: {}, ".format(self.with_prefixlen())
        e = "etat: {}, ".format(('hors ligne', 'en ligne')[self.etat])
        t = "tcp: {}, ".format(self.l_port[SOCK_STREAM])
        u = "udp: {}".format(self.l_port[SOCK_DGRAM])
        return '{' + a + e + t + u + '}'

    def __str__(self):
        """
        Methode d'affichage
        :return: String
        """
        return "Adresse<{} - {}>".format(self.with_prefixlen(), ('hors ligne', 'en ligne')[self.etat])

    def __eq__(self, other):
        """
        Gere la condition d'egalite.
        On regarde l'adresse IP
        :param other: Adresse, une autre Adresse
        :return: Bool
        """
        if isinstance(other, Adresse):
            return self.ip() == other.ip()
        return NotImplemented

    def __hash__(self):
        """
        Fonction de hashage pour une interface reseau
        :return: Int, le hash de l'interface
        """
        return hash(self.adresse)

    @property
    def adresse(self):
        return self._adresse

    @adresse.setter
    def adresse(self, value):
        """
        Setter d'une adresse IP
        On en profite pour initialiser le type
        Adresse IP prise en compte:
            - IPv4
            - IPv6
        :param value: str,IPAddress,IPInterface
        :return: None
        """
        self._adresse = tools.get_ip_interface(value)
        self._type = AF_INET if isinstance(self.adresse, ipaddress.IPv4Interface) else AF_INET6

    @property
    def etat(self):
        return self._etat

    @etat.setter
    def etat(self, value):
        """
        Setter de l'etat d'utilisation de l'adresse IP
        True si elle est utilisee
        False si elle ne l'est pas
        :param value: bool,
        :return: None
        """
        if isinstance(value, bool):
            self._etat = value
        else:
            tools.error("Adresse etat: Invalide, bool attendu")
            self._etat = False

    @property
    def type(self):
        return self._type

    @property
    def l_port(self):
        return self._l_port

    @l_port.setter
    def l_port(self, value):
        """
        Setter des ports en ecoutes
        :param value: list, [0] : Port TCP, [1] Ports UDP
        :return: None
        """
        self._l_port = {SOCK_STREAM: [], SOCK_DGRAM: []}
        if not value:
            return

        if isinstance(value, list) and (len(value) == 2):
            self.add_port(SOCK_STREAM, value[0])
            self.add_port(SOCK_DGRAM, value[1])
        else:
            tools.error("Setter Adresse l_ports : {} Invalide".format(value))

    def add_port(self, t_sock, valeur):
        """
        Ajoute un ou plusieurs port dans la bonne liste
        :param t_sock: int, SOCK_STREAM or SOCK_DGRAM
        :param valeur: int ou list
        :return: None
        """
        if t_sock not in [SOCK_STREAM, SOCK_DGRAM]:
            tools.error("Adresse add_l_port : {} type invalide".format(t_sock))
            return

        lp = self.l_port[t_sock]

        if isinstance(valeur, list):
            for val in valeur:
                self.add_port(t_sock, val)
        elif isinstance(valeur, int):
            if valeur not in lp:
                lp.append(valeur)
                lp.sort()
        else:
            tools.error("Adresse add_l_port : {} port invalide".format(valeur))
            return

    def ip(self):
        """
        :return: IPAdress, l'adresse IP sans le netmask
        """
        return self.adresse.ip

    def network(self):
        """
        :return: IPNetwork, retourne l'adresse reseau auquel l'adresse appartient
        """
        return self.adresse.network

    def with_prefixlen(self):
        """
        :return: str, adresse avec le prefix reseaux
        """
        return self.adresse.with_prefixlen

    def ls_tcp(self):
        """
        :return: list, liste des ports tcp
        """
        return self.l_port[SOCK_STREAM]

    def ls_udp(self):
        """
        :return: list, liste des ports udp
        """
        return self.l_port[SOCK_DGRAM]

    def to_json(self):
        """
        Prepare pour l'exportation en JSON
        :return: dict, format pour l'exportation en JSON
        """
        adr_json = {
            'adresse': self.with_prefixlen(),
            'etat': self.etat,
            'port': {
                'TCP': self.l_port[SOCK_STREAM],
                'UDP': self.l_port[SOCK_DGRAM]
            }
        }
        return adr_json

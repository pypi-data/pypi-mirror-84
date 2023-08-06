#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : Nic -  Definition de l'objet representant les interfaces reseaux
# Auteur : Goehry Martial
# Date : 2020/07/27
#
# Variables d'instance :
#   _mac : str, adresse mac, identifiant unique d'une interface reseau
#   _nom : str, nom de l'interface si disponible
#   _adresses : list, liste des adresses valide pour cette interface
#   _marque : str, nom de constructeur
#   _etat: bool, True si l'interface est UP


# ========================================================================= #
# ===                          IMPORTATIONS                             === #
# ========================================================================= #
from obj.Adresse import Adresse
import lib.interfaces as interfaces
import data.settings as settings
import lib.tools as tools


# ========================================================================= #
# ===                           DEFINITION                              === #
# ========================================================================= #
class Nic:
    """
    Classe representant les interfaces reseaux d'une machine
    :param mac: str, adresse mac
    :param nom: str, nom de l'interface, si disponible
    :param adresse: list, str, IPAddress, IPInterface, adresses a associer a cette interface
    :param etat: bool, donne l'etat UP ou DOWN de l'interface

    autres attributs d'instance
    marque: str, constructeur de l'interface

    """
    def __init__(self, mac, nom="nic", adresse=None, etat=None):
        self._marque = ""
        self.mac = mac
        self.nom = nom
        self.adresses = adresse
        self.etat = etat

    def __repr__(self):
        """
        Representation d'une nic
        :return: str
        """
        n = "nom: {}, ".format(self.nom)
        m = "mac: {}, ".format(self.mac)
        v = "marque: {}, ".format(self.marque)
        a = "adresses : {}".format([a.with_prefixlen() for a in self.adresses])
        return '{' + n + m + v + a + '}'

    def __str__(self):
        """
        Methode d'affichage
        :return: str
        """
        return "{} - {} - {} - {}".format(self.nom,
                                          self.mac,
                                          self.marque,
                                          [a.with_prefixlen() for a in self.ls_online_addr()])

    def __eq__(self, other):
        """
        Gere la condition d'egalite, une Nic se definie par son adresse MAC
        :param other: Nic, une autre interface reseaux
        :return: Bool
        """
        if isinstance(other, Nic):
            return self.mac == other.mac
        return NotImplemented

    def __hash__(self):
        """
        Fonction de hashage pour une interface reseau
        :return: Int, le hash de l'interface
        """
        return hash(self.mac)

    def __contains__(self, item):
        """
        Regarde si une adresse est dans la liste des adresses ip
        :param item: str, IPAddress, IP, Adresse
        :return: bool, vrai si l'adresse est utilisee par l'interface
        """
        if isinstance(item, Adresse):
            return item in self.adresses
        try:
            ip = tools.get_ip_ip(item)
        except SyntaxError:
            return False
        return ip in self.ls_all_ip()

    @property
    def mac(self):
        """
        Getter de l'adresse MAC
        :return: str, l'adresse MAC de l'interface
        """
        return self._mac

    @mac.setter
    def mac(self, value):
        """
        Setter de l'adresse MAC. L'utilisation de "re" permet de controler que la valeur est une adresse mac correct.
        En cas d'erreur une erreur de syntaxe est levee.
        ValueError est levee si value n'est pas un str.
        La marque est egalement modifiee ici.
        :param value: str, l'adresse MAC.
        :return: None
        """
        if not isinstance(value, str):
            raise ValueError("Adresse physique doit etre en string")

        if interfaces.is_mac(value):
            self._mac = value
            self.marque = value
        else:
            raise SyntaxError("Adresse physique invalide : '{}'".format(value))

    @property
    def nom(self):
        """
        Getter du nom de l'interface
        :return: str, le nom de l'interface
        """
        return self._nom

    @nom.setter
    def nom(self, value):
        """
        Setter du nom de l'interface.
        Si la value n'est pas un str, on definit _nom a ""
        :param value: str, le nom de l'interface
        :return: None
        """
        if isinstance(value, str):
            self._nom = value
        else:
            self._nom = ""
            tools.debug("Setter nom : {} Invalide".format(value))

    @property
    def marque(self):
        """
        Getter de la compagnie qui a tres probablement construit l'interface
        :return: str, "Entreprise, Pays"
        """
        return self._marque

    @marque.setter
    def marque(self, value):
        """
        Setter de la marque, Il suffit de donner l'adresse MAC pour obtenir le constructeur.
        Pour plus d'information cf lib.interfaces.py.import_mac_db
        :param value: str, l'adresse mac de l'interface
        :return: None
        """
        data = interfaces.import_mac_db(settings.PATH_TO_MAC_DB)
        if not data:
            self._marque = 'Non reneigne'
        else:
            self._marque = interfaces.get_mac_vendor(value, data)

    @property
    def adresses(self):
        return self._adresses

    @adresses.setter
    def adresses(self, value):
        """
        Setter des adresses de l'interface
        :param value: list, str, IpAddress, IPInterface, Adresse
        :return: None
        """
        self._adresses = []
        if not value:
            return

        if isinstance(value, list):
            for val in value:
                self.add_adresse(val)
        else:
            self.add_adresse(value)

    @property
    def etat(self):
        return self._etat

    @etat.setter
    def etat(self, value):
        """
        Setter de l'etat de l'interface UP(True) ou DOWN (False)
        :param value: bool, ou None
        :return: None
        """
        if self.nom == 'nic':
            self._etat = True
        else:
            self._etat = interfaces.is_up(self.nom) if value is None else value

    def add_adresse(self, value):
        """
        Ajoute une Adresse au reseau.
        Si ce n'est pas un objet Adresse, il faut le creer
        Si la nouvelle adresse existe deja
        :param value : list, Adresse, IPAddress, IPInterface, str
        :return: None
        """
        if not value:
            return

        if isinstance(value, list):
            for val in value:
                self.add_adresse(val)
            return

        if isinstance(value, Adresse):
            new_addr = value
        else:
            try:
                new_addr = Adresse(adresse=value)
            except SyntaxError:
                tools.error("add_adresse : Echec de l'ajout {}".format(value))
                return

        if new_addr not in self:
            self._adresses.append(new_addr)

    def ls_all_ip(self):
        """
        :return: list, liste de toutes les IP de l'interface format IPAddress
        """
        return [a.ip() for a in self.adresses]

    def ls_online_ip(self):
        """
        :return: list, liste de toutes les adresse IP avec le statut en ligne, format IPAddress
        """
        return [a.ip() for a in self.adresses if a.etat]

    def ls_online_addr(self):
        """
        :return: list, la liste de toutes les adresses en ligne, objet Adresse
        """
        return [a for a in self.adresses if a.etat]

    def to_json(self):
        """
        Prepare l'exportation en JSON
        :return: dict, format pour l'exportation en JSON
        """
        nic_json = {
            'mac': self.mac,
            'nom': self.nom,
            'adresses': [adr.to_json() for adr in self.adresses],
            'etat': self.etat
        }
        return nic_json

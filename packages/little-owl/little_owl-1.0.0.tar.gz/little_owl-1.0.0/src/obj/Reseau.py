#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : Reseau - Classe abstraite permettant la representation des reseaux
# Auteur : Goehry Martial
# Date : 2020/07/10

# Variable d'instance :
#   _nom : str, nom du reseau
#   _machines : list, liste des machines appartenant au reseau

# ========================================================================= #
# ===                          IMPORTATIONS                             === #
# ========================================================================= #
import lib.tools as tools
from obj.Machine import Machine
from obj.Nic import Nic


# ========================================================================= #
# ===                          DEFINITION                               === #
# ========================================================================= #
class Reseau:
    """
    Classe abstraite representant des machines en reseau
    :param nom: String, nom du reseau
    :param machines : Machine list, liste des machines appartenant au reseau.
    """
    def __init__(self, nom=None, machines=None):
        self.nom = nom
        self.machines = machines

    def __repr__(self):
        n = "'nom': " + self.nom
        m = "'machines': [{}]".format(", ".join([machine.label for machine in self.machines]))
        return "{" + n + ', ' + m + '}'

    def __str__(self):
        return "Reseau({})<[{}]>".format(self.nom, ", ".join([m.label for m in self.machines]))

    def __contains__(self, item):
        if not isinstance(item, Machine):
            return False

        if not self._machines:
            return False

        return item in self._machines

    def __len__(self):
        return len(self.machines)

    @property
    def machines(self):
        return self._machines

    @machines.setter
    def machines(self, value):
        """
        Modifier completement la liste des machines du reseau
        :param value: List | Machines, Une ou plusieurs machine a ajouter au reseau
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
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if not value:
            self._nom = "Reseau indefini"
        elif isinstance(value, str):
            self._nom = value
        else:
            self._nom = "Reseau indefini"
            tools.debug("setter nom : {} invalide pour nom de reseau".format(self.nom))

    def check_machine(self, machine):
        """
        Controle une machine avant l'ajout
        1. machine est de type Machine
        2. machine ne doit pas etre deja presente
        :param machine: Machine, La nouvelle machine a ajouter
        :return: Bool, False si l'une des deux condition n'est pas respectee, True si on peut ajouter machine
        """
        if isinstance(machine, Machine) and (machine not in self):
            return True
        return False

    def check_mac(self, mac):
        """
        Controle si une adresse mac est deja utilisee par une machine du reseau
        :param mac: str, l'adresse mac
        :return: Bool, vrai si l'adresse est deja utilisee par une machine
        """
        if isinstance(mac, str):
            for machine in self.machines:
                if machine.nic_from_mac(mac):
                    return True
        return False

    def add_machine(self, machine):
        """
        Ajoute une machine au reseau
        :param machine: Machine, La machine a ajouter au reseau
        :return: None
        """
        if self.check_machine(machine):
            self.machines.append(machine)

    def machine_from_nic(self, nic):
        """
        Retourne une machine dans une reseau qui possede une interface nic
        :param nic: Nic, l'interface reseau
        :return: Machine, la machine si elle est dans le reseau
        """
        if not isinstance(nic, Nic):
            tools.error("machine_form_nic : Interface reseau invalide")
            return None

        for machine in self.machines:
            if machine.nic_from_mac(nic.mac):
                return machine

        return None

    def remove(self, machine):
        """
        Retire une machine du reseau.
        :param machine: Machine, la machine qui doit etre retiree
        :return: none
        """
        if machine in self:
            self.machines.remove(machine)

    def to_json(self, keys):
        """
        Prepare l'exportation en JSON
        :param: list, cle des machines membres (cd jsondata.export_json)
        :return: dict, format pour l'exportation en JSON
        """
        rzo_json = {
            "nom": self.nom,
            "machines": keys
        }

        return rzo_json

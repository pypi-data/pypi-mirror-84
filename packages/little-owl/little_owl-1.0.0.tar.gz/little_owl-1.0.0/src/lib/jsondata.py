#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Explication des champs JSON
# 2 key :
#   - machines
#   - reseaux
#
# machines : {key(int): machine_json(obj.Machine ou obj.PcAdmin en json)}
# machine_json:
#   desc: str, description
#   label: str, nom de la machine
#   nics: list(nics_json)
#   Si machine est PcAdmin:
#       rzo: list(int) liste des reseaux associe a la machine
#
# nics_json:
#   adresses: list(adresse_json)
#   etat: bool, True si l'interfaces est up
#   mac: str, adresse MAC
#   nom: str, nom de l'interface
#
# adresse_json:
#   adresse: str, IP/CIDR
#   etat: bool, True si l'adresse est utilisee
#   port: dict, {'TCP': list(int), 'UDP': list(int)} Port en eoute sur cette adresse
#
# reseaux: {key(int): reseau_json(ReseauL2 ou ReseauL3 en json)}
# reseau_json:
#   (L2)
#   adm_mac: str, adresse MAC
#   dhcp_info: dict, (bootp, client, dhcp, dns, domain, gw, netm)
#   machines: list, key des machines appartenant au reseau
#   nom: str, nom du reseau
#
#   (L3)
#   gateway: str, IP de la gateway
#   geoloc: str, resultat de la geolocalisation
#   machines: list, key des machines appartenant au reseau
#   netaddr: IP/CIDR du reseau
#   nom: str, nom du reseau
#   pubip: str, Adresse IP public
#   route: dict, {key(int) numero du saut: value(str) IP}
"""


# ========================================================================= #
# ===                          IMPORTATIONS                             === #
# ========================================================================= #
import json
import os.path
import data.settings as settings
from lib import tools
from obj.Adresse import Adresse
from obj.Machine import Machine
from obj.Nic import Nic
from obj.PcAdmin import PcAdmin


# ========================================================================= #
# ===                           FONCTIONS                               === #
# ========================================================================= #
from obj.ReseauL2 import ReseauL2
from obj.ReseauL3 import ReseauL3


def export_json(pca, file=None):
    """
    Exportation des donnees du programme json dans un fichier
    1. Liste des machines
    2. Liste des reseaux L2 et L3
        Dans chaque reseau on ajoute les cles des machines associees
    3. Dans la machine PcAdmin on ajoute la liste des cle reseaux
    :param pca: PcAdmin, l'ordinateur source de l'analyse
    :param file: str, le nom du fichier pour l'exportation
    :return: None
    """
    d_machines = {key: machine for key, machine in enumerate(settings.LS_MACHINES)}
    d_rzo = {key: rzo for key, rzo in enumerate(pca.rzo['L2'] + pca.rzo['L3'])}

    json_rzo = dict()
    for key, rzo in d_rzo.items():
        m_key = [k for k, m in d_machines.items() if m in rzo]
        json_rzo[key] = rzo.to_json(m_key)

    json_machines = dict()
    for key, machine in d_machines.items():
        json_machines[key] = machine.to_json()
        if machine is pca:
            json_machines[key]['rzo'] = list(d_rzo.keys())

    data = {'machines': json_machines, 'reseaux': json_rzo}

    if not file:
        file = "lo_scan.json"
    c = 0
    while os.path.exists(file):
        file = "lo_scan.{}.json".format(c)
        c += 1

    with open(file, 'w') as jsonfile:
        json.dump(data, jsonfile)


def import_json(file):
    """
    Importation des donnees a partir d'un fichier json
    1. Ouverture du fichier
    2. Recuperation des donnees Json, controle des deux labels
    3. Separation des donnees, machines et reseaux
    4. Importation des machines, point particulier  pour le PcAdmin
    5. Importation des donnees reseaux
    :param file: str, le chemin vers le fichier json avec les donnees
    :return: PcAdmin
    """
    try:
        with open(file, 'r') as f:
            data = f.read()
            if not data:
                tools.info("Aucunes donnees dans {}".format_map(file))
                exit(0)
    except FileNotFoundError:
        tools.error("Importation: {} non trouve".format(file))
        exit(1)
    except PermissionError:
        tools.error("Importation: {} lecture non autorisee".format(file))
        exit(1)

    data = json.loads(data)
    if ('machines' not in data) or ('reseaux' not in data):
        tools.error("Importation: format de donnees invalide")
        exit(1)

    json_machines = data['machines']
    json_reseau = data['reseaux']
    d_machine = dict()

    # Importation des machines
    pca = None
    for key, data_machine in json_machines.items():
        if 'rzo' in data_machine:
            pca = import_pcadmin(data_machine)
            d_machine[key] = pca
        else:
            machine = import_machine(data_machine)
            d_machine[key] = machine

    if not pca:
        tools.error("Importation: creation du PcAdmin non realisee")
        exit(1)

    for key, data_rzo in json_reseau.items():
        import_rzo(data=data_rzo, pca=pca, d_machine=d_machine)

    return pca


def import_pcadmin(data):
    """
    Importation d'une machine PcAdmin a partir des informations au format json.
    L'objet PcAdmin recupere plusieurs type de donnees automatiquement a la creation.
    On ecrase les donnees initiales.
    :param data: dict, les donnees du pcadmin
    :return: PcAdmin
    """
    try:
        pca = PcAdmin()
        pca._label = data['label']
        pca._nics = import_nics(data=data['nics'])
        pca._desc = data['desc']
        pca._rzo = {'L2': [], 'L3': []}
        return pca
    except KeyError:
        tools.error('Importation, pcadmin KeyError')
        exit(1)


def import_machine(data):
    """
    Importation d'une machine a partir des information JSON
    :param data: les donnees de la machine
    :return: Machine
    """
    try:
        machine = Machine(label=data['label'],
                          nic=import_nics(data=data['nics']),
                          desc=data['desc'])
        return machine
    except KeyError:
        tools.error('Importation, machine KeyError')
        exit(1)


def import_nics(data):
    """
    Importation d'une interface nic
    :param data: dict, les donnees des interfaces
    :return: list, Nic
    """
    try:
        nics = []
        for entry in data:
            nic = Nic(mac=entry['mac'],
                      nom=entry['nom'],
                      adresse=import_adresses(entry['adresses']),
                      etat=entry['etat'])
            nics.append(nic)
        return nics
    except KeyError:
        tools.error('Importation, nics KeyError')
        exit(1)


def import_adresses(data):
    """
    Importation d'une adresse a partir d'informations json
    :param data: dict, donnees d'adresses
    :return: list, Adresse
    """
    try:
        adrs = []
        for entry in data:
            adresse = Adresse(adresse=entry['adresse'],
                              etat=entry['etat'],
                              l_port=[entry['port']['TCP'], entry['port']['UDP']])
            adrs.append(adresse)
        return adrs
    except KeyError:
        tools.error('Importation, adresse KeyError')
        exit(1)


def import_rzo(data, pca, d_machine):
    """
    Importation des donnees reseaux a partir d'information json
    :param data: dict, donnees du reseau
    :param pca: PcAdmin, poste administrateur
    :param d_machine: dict, machine avec les cles pour les ajouter directement
    :return: ReseauL2 ou ReseauL3
    """
    if 'adm_mac' in data:
        key = 'L2'
        rzo = ReseauL2(adm_nic=pca.nic_from_mac(data['adm_mac']),
                       nom=data['nom'],
                       dhcp_info=data['dhcp_info'])
    else:
        key = 'L3'
        rzo = ReseauL3(netaddr=data['netaddr'],
                       nom=data['nom'],
                       gateway=data['gateway'],
                       pubip=data['pubip'],
                       geoloc=data['geoloc'],
                       route=data['route'])

    for k in data['machines']:
        rzo.add_machine(d_machine[str(k)])
    pca.add_rzo(key, rzo)


if __name__ == '__main__':
    pass

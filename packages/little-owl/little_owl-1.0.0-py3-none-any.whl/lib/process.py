#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================================= #
# ===                        IMPORTATIONS                               === #
# ========================================================================= #
from multiprocessing import Process, Queue

import obj.PcAdmin as PcAdmin
import data.settings as settings
from lib import tools, network


# ========================================================================= #
# ===                          FONCTIONS                                === #
# ========================================================================= #
def scan_l3(rzo3, queue=None):
    """
    Realise le scan des voisins.
    et la creation des nouvelles machines
    :param rzo3: ReseauL3, le Reseau a scanner
    :param queue: Queue, file d'attente du multiprocessing
    :return: None
    """
    detects = network.find_neigh(rzo3.netaddr)
    if (not detects) or (detects == NotImplemented):
        return
    for addr in detects:
        if not queue:
            tools.create_neigh(rzo=rzo3, mac=addr[1], ip=addr[0])
        else:
            queue.put([rzo3, addr[1], addr[0]])


def multi_proc():
    """
    Utilisation des multiprocesseurs pour accelerer et fiabiliser la decouverte
    De cette maniere les interface seront en ecoutent lors du scan actif.
    1. Scan passif des interfaces et recherche active en parallele
    2. Ajout des machines decouvertes, et des informations DHCP
    3. Recheche des informations sur internet et scan des ports pour chaque machine decouverte
    Globales utilisee : settings.DUREE, settings.LOCAL_ONLY, setting.LS_MACHINES
    :return: None
    """
    tools.info("#-- Recuperation des informations du PC administrateur --#")
    pcadm = PcAdmin.PcAdmin()
    q_machine = Queue()
    q_dhcp = Queue()
    process = []

    tools.info("#-- Scan passif des interfaces --#")
    tps = settings.DUREE
    for rzo2 in pcadm.rzo['L2']:
        if rzo2.adm_nic.etat:
            p1 = Process(target=rzo2.sniff, args=(tps, q_machine))
            process.append(p1)
            p2 = Process(target=rzo2.find_dhcp, args=(q_dhcp,))
            process.append(p2)

    tools.info("#-- Scan actif des reseaux L3 --#")
    for rzo3 in pcadm.rzo['L3']:
        p3 = Process(target=scan_l3, args=(rzo3, q_machine))
        process.append(p3)

    tools.info("#-- Début multi-processing --#")
    tools.multip_exec(process)

    tools.info("#-- Fin de la phase de decouverte des voisins --#")

    # Ajout des machines decouvertes, vidange de la queue machine
    while not q_machine.empty():
        val = q_machine.get()
        try:
            rzo = pcadm.contains_rzo(val[0])
        except ValueError:
            continue
        tools.create_neigh(rzo, val[1], val[2])

    # Ajout des informations DHCP, vidange de la queue dhcp
    while not q_dhcp.empty():
        val = q_dhcp.get()
        try:
            rzo = pcadm.contains_rzo(val[0])
        except ValueError:
            continue
        rzo.dhcp_info = val[1]

    # Recherche des informations sur Internet
    process = []
    q_inet = Queue()
    if not settings.LOCAL_ONLY:
        tools.info("#-- Recherche informations sur Internet --#")
        for rzo3 in pcadm.rzo['L3']:
            p4 = Process(target=rzo3.internet_info, args=(q_inet,))
            process.append(p4)

    q_port = Queue()
    if settings.PORT_SCAN:
        tools.info("#-- Ports scan des machines decouvertes --#")
        for machine in [ordi for ordi in settings.LS_MACHINES if not isinstance(ordi, PcAdmin.PcAdmin)]:
            p5 = Process(target=machine.host_scan, args=(q_port,))
            process.append(p5)

    tools.multip_exec(process)

    # Ajout des informations internet
    while not q_inet.empty():
        val = q_inet.get()
        try:
            rzo = pcadm.contains_rzo(val[0])
        except ValueError:
            continue
        rzo.pubip = val[1]
        rzo.geoloc = val[2]
        rzo.route = val[3]

    # Ajout des resulats du port scan
    while not q_port.empty():
        val = q_port.get()
        qma = val[0]
        qip = str(val[1].ip())
        qp = [val[2], val[3]]

        for machine in [ordi for ordi in settings.LS_MACHINES if not isinstance(ordi, PcAdmin.PcAdmin)]:
            if qma == machine:
                adresse = machine.addr_from_ip(qip)
                if adresse:
                    adresse.l_port = qp
                    break

    return pcadm


def single_proc():
    """
    Utilisation du programme en single processing
    Temps d'execution plus long.
    Certaines machines d'un RZO L3 peuvent ne pas apparaitre dans une RZO L2
    1. Recherche des informations du pc administrateur
    2. Scan passif des interfaces reseau (reseau L2)
    3. Scan actif des reseau L3
    4. Recherche des informations accessibles sur Internet
    5. Scan des ports
    Globales utilisee : settings.DUREE, settings.LOCAL_ONLY, setting.LS_MACHINES
    :return: PCAdmin, la machine administrateur
    """
    tools.info("#-- Recuperation des informations du PC administrateur --#")
    pcadm = PcAdmin.PcAdmin()

    tools.info("#-- Scan passif des interfaces --#")
    for rzo2 in pcadm.rzo['L2']:
        tools.info("#-- Scan: {} --#".format(rzo2.adm_nic.nom))
        if rzo2.adm_nic.etat:
            rzo2.find_dhcp()
            rzo2.sniff(settings.DUREE)

    tools.info("#-- Scan actif des reseaux L3 --#")
    for rzo3 in pcadm.rzo['L3']:
        tools.info("#-- Scan, {} --#".format(rzo3.nom))
        scan_l3(rzo3)

        if not settings.LOCAL_ONLY:
            tools.info("#-- Recherche informations sur Internet : {} --#".format(rzo3.nom))
            tools.info("--- Ces operations peuvent prendre plusieurs minutes ---")
            rzo3.internet_info()

    if settings.PORT_SCAN:
        tools.info("#-- Ports scan des machines decouvertes --#")
        for machine in [ordi for ordi in settings.LS_MACHINES if not isinstance(ordi, PcAdmin.PcAdmin)]:
            machine.host_scan()

    return pcadm

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Nom : network -  Fonctions utilisant le module Scapy
# Auteur : Goehry Martial
# Date : 2020/06/07

# ========================================================================= #
# ===                        IMPORTATIONS                               === #
# ========================================================================= #
import ipaddress
import json
import ssl
import urllib.request

from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import *
from scapy.layers.l2 import ARP
import lib.tools as tools
import data.settings as settings

# ========================================================================= #
# ===                        CONFIGURATIONS                             === #
# ========================================================================= #
conf.verb = 0
conf.checkIPaddr = False


# ========================================================================= #
# ===                          FONCTIONS                                === #
# ========================================================================= #
def ping_icmp(target, source, ttl=64):
    """
    Realise un ping en ICMP vers la cible
    infos : ICMP.type : 0 = echo-reply,
                        11 = time-exceeded
    :param target: str, Ip de la cible que l'on cherche a atteindre
    :param source: str, Ip source
    :param ttl: Int, time to live (64 defaut)
    :return Tuple | None,  (IP.src, ICMP.type)
    """
    try:
        reponses, perdus = sr(IP(src=source, dst=target, ttl=ttl) / ICMP(), timeout=5)
        if not reponses:
            return None
        return reponses[0][1][IP].src, reponses[0][1][ICMP].type
    except PermissionError:
        return None


def ping_tcp(target, source, dp=80):
    """
    Effectuer un ping sur un port particulier de la cible en TCP,
    Le but etant d'effectuer un ping sur un materiel qui interdit les requetes ICMP
    :param target: str, la cible que l'on cherche a atteindre
    :param source: str, la source de la requete
    :param dp: destination port (80 defaut)
    :return Tuple | None,
    """
    try:
        reponses, perdus = sr(IP(src=source, dst=target) / TCP(dport=dp), timeout=5)
        if not reponses:
            return None
        if reponses[0][1][TCP].flags == 18:
            return reponses[0][1][IP].src, reponses[0][1][TCP].sport
        return None
    except PermissionError:
        return None


def ping_udp(target, source, dp=53):
    """
    Effectuer un ping sur un port particulier de la cible en TCP,
    :param target: la cible a joindre
    :param source: time to live
    :param dp: port a joindre

    Si on obtient pas de reponse le port est peut etre ouvert
    Si on obtient une reponse ICMP on est sur que le port est ferme.

    :return None | Tuple, (IP, port)
    """
    try:
        reponses, perdus = sr(IP(src=source, dst=target) / UDP(sport=RandShort(), dport=dp), timeout=5)
        if reponses:
            return None
        return perdus[0][IP].dst, perdus[0][UDP].dport
    except PermissionError:
        return None


def host_scan(target, tcp_ports=None, udp_ports=None):
    """
    Scan des ports ouverts TCP et UDP ouvert sur une cible
    Utilisation du multi-threading integre dans scapy
    :param target: IPaddress | String, la cible du scan
    :param tcp_ports: INT | LIST, liste des ports TCP a scanner
    :param udp_ports: INT | LIST, liste des ports UDP a scanner
    :return Tuple, (List TCP ouvert, List UDP ouvert)
    """
    # TCP Scan
    if not tcp_ports:
        tcp_ports = settings.TCP_PORTS
    tcp_open = []

    reponses, perdus = sr(IP(dst=target) / TCP(flags='S', dport=tcp_ports), timeout=3)
    for query, resp in reponses:
        if (resp[TCP].flags == 18) and (query[TCP].dport not in tcp_open):
            tcp_open.append(query[TCP].dport)

    # UDP Scan
    if not udp_ports:
        udp_ports = settings.UDP_PORTS
    udp_open = []

    reponses, perdus = sr(IP(dst=target) / UDP(sport=RandShort(), dport=udp_ports), timeout=3)
    for paquet in perdus:
        if paquet[UDP].dport not in udp_open:
            udp_open.append(paquet[UDP].dport)

    return tcp_open, udp_open


def find_neigh(netw):
    """
    Trouver les couples MAC/IP des voisins
    :param netw: String, netaddr avec son masque 192.168.0.0/24
    :return une liste de tuples (IP, MAC)
    """
    if isinstance(netw, ipaddress.IPv4Interface):
        netw = netw.with_prefixlen
    elif isinstance(netw, ipaddress.IPv4Network):
        netw = netw.with_prefixlen
    elif isinstance(netw, str):
        try:
            ipaddress.ip_interface(netw)
        except ValueError:
            tools.error("Fonction find_neigh : '{}' Adresse invalide".format(netw))
            return None
    else:
        return NotImplemented

    try:
        reponse, perdu = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=netw), timeout=5)
        return [(p[1].psrc, p[1].hwsrc) for p in reponse]
    except PermissionError:
        tools.error("Fonction find_neigh : Operation non permise")
        return None


def find_dhcp(iface):
    """
    Recuperation des informations a partir du serveur DHCP
    iface : l'interface utiliser pour lancer la recherche
    Retourne :  0.   l'adresse du serveur bootp,
                1.   le masque de sous reseau,
                2.   la route par defaut (gateway),
                3.   l'adresse du serveur dhcp,
                4-5. les adresses des dns 1 & 2
                6.   le nom de domaine
                7.   l'adresse IP proposee
                7.   l'adresse mac de l'interface iface
    """

    rq = Ether(dst="ff:ff:ff:ff:ff:ff") / \
         IP(src="0.0.0.0", dst="255.255.255.255") / \
         UDP(sport=68, dport=67) / \
         BOOTP(chaddr=get_if_raw_hwaddr(iface)[1]) / \
         DHCP(options=[("message-type", "discover"), "end"])

    try:
        reponse, perdu = srp(rq, timeout=10)
    except PermissionError:
        tools.info("find DHCP, Permission non accordee")
        return None

    if not reponse:
        return None

    bootp_srv = reponse[0][1][BOOTP].siaddr
    yiaddr = reponse[0][1][BOOTP].yiaddr
    hwdst = reponse[0][1][Ether].dst

    opts = reponse[0][1][DHCP].options
    dhcp_mask = member('subnet_mask', opts, key=lambda x: x[0])[1]
    gateway = member('router', opts, key=lambda x: x[0])[1]
    dhcp_srv = member('server_id', opts, key=lambda x: x[0])[1]
    dns1, dns2 = member('name_server', opts, key=lambda x: x[0])[1:]
    domain = member('domain', opts, key=lambda x: x[0])[1].decode()

    return [bootp_srv, dhcp_mask, gateway, dhcp_srv, dns1, dns2, domain, hwdst, yiaddr]


def member(objet, liste, key=lambda x: x):
    """
    Regarder si un element est membre d'une liste
    Si c'est le cas on le retourne
    Sinon on return None
    objet : un objet python
    liste : un iterable
    key : une fonction d'extraction eventuelle d'un element
    Retourne l'element s'il a ete trouve, sinon None
    """
    try:
        for element in liste:
            if key(element) == objet:
                return element
    except (TypeError, ValueError):
        return None
    return None


def check_mac_ip(mac, ip):
    """
    Utilise le protocol ARP pour controler si une netaddr MAC utilse une netaddr IP specifique
    :param mac: str, Adresse Mac
    :param ip: str, netaddr IP
    :return: bool, True si l'IP est utilisee par l'netaddr Mac
    """
    req = Ether(dst=mac)/ARP(pdst=ip)
    r, p = srp(req, timeout=2)
    if r:
        return True
    return False


def p_scan(netf, duration):
    """
    Declenche un Scan passif afin de decouvrir les hotes present sur un reseau.
    Le but est de trouver les voisins quand il n'y a pas serveur DHCP
    Utile seulement si l'interface est UP, plus efficace si l'interface est en PROMISC
    :param netf: str, l'interface a sniffer
    :param duration: int, le temps de sniff en secondes
    :return scapy.plist.PacketList, les paquets captures
    """
    try:
        sniffed = sniff(iface=netf, store=True, timeout=duration)
    except (KeyboardInterrupt, PermissionError):
        sniffed = None
    return sniffed


def paquets_analyse(paquets_set):
    """
    Analyse les paquets ARP et IP d'un set de paquets captures.
    Recuperation des adresses MAC et adresses IP associees
    :param paquets_set: scapy.plist.PacketList, ensemble des paquets recuperes d'un scan scapy
    :return dict, adresses MAC avec adresse IP correspondantes {MAC : [IP, ...]}
    """
    couple = {}
    if not paquets_set:
        return couple

    for paquet in paquets_set:
        if ARP in paquet:
            mac = paquet[ARP].hwsrc
            ip = paquet[ARP].psrc
        elif IP in paquet:
            mac = paquet[Ether].src
            ip = paquet[IP].src
        else:
            continue

        if mac in couple.keys():
            if ip in couple[mac]:
                continue
            couple[mac].append(ip)
        else:
            couple[mac] = [ip]

    return couple


def get_public_ip(ip):
    """
    Recupere l'adresse IP public de l'hote en utilisant la requete du moteur de recherche duckduckgo
    On recherche dans la page web le texte :
    Your IP address is ([0-9]{1,3}\.){3}[0-9]{1,3} in <a href=.*>.*</a>
    :param ip: str, adresse IP
    :return str, str, Public IP et localisation
    """
    query = "https://duckduckgo.com/?q=whats++my+ip&t=canonical&ia=answer"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((ip, 65432))
            context = ssl.create_default_context()
            context.wrap_socket(sock, server_hostname="duckduckgo.com")
            r = urllib.request.urlopen(query, context=context)
            page = r.read().decode()

            regex = re.compile(r"Your IP address is (?P<myip>(\d{1,3}\.){3}\d{1,3}) in <a (.)*>(?P<geoloc>(.)+)</a>")
            match = re.search(regex, page)
            if match:
                return match.group('myip'), match.group('geoloc')
    except OSError:
        tools.debug("Get public ip: OS erreur")
    except ssl.CertificateError:
        tools.error("Get public ip: Erreur de certificat")
    return None, None


def get_loc(target):
    """
    Recupere les coordonnees de la cible en utilisant le site ipinfo.com et json
    :param target : adresse IP ou nom
    :return tuple, str la ville, la region, le pays et les coordonnees en lat/long
    """
    if not re.match("(\d{1,3}\.){3}\d{1,3}", target):
        print("{} : Invalide, Ip demandee".format(target), file=sys.stderr)
        return None

    url = "http://ipinfo.io/" + target + "/json"
    reponse = urllib.request.urlopen(url)
    if not reponse:
        return None

    try:
        data = json.load(reponse)
    except json.decoder.JSONDecodeError:
        return None
    ville = data.get('city', '*')
    region = data.get('region', '*')
    pays = data.get('country', '*')
    coord = data.get('loc', '*')

    return ville, region, pays, coord


def trcroute(target, source, fping=ping_icmp, minttl=1, maxttl=8):
    """
    Realise un traceroute vers une destination quelconque.
    Le but est de determiner les elements fixe de la route vers internet.
    target : la cible vers l'exterieur du reseau local
    source : Ip source
    :param fping: la fonction a utiliser pour realiser le ping
    :param minttl : ttl minimum
    :param maxttl : ttl maximum
    :return list, liste des adresses IP de la route vers la target
    """
    route = {}
    for x in range(minttl, maxttl):
        hop = fping(target, source, ttl=x)
        if hop:
            hop = hop[0]
        else:
            continue
        if member(hop, list(route.values())):
            break
        route[x] = hop

    return route


def get_route(source):
    """
    Lancer plusieurs trcroute vers plusieurs destinations.
    Determiner ainsi les points de passages recurants
    :param source: str, IP source
    :return dict, {key = int-nombre de saut, value = str-adresse_ip}
    """
    sites = [
        "www.google.com",
        "www.sputniknews.com",
        "www.lequipe.fr",
        "www.japantimes.co.jp",
        "www.baidu.com",
        "www.brandsouthafrica.com"
    ]

    sroute = trcroute(sites[0], source)
    hop2del = []
    for site in sites[1:]:
        rte = trcroute(site, source)
        if not rte:
            continue

        for hop, ip in sroute.items():
            if hop not in rte:
                hop2del.append(hop)
                continue
            if not ip == rte[hop]:
                hop2del.append(hop)

        for hop in hop2del:
            if hop in sroute:
                del sroute[hop]

    return sroute


def reverse_dns(target):
    """
    Recuperation du nom de domaine a partir de l'adresse IP en utilisant le module inclu dans socket
    :param target: str, Adresse IP cible
    :return str, le nom de domaine associe a l'adresse IP
    """
    try:
        return socket.gethostbyaddr(target)[0]
    except socket.herror:
        return "Inconnu"

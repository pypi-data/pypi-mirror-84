#! /usr/bin/env python3
# coding: utf-8

# Nom : little_owl - outil d'aide a l'administration reseau
# Auteur : Goehry Martial
# Date : 2020/05/28

# Accès à la base de données en chemin relatif

# usage: little_owl [-h] [-q] [-d SEC] [-l] [-s | -m | -r JSONF] [-e [JSONF]]
#                  [-o [FICHIER]] [--update-path] [-p]
#
# Decouverte des reseaux et machines voisines a partir du poste admin
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -q, --quiet           l'affichage des infos et erreurs est desactivee
#   -d SEC, --duree SEC   temps en seconde pour le scan passif
#   -l, --local           recherche uniquement les informations des reseaux
#                         locaux
#   -s, --single-p        deroule sequentiel du programme
#   -m, --mulpi-p         realisation de scans en parallele (par defaut)
#   -r JSONF, --read JSONF
#                         lecture et affichage d'un fichier de donnees au format
#                         json
#   -e [JSONF], --export [JSONF]
#   -p, --no-port       Ne scanne pas les ports ouverts pour les machines
#                         detectees


# ========================================================================= #
# ===                       IMPORTATIONS                                === #
# ========================================================================= #
import argparse
import os
import sys

import data.settings as settings
from lib import tools, jsondata, process


# ========================================================================= #
# ===                    GESTION DES ARGUMENTS                          === #
# ========================================================================= #
def args_handle():
    parser = argparse.ArgumentParser(prog="little_owl",
                                     description="Decouverte des reseaux et machines voisines a partir du poste de travail."
                                                 " Scan passif, actif, et des ports ouverts.",
                                     epilog="Attention ce programme n'est absolument pas discret, ENJOY")
    gp_process = parser.add_mutually_exclusive_group()

    parser.add_argument('-q', "--quiet",
                        help="l'affichage des infos et erreurs est desactive",
                        action="store_true")
    parser.add_argument('-d', "--duree",
                        type=int,
                        help="temps en seconde pour le scan passif",
                        default=20,
                        dest='sec')
    parser.add_argument('-l', '--local',
                        help="recherche uniquement les informations des reseaux locaux",
                        action="store_true")
    gp_process.add_argument('-s', "--single-p",
                            help="deroule sequentiel du programme",
                            action="store_true")
    gp_process.add_argument('-m', "--mulpi-p",
                            help="realisation de scans en parallele (par defaut)",
                            action="store_true")
    gp_process.add_argument('-r', "--read",
                            help="lecture et affichage d'un fichier JSONF de donnees au format json",
                            dest='importf',
                            metavar='jsonf'.upper())
    parser.add_argument('-e', "--export",
                        help="fichier JSONF pour l'exportation des donnees au format json",
                        dest='exportf', metavar='jsonf'.upper(),
                        nargs='?',
                        default=False)
    parser.add_argument('-o', "--output",
                        help="fichier FICHIER de sortie pour l'affichage",
                        dest='fichier',
                        nargs='?',
                        default=False)
    parser.add_argument('-p', '--no-port',
                        help="Ne scanne pas les ports ouverts pour les machines detectees",
                        action="store_true")

    return parser.parse_args()


# ========================================================================= #
# ===                           MAIN                                    === #
# ========================================================================= #
def main():
    args = args_handle()
    settings.QUIET = args.quiet
    settings.LOCAL_ONLY = args.local
    settings.DUREE = 0 if args.sec < 0 else args.sec
    settings.PORT_SCAN = not args.no_port

    if args.fichier is False:
        out_file = sys.stdout
    elif args.fichier is None:
        out_file = "lowl.out"
        c = 0
        while os.path.exists(out_file):
            out_file = "lowl.{}.out".format(c)
            c += 1
    else:
        out_file = args.fichier

    try:
        if args.importf:
            tools.info("Importation : {}".format(args.importf))
            pc = jsondata.import_json(args.importf)
        elif args.single_p:
            pc = process.single_proc()
        else:
            pc = process.multi_proc()

        tools.show_result(pc, out_file)

        if args.exportf is not False:
            jsondata.export_json(pc, args.exportf)

    except KeyboardInterrupt:
        print("Fermeture utilisateur")
        exit(1)


if __name__ == '__main__':
    main()

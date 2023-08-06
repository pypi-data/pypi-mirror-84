#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================================= #
# ===                              GLOBALES                             === #
# ========================================================================= #
import os

PATH_TO_MAC_DB = os.path.dirname(os.path.realpath(__file__)) + '/macaddress.io-db.json'

TCP_PORTS = [7, 15, 20, 21, 22, 23, 25, 37, 42, 43, 53, 67, 68, 80, 143, 161, 194, 443, 546,
             547, 554, 989, 990, 992, 993, 995, 1080, 1194, 1433, 1900, 3000, 8080, 8081, 8888]
UDP_PORTS = [7, 37, 53, 67, 68, 161, 194, 546, 547, 554, 1080, 1194, 1433, 1900]

LS_MACHINES = []

DEBUG = False
QUIET = False
DUREE = 20
LOCAL_ONLY = False
PORT_SCAN = True

# -*- coding: utf-8 -*-
#Le programme suivant permet de cr�er unseul fichier .exe pour le script python saisie.py
#Ce programme necessite obligatoirement le pachage py2exe de python qui se trouve dans www.py2exe.org
#Le programme est dedi� sous plat form windows et necessite le fichier MSVCR90.dll dans C:\Python27\DLLs\
#
#
from distutils.core import setup
import py2exe
import os
import sys
import subprocess
import shutil


setup(
    console=['main.py'],
    options={
            "py2exe":{
                    "skip_archive": True,
                    "unbuffered": True,
                    "optimize": 2
            }
    }
)

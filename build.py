#!/usr/bin/env python3

import os

python_exe = "c:/python34/python.exe"
pyqt5_dir = "c:/python34/lib/site-packages/PyQt5"
pyuic5_exe = pyqt5_dir + "/pyuic5.bat"
pyrcc5_exe = pyqt5_dir + "/pyrcc5.exe"

dopewars_dir = "./dopewars"
templates_dir = dopewars_dir + "/templates"
templates = ["fight_dialog.ui",
             "finances_dialog.ui",
             "main_window.ui",
             "store_dialog.ui",
             "transact_dialog.ui"]

for t in templates:
    pyname = "qt_"+t.lower().replace(".ui", ".py")
    os.system("%s %s/%s > %s/%s" % (pyuic5_exe,
                                    templates_dir,
                                    t,
                                    dopewars_dir,
                                    pyname))

os.system("%s %s/dopewars.qrc > %s/dopewars_rc.py")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import codecs
import assets
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QTranslator

current_dir = os.path.dirname(os.path.realpath(__file__))

class HAEClient:
    def __init__(self, app_dir):
        from codec import Codec
        from window import Window
        from system import System
        from datajar import DataJar
        from filesystem import FileSystem

        manifest_json = os.path.join(app_dir, "manifest.json")

        try:
            manifest = json.load(codecs.open(manifest_json, 'r', 'utf-8'))
        except:
            manifest = {}

        for key in assets.manifest:
            if key in manifest:
                assets.manifest[key] = manifest[key]

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(assets.manifest['name'])
        self.app.setApplicationVersion(assets.manifest['version'])

        assets.sys = System()
        assets.codec = Codec()
        assets.fs = FileSystem()
        assets.dataJar = DataJar()

        translator = QTranslator()
        if translator.load(os.path.join(current_dir, "zh_CN.qm")):
            self.app.installTranslator(translator)

        paths = [app_dir]
        paths += assets.manifest['path'].split("/")
        paths.append("index.html")
        html_index = os.path.join(*paths)
        self.window = Window(None, html_index)

        sys.exit(self.app.exec_())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        HAEClient(sys.argv[1])
    else:
        root_dir = os.path.dirname(current_dir)
        app_dir = os.path.join(root_dir, "assets")
        HAEClient(app_dir)

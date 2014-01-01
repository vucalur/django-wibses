#!/usr/bin/env python

import argparse
import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_wibses.settings'

import fapws._evwsgi as evwsgi
from fapws import base
from fapws.contrib import django_handler

from django_wibses.wibses.app_config import configure_app


parser = argparse.ArgumentParser(description='Starts WIBSES application server.')
parser.add_argument('--port',  default='8000', help="Defaults to 8000")
parser.add_argument('--host', default='127.0.0.1', help="Defaults to 127.0.0.1")
parser.add_argument('--pydict_storages', default='', help="Specifies dictionary storages paths: path1;path2..;pathN")
parser.add_argument('--script_storage', default='', help="Specifies scripts storage path")
args = parser.parse_args()


app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.dirname(app_dir))

dict_storages = None
scripts_storage = None

if len(args.pydict_storages) > 0:
    dict_storages = args.pydict_storages.split(";")
if len(args.script_storage) > 0:
    scripts_storage = args.script_storage


configure_app(scripts_storage=scripts_storage, dictionary_storages=dict_storages)


def application(environ, start_response):
    response = django_handler.handler(environ, start_response)
    return [response]

evwsgi.start(
    args.host,
    args.port
)
evwsgi.set_base_module(base)
evwsgi.wsgi_cb(('', application))
evwsgi.set_debug(0)

try:
    evwsgi.run()
except KeyboardInterrupt:
    sys.exit(0)

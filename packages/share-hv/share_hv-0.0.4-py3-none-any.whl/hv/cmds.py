import click
import io
import json
import os
import re
import requests
import hv.settings as settings
import subprocess
import sys
import tempfile
from pathlib import Path
from hv.adb import Adb

_JSON_PREFIX = 'INSTRUMENTATION_STATUS: stream={"windows":'
_JSON_STRIP = 'INSTRUMENTATION_STATUS: stream='
_HV_URL = 'https://sharehv.com/hv/v1/new-hv'
_APK_PKG = 'com.kbs.hv'
_APK_TEST_PKG = 'com.kbs.hv.test'
_APK_VERSION = '0.0.1'
_APK_VERSION_CODE = '1'

def _find_adb(path_option):
    # Use provided option if provided.
    # Otherwise,
    # 1. Try to find from settings
    if not path_option:
        config = settings.load_settings()
        path_option = settings.get_option(config, 'adb')

    # 2. Try to discover from ANDROID_SDK_ROOT
    if not path_option:
        sdk_root = os.environ.get('ANDROID_SDK_ROOT')
        if sdk_root:
            candidate = os.path.join(sdk_root, 'platform-tools', 'adb')
            if os.access(candidate, os.X_OK):
                path_option = candidate
    

    # 3. Try to discover from PATH
    if not path_option:
        paths = os.environ.get('PATH')
        if paths:
            for p in paths.split(os.pathsep):
                candidate = os.path.join(p, 'adb')
                if candidate and os.access(candidate, os.X_OK):
                    path_option = candidate
                    break
    return path_option


@click.group()
def cli():
    pass

@cli.command()
@click.option('--adb', default='', help='Path to the adb binary to use')
@click.option('--device', default='', help='Use device with the given id')
def grab(adb, device):
    '''Grab a snapshot of the currently displayed app.'''
    adbPath = _find_adb(adb)
    if not adbPath:
        raise click.UsageError('''
Please set the path to your adb binary with
share-hv set adb path/to/adb

The adb binary will usually be at <sdk_root>/platform-tools/adb
''')
    if not Path(adbPath).is_file:
        raise click.UsageError('''
The path to the adb binary
%s
does not exist. Please correct the path with
share-hv set adb path/to/adb
The adb binary will usually be at <sdk_root>/platform-tools/adb
''' % adbPath)

    print('''Using \033[1m%s\033[0m
You can change this with
share-hv set adb path/to/adb
''' % adbPath)
    adb = Adb(adbPath, device)
    print('Obtaining window size')
    (dwidth, dheight) = adb.wmsize()
    print('Setting up instrumentation...')
    shouldUninstall = False
    shouldInstall = False
    info = adb.packageInfo(_APK_PKG)
    infoTest = adb.packageInfo(_APK_TEST_PKG)
    if info is None:
        shouldInstall = True
    else:
        (name, code) = info
        if name != _APK_VERSION or code != _APK_VERSION_CODE:
            shouldInstall = True
            shouldUninstall = True
    if shouldUninstall:
        adb.uninstall(_APK_PKG)
        adb.uninstall(_APK_TEST_PKG)
    if shouldInstall:
        here = os.path.dirname(__file__)
        adb.install(os.path.join(here, 'apks', 'app-v{}.apk'.format(_APK_VERSION)))
        adb.install(os.path.join(here, 'apks', 'app-debug-androidTest.apk'))

    print('Capturing layout...')
    lines = adb.instrument(_APK_TEST_PKG)
    print('Taking screenshot...')
    (fd, screencap) = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    adb.screencap(screencap)

    jsonString = None
    for line in io.StringIO(lines):
        if line.startswith(_JSON_PREFIX):
            jsonString = line[len(_JSON_STRIP):]
            break

    if jsonString is None:
        raise click.UsageError('Unable to dump hierarchy, sorry %s' % lines)

    hvJson = json.loads(jsonString)
    hvJson['width'] = dwidth
    hvJson['height'] = dheight

    print('Uploading...')
    r = requests.post(_HV_URL, data = '{"version":1}')
    r.raise_for_status()
    upload = r.json()
    with open(screencap, 'rb') as f:
        r = requests.put(upload['screencap_url'], headers={'content-type': 'image/png'}, data=f)
        r.raise_for_status()
    os.remove(screencap)
    r = requests.put(upload['hv_url'], headers={'content-type': 'application/json'}, data=json.dumps(hvJson))
    r.raise_for_status()
    print('\nYour snapshot is ready at \033[1m%s\033[0m\n%s' % (upload['url'], upload['message']))

@cli.command()
@click.argument('name')
@click.argument('value')
def set(name, value):
    '''Saves a key-value pair in the settings.'''
    config = settings.load_settings()
    settings.set_option(config, name, value)
    settings.replace_settings(config)


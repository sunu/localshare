# -*- coding: utf-8 -*-

import time
import urllib.request as urllib
from http import server as httpserver
from collections import namedtuple
import os

import zeroconf
import click

import utils


__version__ = '0.1'


@click.group()
@click.version_option(__version__)
def cli():
    """localshare: A commandline utility to share files over local network."""


@cli.command()
@click.argument('filename', nargs=1)
def share(filename):
    """Share a file in the local network."""
    ip = utils.get_ip()
    # port = get_port()

    # check if file exists
    full_path = os.path.join(os.curdir, filename)
    if not os.path.isfile(full_path):
        click.echo("%s is not an existing file. Aborting." % full_path)

    # Bind to port 0. OS assigns a random open port.
    server = httpserver.HTTPServer((ip, 0), utils.LocalFileHandler)
    port = server.server_port
    server.filename = filename

    zc_info = zeroconf.ServiceInfo(
            "_http._tcp.local.",
            "%s._http._tcp.local." % filename,
            utils.ip_to_bytes(ip), port, 0, 0,
            {'filename': filename}
    )
    url = "http://" + ip + ":" + str(port) + "/" + urllib.pathname2url(filename)

    zc_instance = zeroconf.Zeroconf()
    try:
        zc_instance.register_service(zc_info)
        click.echo('Sharing %s at %s' % (filename, url))
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass


def list_files():
    """List all available files."""
    files = []
    zc_instance = zeroconf.Zeroconf()
    listener = utils.ServiceListener()
    Localfile = namedtuple('Localfile', ['filename', 'url'])

    zeroconf.ServiceBrowser(zc_instance, "_http._tcp.local.", listener)

    try:
        if not listener.services:
            click.echo('No files available. Waiting ...')
        while not listener.services:
            time.sleep(0.5)
        click.echo('Peer(s) found.')
        for service in listener.services:
            address = utils.bytes_to_ip(service.address)
            port = service.port
            filename = service.properties[b'filename'].decode('utf-8')
            url = "http://" + address + ":" + str(port) + "/" + \
                  urllib.pathname2url(filename)
            localfile = Localfile(filename, url)
            files.append(localfile)
    except KeyboardInterrupt:
        pass
    return files


@cli.command()
def download():
    """List all available files and download the chosen one."""
    files = list_files()
    for index, file in enumerate(files):
        click.echo("%s - %s - %s" % (index, file.filename, file.url))
    choice = click.prompt('Enter index of file to download:', type=int)
    if 0 <= choice < len(files):
        urllib.urlretrieve(files[choice].url, files[choice].filename)
        click.echo('Download complete.')
    else:
        click.echo('Invalid choice.')


if __name__ == '__main__':
    cli()

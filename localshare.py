# -*- coding: utf-8 -*-

import time
import urllib.request as urllib
from http import server as httpserver
from collections import OrderedDict
import sys

import zeroconf
import click

import utils


__version__ = '0.1'


@click.group()
@click.version_option(__version__)
def cli():
    """localshare: A commandline utility to share files over local network."""


@cli.command()
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.option('--forever', default=False)
def share(filename, forever):
    """Share a file in the local network."""
    ip = utils.get_ip()
    # port = get_port()

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
        if forever:
            server.serve_forever(poll_interval=0.5)
        else:
            server.handle_request()
            click.echo('File downloaded by peer. Exiting')
            sys.exit(0)
    except KeyboardInterrupt:
        pass


def map_files():
    """List all available files."""
    files = OrderedDict()
    zc_instance = zeroconf.Zeroconf()
    listener = utils.ServiceListener()

    zeroconf.ServiceBrowser(zc_instance, "_http._tcp.local.", listener)

    try:
        # Give listener some time to discover available services.
        time.sleep(0.5)
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
            files[filename] = url
    except KeyboardInterrupt:
        sys.exit(0)
    return files


@cli.command()
@click.argument('filename', default='')
def download(filename):
    """List all available files and download the chosen one."""
    files = map_files()
    if filename:
        if filename in files.keys():
            click.echo('File found.')
            click.echo('Download started ...')
            urllib.urlretrieve(files[filename], filename)
            click.echo('Download complete.')
            sys.exit(0)
        else:
            raise SystemExit('%s not found in available files. Aborting.' % filename)
    for index, (filename, url) in enumerate(files.items()):
        click.echo("%s - %s - %s" % (index, filename, url))
    choice = click.prompt('Enter index of file to download', type=int)
    if 0 <= choice < len(files):
        click.echo('Download started ...')
        urllib.urlretrieve(list(files.items())[choice][1], list(files.items())[choice][0])
        click.echo('Download complete.')
    else:
        click.echo('Invalid choice.')


if __name__ == '__main__':
    cli()

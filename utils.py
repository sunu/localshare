# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
import urllib.request as urllib
import os
import socket

import netifaces


class LocalFileHandler(BaseHTTPRequestHandler):
    """Handler to serve local file."""

    def do_GET(self):
        # Continue only if the requested file matches the file we are serving.
        if self.path == urllib.pathname2url(os.path.join('/', self.server.filename)):
            file_path = os.path.join(os.curdir, self.server.filename)
            with open(file_path, 'rb') as f:
                maxsize = os.path.getsize(file_path)
                # Set response header.
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-length', maxsize)
                self.end_headers()
                while True:
                    data = f.read(1024 * 8)
                    if not data:
                        break
                    self.wfile.write(data)
        # If the requested file is not the one we are serving, send a 404 response.
        else:
            self.send_response(404)
            self.end_headers()


class ServiceListener(object):
    """zeroconf listener to find available services."""
    services = []

    def remove_service(*args):
        pass

    def add_service(self, zc_instance, type, name):
        info = zc_instance.get_service_info(type, name)
        if info:
            self.services.append(info)


def get_ip():
    """Get local ip address of the machine."""

    # Get the default gateway interface name
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    # Get the ip address of the machine for that interface
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']


def ip_to_bytes(addr):
    """
    Convert an IPv4 address from dotted-quad string format to 32-bit packed
    binary format,as a string four characters in length.
    """
    return socket.inet_aton(addr)


def bytes_to_ip(packed_ip):
    """
    Convert packed ip byte string to dotted string representation.
    """
    return socket.inet_ntoa(packed_ip)


def get_port():
    """Returns a port number."""
    return 0

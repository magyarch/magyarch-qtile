# -*- coding: utf-8 -*-
# Copyright (C) 2019, Krisztián Veress <krive001@gmail.com>


import requests
import subprocess
from libqtile.widget import base
# from libqtile.log_utils import logger
import socket


class WttrWeather(base.ThreadedPollText):
    """Display https://wttr.in weather."""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('location', 'London', 'Add location'),
        ('units', '&m', '&u USCS &m metric and &M  speed in m/s'),
        ('format', "{c} {C}", '1-4 change variable'),
        ('execute', None, 'Command to execute on click'),
        ("update_interval", 3600.0, "Update interval for the Memory"),
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(WttrWeather.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        """Check internet connection."""

        try:
            host = socket.gethostbyname("8.8.8.8")
            s = socket.create_connection((host, 443))
            s.close()
            connect = True
        except socket.error:
            connect = False

        if connect:
            val = {}
            data_keys = ['c', 'C', 'h', 't', 'f', 'w', 'l', 'm', 'p', 'P']
            url = 'https://v2.wttr.in/' + self.location + '?format=%c\\%C\\%h\\%t\\%f\\%w\\%l\\%m\\%p\\%P' + self.units

            """Check Webpage data valid."""
            try:
                data = requests.get(url, headers={'user-agent': 'curl'})
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                data = False
            except requests.exceptions.TooManyRedirects:
                # Tell the user their URL was bad and try a different one
                data = False
            except requests.exceptions.RequestException:
                # catastrophic error. bail.
                data = False
            if data:

                """Check dict no empty."""
                try:
                    for x, y in zip(data_keys, data.text.split("\\")):
                        val[x] = y
                    output = self.format.format(**val)
                    self.update_interval = 3600
                except KeyError:
                    output = "N/A"
                    self.update_interval = 10
            else:
                output = "N/A"
                self.update_interval = 10
        else:
            output = "N/A"
            self.update_interval = 10
        return output

    def button_press(self, x, y, button):
        base.ThreadedPollText.button_press(self, x, y, button)
        if button == 1 and self.execute is not None:
            subprocess.Popen([self.execute], shell=True)

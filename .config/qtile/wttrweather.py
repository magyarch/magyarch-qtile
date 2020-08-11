# -*- coding: utf-8 -*-
# Copyright (C) 2019, Krisztián Veress <krive001@gmail.com>


import requests
import subprocess
from libqtile.widget import base


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
        val = {}
        data_keys = ['c', 'C', 'h', 't', 'f', 'w', 'l', 'm', 'p', 'P']
        url = 'https://v2.wttr.in/' + self.location + '?format=%c\\%C\\%h\\%t\\%f\\%w\\%l\\%m\\%p\\%P' + self.units
        data = requests.get(url, headers={'user-agent': 'curl'})

        if data.ok is False:
            output = "N/A"
        else:
            for x, y in zip(data_keys, data.text.split("\\")):
                val[x] = y
            output = self.format.format(**val)
        return output

    def button_press(self, x, y, button):
        base.ThreadedPollText.button_press(self, x, y, button)
        if button == 1 and self.execute is not None:
            subprocess.Popen([self.execute], shell=True)

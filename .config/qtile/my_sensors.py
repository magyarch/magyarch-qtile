# -*- coding: utf-8 -*-
# Copyright (c) 2020 MagyArch Linux (krive@magyarchlinux.org)

import psutil

from libqtile.widget import base


class SENSORS(base.InLoopPollText):

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("format", "", "Formatting for field names."),
        ("fahrenheit", False, "Unit set."),
        ("update_interval", 1.0, "Update interval for the Memory"),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(SENSORS.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        if self.fahrenheit:
            unit = "°F"
        else:
            unit = "°C"

        data = psutil.sensors_temperatures(fahrenheit=self.fahrenheit)

        val = {}
        for i in data.keys():
            for x in data.get(i):
                val[x.label] = f'{x.current:.1f}{unit}'
        if not self.format:
            for j in val.keys():
                self.format = "{" + j + "}"
                break
        try:
            out = self.format.format(**val)
        except KeyError:
            out = "N/A"

        return out

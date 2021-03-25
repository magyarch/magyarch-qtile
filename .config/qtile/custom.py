import subprocess
from libqtile.widget import base
# from libqtile.widget import groupbox


class Cpu(base.InLoopPollText):
    """Display CPU usage"""
    defaults = [
        ('update_interval', 1, 'The update interval.'),
        ('threshold', 75, 'Alert treshold value.'),
        ('foreground_alert', 'ff0000', 'Alert color'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Cpu.defaults)
        self.stats = self.get_stats()

    def get_stats(self):
        with open('/proc/stat', 'r') as f:
            # user, nice, system, idle
            val = [int(x) for x in f.readline().split(None, 5)[1:-1]]
        return sum(val[:-1]), sum(val)

    def poll(self):
        stats = self.get_stats()
        use = (100 * (stats[0] - self.stats[0])) // (stats[1] - self.stats[1])
        self.stats = stats
        self.layout.colour = (self.foreground_alert
                              if use > self.threshold else self.foreground)
        return f'{use}%'.ljust(4)


class Hdd(base.InLoopPollText):
    """Display HDD I/O"""
    defaults = [
        ('bytes_per_sector', 512, 'Sector size in bytes.'),
        ('update_interval', 1, 'The update interval.'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Hdd.defaults)
        self.stats = self.get_stats()

    def get_unit(self, b):
        for unit, div in [('GB', 2**30), ('MB', 2**20), ('kB', 2**10)]:
            if b >= div:
                return b / div, unit
        return b, 'B'

    def get_stats(self):
        r = w = 0
        with open('/proc/diskstats', 'r') as f:
            for line in f:
                info = line.split()
                if len(info[2]) == 3:
                    r += int(info[5])
                    w += int(info[9])
        # sectors read, written
        return r, w

    def poll(self):
        stats = self.get_stats()
        r, ru = self.get_unit((stats[0] - self.stats[0]) *
                              self.bytes_per_sector / self.update_interval)
        w, wu = self.get_unit((stats[1] - self.stats[1]) *
                              self.bytes_per_sector / self.update_interval)
        self.stats = stats
        return f'R:{r:-.3g}{ru}/s'.ljust(11) + f'W:{w:-.3g}{wu}/s'.ljust(10)


class Memory(base.InLoopPollText):
    """Display memory usage"""
    defaults = [
        ('update_interval', 1, 'The update interval.'),
        ('threshold', 75, 'Alert treshold value.'),
        ('foreground_alert', 'ff0000', 'Alert color'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Memory.defaults)

    def get_stats(self):
        total = free = None
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    total = int(line.split()[1])
                    if free is not None:
                        break
                elif line.startswith('MemAvailable'):
                    free = int(line.split()[1])
                    if total is not None:
                        break
        return 100 - (100 * free) // total

    def poll(self):
        use = self.get_stats()
        self.layout.colour = self.foreground_alert if use > self.threshold else self.foreground
        return use


class Net(base.InLoopPollText):
    """Displays interface down and up speed"""
    defaults = [
        ('interface', 'wlan0', 'The interface to monitor'),
        ('update_interval', 1, 'The update interval.'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Net.defaults)
        self.stats = self.get_stats()

    def get_unit(self, b):
        for unit, div in [('GB', 2**30), ('MB', 2**20), ('kB', 2**10)]:
            if b >= div:
                return b / div, unit
        return b, 'B'

    def get_stats(self):
        with open('/proc/net/dev', 'r') as f:
            for line in f.readlines()[2:]:
                info = line.split()
                if info[0][:-1] == self.interface:
                    # down, up
                    return float(info[1]), float(info[9])
        return 0, 0

    def poll(self):
        stats = self.get_stats()
        d, du = self.get_unit(
            (stats[0] - self.stats[0]) / self.update_interval)
        u, uu = self.get_unit(
            (stats[1] - self.stats[1]) / self.update_interval)
        self.stats = stats
        return f'D:{d:-.3g}{du}/s'.ljust(21) + "\n" + f'U:{u:-.3g}{uu}/s'.ljust(11)


class Host(base.InLoopPollText):
    """Check host status."""
    defaults = [
        ('address', 'localhost', 'Host address to check.'),
        ('update_interval', 10, 'The update interval.'),
        ('label', '{address}', 'Text to display when host is reachable.'),
        ('label_alert', '{address}',
         'Text to display when host is unreachable.'),
        ('foreground_alert', 'ff0000', 'Alert color'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Host.defaults)

    def poll(self):
        ret = subprocess.run(['ping', '-qc', '1', '-W', '1', self.address])
        if ret.returncode == 0:
            label = self.label.format(address=self.address)
            self.layout.colour = self.foreground
        else:
            label = self.label_alert.format(address=self.address)
            self.layout.colour = self.foreground_alert
        return label
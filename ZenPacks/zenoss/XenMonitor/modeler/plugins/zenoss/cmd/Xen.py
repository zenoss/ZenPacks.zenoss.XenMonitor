###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="""Xen
Plugin to gather information about virtual machines running
under Xen
"""

from sets import Set

import Globals
from Products.DataCollector.plugins.CollectorPlugin \
     import CommandPlugin
from Products.DataCollector.plugins.DataMaps \
     import ObjectMap

class Xen(CommandPlugin):
    """
    Fetch data from a Xen server using ssh and the xm command
    """
    relname = "guestDevices"
    modname = 'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachine'
    command = '/usr/sbin/xm list'

    def copyDataToProxy(self, device, proxy):
        result = CommandPlugin.copyDataToProxy(self, device, proxy)
        proxy.guestDevices = [g.id for g in device.guestDevices()]
        return result
    
    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        log.debug('Results from %s = "%s"', self.command, results)

        rm = self.relMap()
        before = Set(device.guestDevices)
        # Skip the first two lines, which are
        # the header line and the domain-0 line.
        for line in results.split('\n')[1:]:
            if not line or line.startswith('Domain-0'):
                continue

            try:
                # Name  ID Mem(MiB) VCPUs State  Time(s)
                name, id, memory, cpus, state, times = line.rsplit(None, 5)
            except ValueError:
                name = line.split()[0]
                log.warn("Ignoring %s as data missing (eg ID, Mem,"
                         " VCPUs, State or Time info): '%s'",
                         name, line)
                continue

            info = {}
            info['adminStatus'] = True
            info['operStatus'] = (state.find('r') >= 0 or state.find('b') >= 0)
            info['memory'] = int(memory)
            info['osType'] = 'Unknown'
            info['displayName'] = name
            om = self.objectMap(info)
            om.id = self.prepId(name)
            before.discard(om.id)
            rm.append(om)

        for id in before:
            om = self.objectMap(dict(adminStatus=False))
            om.id = id
            rm.append(om)

        return [rm]


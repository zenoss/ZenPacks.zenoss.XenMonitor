######################################################################
#
# Copyright 2007 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

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
    "fetch data from a xen server using ssh and the xm command"
    relname = "guestDevices"
    modname = 'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachine'
    command = '/usr/sbin/xm list'

    def copyDataToProxy(self, device, proxy):
        result = CommandPlugin.copyDataToProxy(self, device, proxy)
        proxy.guestDevices = [g.id for g in device.guestDevices()]
        return result
    
    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        rm = self.relMap()
        before = Set(device.guestDevices)
        # SKIP THE FIRST TWO LINES, WHICH ARE
        # THE HEADER LINE AND THE DOMAIN-0 LINE.
        for line in results.split('\n')[1:]:
            if not line or line.startswith('Domain-0'): continue
            name, data = line[0:40], line[40:]
            id, memory, cpus, state, times = data.split()
            name = name.rstrip()
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


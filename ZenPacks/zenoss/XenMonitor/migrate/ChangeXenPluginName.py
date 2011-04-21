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

import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration
import logging
log = logging.getLogger('zenpack')

class ChangeXenPluginName(ZenPackMigration):
    version = Version(1, 0, 0)

    def migrate(self, pack):
        log.info( 'Renaming Xen plugin to zenoss.snmp.Xen')
        fromPluginName = 'Xen'
        toPluginName = 'zenoss.cmd.Xen'
        vhmDeviceClass = 'Virtual Machine Host'
        deviceClass = pack.dmd.Devices.Server._getOb(vhmDeviceClass).Xen
        collectorPlugins = list( deviceClass.zCollectorPlugins )
        newPluginList = []
        for plugin in collectorPlugins:
            if plugin == fromPluginName:
                newPluginList.append( toPluginName )
            else:
                newPluginList.append( plugin )
        if newPluginList != collectorPlugins:
            deviceClass.setZenProperty( 'zCollectorPlugins',
                                        tuple( newPluginList ) )
        
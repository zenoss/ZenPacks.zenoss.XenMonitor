######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

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
        newPluginList = [ plugin == fromPluginName and toPluginName or plugin
                          for plugin in collectorPlugins ]
        if newPluginList != collectorPlugins:
            deviceClass.setZenProperty( 'zCollectorPlugins',
                                        tuple( newPluginList ) )
        
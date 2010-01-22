###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import logging
log = logging.getLogger("zen.testcases")
import os

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from ZenPacks.zenoss.ZenossVirtualHostMonitor.modeler.plugins.Xen \
    import Xen


class TestXen(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.adm = ApplyDataMap()
        self.plugin = Xen()
        self.device = self.dmd.Devices.createInstance('testDevice')
        self.device.guestDevices = []
        log.setLevel(logging.ERROR)


    def testTruncatedData(self):
        """
        Data format can be truncated
        """
        results = """Name ID Mem VCPUs State Time(s)
AD01_SIMSPOC 53 1024 2 -b---- 14331.1
AD02_SIMSPOC 43 1024 2 -b---- 15503.9
Domain-0 0 3765 16 r----- 11621.6
TS01_SIMSPOC 58 2048 2 -b---- 6058.3
TS02_SIMSPOC 54 2048 2 -b---- 11608.6
TSGW01_SIMSPOC 55 2048 1 -b---- 9271.8
TSGW02_SIMSPOC 48 2048 1 -b---- 9473.5
centos54_x32_GOLD 1024 1 86.3
centos54_x64_GOLD 1024 1 0.0
xenwin2k8x32GPLPV_GOLD 2048 1 0.0
xenwin2k8x32_GOLD 2048 1 0.0
xenwin2kx32_base 2048 1 28.8
zenoss_Centos54x32 57 2050 2 -b---- 2185.9
"""
        
        # Verify that the modeler plugin processes the data properly.
        relmap = self.plugin.process(self.device, results, log)
        self.assertEquals(len(relmap[0].maps), 7)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXen))
    return suite

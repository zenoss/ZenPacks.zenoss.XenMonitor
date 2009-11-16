Xen Monitor
---------------------------

XenMonitor is a ZenPack that allows you to monitor
virtually hosted operating systems running on a Xen hypervisor.
It depends on the prior installation of the ZenossVirtualHostMonitor zenpack.

This zenpack:

     1) Extends ZenModeler to find Guest OS's and add them to Virtual Hosts

     3) Provides templates for collecting resources allocated to Guest OSs.

To Use XenMonitor:

     1) Ensure that you have SSH keys to your Xen servers (as root).

     2) Create your Xen servers using the /Servers/Virtual
     Hosts/Xen device class.  If you have these servers modeled
     already, remove them and recreate them under the Xen device class.
     DO NOT MOVE THEM.

     3) Select the Guest menu and ensure that the guest hosts were
     found when the devices were added.

